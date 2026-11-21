import { copyFileSync, mkdirSync, readFileSync, realpathSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repository = dirname(dirname(fileURLToPath(import.meta.url)));
const directories = [
  'src', 'skills', 'assets', 'reference', 'manuscript',
  'storyboard', 'audio', 'review', 'exports',
];

function reserveProject(projects, title, useSuffix) {
  for (let number = 1; ; number++) {
    const name = number === 1 ? title : `${title}-${number}`;
    const project = join(projects, name);
    try {
      mkdirSync(project);
      return project;
    } catch (error) {
      if (!useSuffix || error.code !== 'EEXIST') throw error;
    }
  }
}

function createProject(name, manuscript, pasted) {
  if (!name || name !== name.trim() || !/^[\p{L}\p{N}][\p{L}\p{N}\p{M} _.-]*$/u.test(name) || name.endsWith('.')) {
    throw new Error('片名应以字母、汉字或数字开头，可包含空格、点、连字符和下划线。');
  }
  if (manuscript && !statSync(manuscript).isFile()) {
    throw new Error('原稿应是一个文件。');
  }
  const projects = join(repository, 'projects');
  mkdirSync(projects, { recursive: true });
  if (realpathSync(projects) !== projects) {
    throw new Error('projects 必须是仓库中的实际目录。');
  }
  const project = reserveProject(projects, name, pasted !== undefined);
  try {
    for (const dir of directories) {
      mkdirSync(join(project, dir));
      writeFileSync(join(project, dir, '.gitkeep'), '');
    }
    if (manuscript) copyFileSync(manuscript, join(project, 'manuscript/original.md'));
    if (pasted) writeFileSync(join(project, 'manuscript/original.md'), pasted);
    const state = {
      title: basename(project),
      stage: 'manuscript',
      files: {
        original: manuscript || pasted ? 'manuscript/original.md' : null,
        script: null, storyboard: null, narration: null,
        subtitles: null, preview: null, final: null,
      },
      approvals: { manuscript: null, storyboard: null, preview: null },
    };
    writeFileSync(join(project, 'project.json'), JSON.stringify(state, null, 2) + '\n');
  } catch (error) {
    rmSync(project, { recursive: true, force: true });
    throw error;
  }
  return project;
}

const args = process.argv.slice(2);
function main() {
  if (args.length < 1 || args.length > 2) throw new Error('用法：project:new -- --stdin [片名]，或 project:new -- "片名" [原稿路径]');
  if (args[0] === '--stdin') {
    const pasted = readFileSync(0);
    const raw = new TextDecoder('utf-8', { fatal: true }).decode(pasted);
    if (!raw.trim()) throw new Error('粘贴的原稿为空。');
    const firstLine = raw.trim().split(/\r?\n/, 1)[0];
    const words = firstLine.match(/[\p{L}\p{N}]+/gu) || [];
    const suggested = Array.from(words.join(' ')).slice(0, 24).join('').trim();
    return createProject(args[1] ?? (suggested || '新片'), undefined, pasted);
  }
  const [name, input] = args;
  if (input && !/\.(md|txt)$/i.test(input)) throw new Error('支持 UTF-8 Markdown 或纯文本原稿。');
  // npm runs scripts from the package root; resolve user input from the invocation directory.
  const manuscript = input && resolve(process.env.INIT_CWD || process.cwd(), input);
  return createProject(name, manuscript);
}

try {
  console.log(main());
} catch (error) {
  console.error(error.code === 'EEXIST' ? '已有同名文件或项目，请直接打开原项目或换一个片名。' : error.message);
  process.exitCode = 1;
}
