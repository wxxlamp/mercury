"""Record the author's decisions and deliver the exact edition they reviewed."""
import argparse
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

STEPS = ('manuscript', 'storyboard', 'preview')
FIELDS = dict(zip(STEPS, ('script', 'storyboard', 'preview')))
PENDING = dict(zip(STEPS, ('manuscript', 'storyboard', 'review')))
APPROVED = dict(zip(STEPS, ('storyboard', 'voice', 'review')))
FOLDERS = dict(zip(STEPS, ('manuscript', 'storyboard', 'review')))


def require(test, message):
    if not test:
        raise ValueError(message)


def rel_file(root, name, folder=None):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts, f'需要片内相对路径：{name}')
    resolved = (root / path).resolve(strict=True)
    require(resolved.is_relative_to(root) and resolved.is_file(), f'文件不在本片：{name}')
    if folder:
        require(path.parts[0] == folder and resolved.is_relative_to(root / folder), f'文件应在 {folder}/：{name}')
    return path.as_posix()


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, data):
    with NamedTemporaryFile('w', dir=path.parent, delete=False, encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    os.replace(stream.name, path)


def check_inputs(root, inputs):
    for name, expected in inputs.items():
        require(digest(root / rel_file(root, name)) == expected, f'版本已变化：{name}，请从受影响阶段重新交审。')


def invalidate(state, step):
    files = state['files']
    for downstream in STEPS[STEPS.index(step):]:
        state['approvals'][downstream] = None
        state['candidates'].pop(downstream, None)
        files[FIELDS[downstream]] = None
        if downstream == 'storyboard':
            files['silent'] = None
        if downstream == 'preview':
            files.update(narration=None, subtitles=None, preview=None, final=None)
    state['stage'] = PENDING[step]


def upstream(root, state, step):
    combined = {}
    for prior in STEPS[:STEPS.index(step)]:
        approved = state['approvals'].get(prior)
        require(approved and approved.get('file') == state['files'].get(FIELDS[prior]), f'需要确认本片的 {prior} 版本。')
        # Older projects may have a recorded decision but no fingerprints.
        require(approved.get('inputs'), f'旧版 {prior} 审批缺少输入记录，请提交对应版本并请作者核对。')
        combined.update(approved['inputs'])
    check_inputs(root, combined)
    return combined


def preview_inputs(root, receipt_name):
    receipt = read(root / receipt_name)
    folder = Path(receipt_name).parent
    require(folder.parent == Path('review') and Path(receipt_name).name == 'render.json', '请指定 review/<版本>/render.json。')
    inputs = dict(receipt['inputs'])
    timeline = rel_file(root, receipt['timeline'])
    require(timeline in inputs, '渲染凭据缺少时间线。')
    plan = read(root / timeline)
    media = {}
    preview = rel_file(root, str(folder / 'preview.mp4'), 'review')
    inputs[preview] = receipt['preview']
    media['preview'] = preview
    renderer = rel_file(root, str(folder / 'film-media.py'), 'review')
    inputs[renderer] = receipt['rendererSha256']
    for key in ('narration', 'subtitles'):
        name = rel_file(root, plan[key], 'audio')
        require(name in inputs, f'渲染凭据中缺少 {key}')
        media[key] = name
    check_inputs(root, inputs)
    return media, inputs


def submit(root, state, args):
    step = args.step
    inherited = upstream(root, state, step)
    file = rel_file(root, args.file, FOLDERS[step])
    inputs = {name: digest(root / name) for name in [file, *(rel_file(root, f) for f in args.input)]}
    media = {}
    if step == 'storyboard':
        require(args.silent, '请用 --silent 指定本次交审的静音预演。')
        media['silent'] = rel_file(root, args.silent, 'review')
        inputs[media['silent']] = digest(root / media['silent'])
    if step == 'preview':
        media, rendered = preview_inputs(root, file)
        inputs.update(rendered)
    for name in inherited.keys() & inputs.keys():
        require(inputs[name] == inherited[name], f'前序已审输入发生变化：{name}')
    invalidate(state, step)
    state['files'].update({k: v for k, v in media.items() if k != 'master'})
    selected = media.get('preview', file)
    state['files'][FIELDS[step]] = selected
    state['candidates'][step] = dict(file=selected, inputs=inherited | inputs, media=media)


def approve(root, state, args):
    upstream(root, state, args.step)
    candidate = state['candidates'].get(args.step)
    require(candidate and candidate['file'] == args.file, '批准的路径与本轮交审版本不符。')
    check_inputs(root, candidate['inputs'])
    if state['approvals'].get(args.step):
        # Replaying a confirmation must not rewind a later stage.
        return
    state['approvals'][args.step] = dict(candidate, note=args.note)
    record = {'step': args.step, **state['approvals'][args.step]}
    history = state.setdefault('reviewHistory', [])
    if not history or record != history[-1]:
        history.append(record)
    state['stage'] = APPROVED[args.step]


def export(root, state):
    upstream(root, state, 'preview')
    approval = state['approvals']['preview']
    require(approval and approval.get('media') and approval['file'] == state['files'].get('preview'),
            '需要作者先确认当前的带声预演。')
    review = Path(approval['file']).parent
    media = approval['media']
    hashes = approval['inputs']
    check_inputs(root, hashes)
    exports = (root / 'exports').resolve(strict=True)
    require(exports == root / 'exports', 'exports 应是本片目录。')
    target = exports / review.name
    files = {'narration.wav': media['narration'], 'subtitles.srt': media['subtitles']}
    renderer = root / review / 'film-media.py'
    receipt = read(root / review / 'render.json')
    manifest = dict(approvals=state['approvals'], timeline=receipt['timeline'], renderer=(review / 'film-media.py').as_posix())
    if target.exists():
        cached = read(target / 'manifest.json')
        final_hash = cached.pop('finalSha256')
        require(not target.is_symlink() and cached == manifest, '同名交付目录已有其他版本。')
        check_inputs(target, {'final.mp4': final_hash, **{dst: hashes[src] for dst, src in files.items()}})
        check_inputs(target / 'project', hashes)
    else:
        with TemporaryDirectory(dir=exports) as temp:
            folder = Path(temp) / 'edition'
            folder.mkdir()
            subprocess.run([sys.executable, str(renderer), str(root), receipt['timeline'], 'master',
                            str(folder / 'final.mp4')], check=True)
            for dest, source in files.items():
                shutil.copyfile(root / source, folder / dest)
                require(digest(folder / dest) == hashes[source], f'交付时输入发生变化：{source}')
            for source in hashes:
                dest = folder / 'project' / source
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / source, dest)
            check_inputs(folder / 'project', hashes)
            (folder / 'project/exports').mkdir(exist_ok=True)
            save(folder / 'project/project.json', dict(state, stage='review'))
            save(folder / 'manifest.json', dict(manifest, finalSha256=digest(folder / 'final.mp4')))
            folder.rename(target)
    state['files']['final'] = (target / 'final.mp4').relative_to(root).as_posix()
    state['stage'] = 'delivered'
    print(state['files']['final'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    sub = parser.add_subparsers(dest='action', required=True)
    send = sub.add_parser('submit')
    send.add_argument('step', choices=STEPS)
    send.add_argument('file')
    send.add_argument('--silent')
    send.add_argument('--input', action='append', default=[], help='本片采用的额外源文件，可重复')
    confirm = sub.add_parser('approve')
    confirm.add_argument('step', choices=STEPS)
    confirm.add_argument('file')
    confirm.add_argument('--note', required=True)
    sub.add_parser('revise').add_argument('step', choices=STEPS)
    sub.add_parser('export')
    args = parser.parse_args()
    root = args.project.resolve(strict=True)
    state_file = root / 'project.json'
    rel_file(root, 'project.json')
    # Lock the directory, since the JSON itself is atomically replaced.
    fd = os.open(root, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        state = read(state_file)
        state.setdefault('candidates', {})
        if args.action == 'submit':
            submit(root, state, args)
        elif args.action == 'approve':
            require(args.note.strip(), '请记录作者实际确认的意见。')
            approve(root, state, args)
        elif args.action == 'revise':
            upstream(root, state, args.step)
            invalidate(state, args.step)
        else:
            export(root, state)
        save(state_file, state)
    finally:
        os.close(fd)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        sys.exit(f'未更新项目：{error}')
