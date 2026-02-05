import { readFile, mkdir, writeFile, copyFile, access } from 'node:fs/promises';
import { join } from 'node:path';
import type { PlatformConfig } from '../types/index.js';

// Get the assets directory
function getAssetsDir(): string {
  return join(__dirname, '..', 'assets');
}

const AI_TO_PLATFORM: Record<string, string> = {
  claude: 'claude',
  cursor: 'cursor',
  windsurf: 'windsurf',
  antigravity: 'agent',
  copilot: 'copilot',
  kiro: 'kiro',
  codex: 'codex',
  qoder: 'qoder',
  roocode: 'roocode',
  gemini: 'gemini',
  trae: 'trae',
  opencode: 'opencode',
  continue: 'continue',
  codebuddy: 'codebuddy',
};

async function exists(path: string): Promise<boolean> {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

export async function loadPlatformConfig(aiType: string): Promise<PlatformConfig> {
  const platformName = AI_TO_PLATFORM[aiType];
  if (!platformName) {
    throw new Error(`Unknown AI type: ${aiType}`);
  }

  const configPath = join(getAssetsDir(), 'templates', 'platforms', `${platformName}.json`);
  const content = await readFile(configPath, 'utf-8');
  return JSON.parse(content) as PlatformConfig;
}

async function loadTemplate(templateName: string): Promise<string> {
  const templatePath = join(getAssetsDir(), 'templates', templateName);
  return readFile(templatePath, 'utf-8');
}

function renderFrontmatter(frontmatter: Record<string, string> | null): string {
  if (!frontmatter) return '';

  const lines = ['---'];
  for (const [key, value] of Object.entries(frontmatter)) {
    if (value.includes(':') || value.includes('"') || value.includes('\n')) {
      lines.push(`${key}: "${value.replace(/"/g, '\\"')}"`);
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  lines.push('---', '');
  return lines.join('\n');
}

export async function renderSkillFile(config: PlatformConfig): Promise<string> {
  let content = await loadTemplate('base/skill-content.md');

  const frontmatter = renderFrontmatter(config.frontmatter);

  content = content
    .replace(/\{\{TITLE\}\}/g, config.title)
    .replace(/\{\{DESCRIPTION\}\}/g, config.description);

  // Include quick reference section if supported
  if (config.sections.quickReference) {
    try {
      const quickRef = await loadTemplate('base/quick-reference.md');
      content = quickRef + '\n' + content;
    } catch {
      // Skip if quick-reference.md doesn't exist
    }
  }

  return frontmatter + content;
}

async function copyRecursive(src: string, dest: string): Promise<void> {
  const { stat, readdir, mkdir: mkdirFs, copyFile: copyFileFs } = await import('node:fs/promises');
  const srcStat = await stat(src);

  if (srcStat.isDirectory()) {
    await mkdirFs(dest, { recursive: true });
    const entries = await readdir(src);
    for (const entry of entries) {
      await copyRecursive(join(src, entry), join(dest, entry));
    }
  } else {
    await copyFileFs(src, dest);
  }
}

async function copyTaiwanTranslateAssets(
  targetSkillDir: string,
  sections: PlatformConfig['sections']
): Promise<void> {
  const sourceDir = join(getAssetsDir(), 'taiwan-translate');

  // Copy EXAMPLES.md if enabled
  if (sections.examples && await exists(join(sourceDir, 'EXAMPLES.md'))) {
    await copyFile(join(sourceDir, 'EXAMPLES.md'), join(targetSkillDir, 'EXAMPLES.md'));
  }

  // Copy CLAUDE.md
  if (await exists(join(sourceDir, 'CLAUDE.md'))) {
    await copyFile(join(sourceDir, 'CLAUDE.md'), join(targetSkillDir, 'CLAUDE.md'));
  }

  // Copy references if enabled
  if (sections.references && await exists(join(sourceDir, 'references'))) {
    const refsTarget = join(targetSkillDir, 'references');
    await mkdir(refsTarget, { recursive: true });
    await copyRecursive(join(sourceDir, 'references'), refsTarget);
  }

  // Copy scripts if enabled
  if (sections.scripts && await exists(join(sourceDir, 'scripts'))) {
    const scriptsTarget = join(targetSkillDir, 'scripts');
    await mkdir(scriptsTarget, { recursive: true });
    await copyRecursive(join(sourceDir, 'scripts'), scriptsTarget);
  }

  // Copy data if scripts are enabled
  if (sections.scripts && await exists(join(sourceDir, 'data'))) {
    const dataTarget = join(targetSkillDir, 'data');
    await mkdir(dataTarget, { recursive: true });
    await copyRecursive(join(sourceDir, 'data'), dataTarget);
  }
}

export async function generatePlatformFiles(
  targetDir: string,
  aiType: string,
  isGlobal: boolean = false
): Promise<string[]> {
  const config = await loadPlatformConfig(aiType);
  const createdFolders: string[] = [];
  const os = await import('node:os');

  let skillDir: string;

  if (isGlobal && config.folderStructure.globalRoot) {
    const globalRoot = config.folderStructure.globalRoot.replace(/^~/, os.homedir());
    let skillPath = config.folderStructure.skillPath;

    if (config.folderStructure.globalRoot.includes('global_skills')) {
      skillPath = skillPath.replace(/^skills\//, '');
    }

    skillDir = join(globalRoot, skillPath);
    createdFolders.push(globalRoot);
  } else {
    skillDir = join(
      targetDir,
      config.folderStructure.root,
      config.folderStructure.skillPath
    );
    createdFolders.push(config.folderStructure.root);
  }

  await mkdir(skillDir, { recursive: true });

  // Generate and write SKILL.md
  const skillContent = await renderSkillFile(config);
  const skillFilePath = join(skillDir, config.folderStructure.filename);
  await writeFile(skillFilePath, skillContent, 'utf-8');

  // Copy additional assets
  await copyTaiwanTranslateAssets(skillDir, config.sections);

  return createdFolders;
}

export async function generateAllPlatformFiles(targetDir: string): Promise<string[]> {
  const allFolders = new Set<string>();

  for (const aiType of Object.keys(AI_TO_PLATFORM)) {
    try {
      const folders = await generatePlatformFiles(targetDir, aiType);
      folders.forEach(f => allFolders.add(f));
    } catch {
      // Skip if generation fails
    }
  }

  return Array.from(allFolders);
}

export function getSupportedAITypes(): string[] {
  return Object.keys(AI_TO_PLATFORM);
}
