export type AIType =
  | 'claude'
  | 'cursor'
  | 'windsurf'
  | 'antigravity'
  | 'copilot'
  | 'kiro'
  | 'codex'
  | 'qoder'
  | 'roocode'
  | 'gemini'
  | 'trae'
  | 'opencode'
  | 'continue'
  | 'codebuddy'
  | 'all';

export type InstallType = 'full' | 'reference' | 'workflow';

export interface PlatformConfig {
  platform: string;
  displayName: string;
  installType: InstallType;
  folderStructure: {
    root: string;
    skillPath: string;
    filename: string;
    sharedRoot?: string;
    sharedPath?: string;
    globalRoot?: string;
  };
  scriptPath?: string;
  frontmatter: Record<string, string> | null;
  sections: {
    examples: boolean;
    references: boolean;
    scripts: boolean;
    quickReference?: boolean;
  };
  title: string;
  description: string;
  skillOrWorkflow?: string;
}

export const AI_TYPES: AIType[] = [
  'claude',
  'cursor',
  'windsurf',
  'antigravity',
  'copilot',
  'kiro',
  'codex',
  'qoder',
  'roocode',
  'gemini',
  'trae',
  'opencode',
  'continue',
  'codebuddy',
  'all'
];

export const AI_FOLDERS: Record<Exclude<AIType, 'all'>, string[]> = {
  claude: ['.claude'],
  cursor: ['.cursor'],
  windsurf: ['.windsurf'],
  antigravity: ['.agent'],
  copilot: ['.github'],
  kiro: ['.kiro'],
  codex: ['.codex'],
  qoder: ['.qoder'],
  roocode: ['.roo'],
  gemini: ['.gemini'],
  trae: ['.trae'],
  opencode: ['.opencode'],
  continue: ['.continue'],
  codebuddy: ['.codebuddy'],
};

export const AI_DISPLAY_NAMES: Record<Exclude<AIType, 'all'>, string> = {
  claude: 'Claude Code',
  cursor: 'Cursor',
  windsurf: 'Windsurf',
  antigravity: 'Antigravity / Generic Agent',
  copilot: 'GitHub Copilot',
  kiro: 'Kiro',
  codex: 'Codex',
  qoder: 'Qoder',
  roocode: 'Roo Code',
  gemini: 'Gemini',
  trae: 'Trae',
  opencode: 'OpenCode',
  continue: 'Continue',
  codebuddy: 'CodeBuddy',
};
