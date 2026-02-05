import ora from 'ora';
import chalk from 'chalk';

export const INSTALL_STEPS = [
  { text: '載入模板...', done: '模板載入完成' },
  { text: '生成技能文件...', done: '技能文件已生成' },
  { text: '複製參考文件...', done: '參考文件已複製' },
  { text: '複製腳本...', done: '腳本已複製' },
  { text: '複製資料檔案...', done: '資料檔案已複製' },
];

/**
 * 計算字串的顯示寬度（中文字 = 2，英文字 = 1）
 */
export function getDisplayWidth(str: string): number {
  let width = 0;
  for (const char of str) {
    const code = char.charCodeAt(0);
    // CJK characters, full-width characters
    if (
      (code >= 0x4E00 && code <= 0x9FFF) ||   // CJK Unified Ideographs
      (code >= 0x3400 && code <= 0x4DBF) ||   // CJK Unified Ideographs Extension A
      (code >= 0xFF00 && code <= 0xFFEF) ||   // Full-width forms
      (code >= 0x3000 && code <= 0x303F)      // CJK Symbols and Punctuation
    ) {
      width += 2;
    } else {
      width += 1;
    }
  }
  return width;
}

/**
 * 根據顯示寬度填充空格
 */
export function padEndDisplay(str: string, targetWidth: number): string {
  const currentWidth = getDisplayWidth(str);
  const padding = targetWidth - currentWidth;
  return str + ' '.repeat(Math.max(0, padding));
}

// ASCII Art Banner
export const BANNER = `
  ╔════════════════════════════════════════════════════╗
  ║                                                    ║
  ║   ████████╗██╗    ██╗    ████████╗██████╗          ║
  ║   ╚══██╔══╝██║    ██║    ╚══██╔══╝██╔══██╗         ║
  ║      ██║   ██║ █╗ ██║       ██║   ██████╔╝         ║
  ║      ██║   ██║███╗██║       ██║   ██╔══██╗         ║
  ║      ██║   ╚███╔███╔╝       ██║   ██║  ██║         ║
  ║      ╚═╝    ╚══╝╚══╝        ╚═╝   ╚═╝  ╚═╝         ║
  ║                                                    ║
  ║          Taiwan Translate Skill v1.0.0             ║
  ║                                                    ║
  ╚════════════════════════════════════════════════════╝
`;

// Mini Banner - 不用框線避免對齊問題
export const MINI_BANNER = `
  ════════════════════════════════════
    Taiwan Translate Skill  v1.0.0
    台灣正體中文翻譯技能包
  ════════════════════════════════════
`;

/**
 * 顯示 ASCII Banner
 */
export function showBanner(mini: boolean = false): void {
  if (mini) {
    console.log(chalk.cyan(MINI_BANNER));
  } else {
    console.log(chalk.cyan(BANNER));
  }
}

/**
 * 進度條
 */
export function progressBar(current: number, total: number, width: number = 30): string {
  const percentage = Math.round((current / total) * 100);
  const filled = Math.round((current / total) * width);
  const empty = width - filled;

  const bar = chalk.cyan('█'.repeat(filled)) + chalk.dim('░'.repeat(empty));
  return `${bar} ${percentage}%`;
}

export class InstallProgress {
  private spinner: ReturnType<typeof ora>;
  private steps: typeof INSTALL_STEPS;
  private currentStep: number;
  private startTime: number;

  constructor(steps: typeof INSTALL_STEPS) {
    this.steps = steps;
    this.currentStep = 0;
    this.startTime = Date.now();
    this.spinner = ora({
      text: this.getStepText(),
      color: 'cyan',
      spinner: {
        interval: 80,
        frames: ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
      }
    });
  }

  private getStepText(): string {
    const step = this.steps[this.currentStep];
    const bar = progressBar(this.currentStep, this.steps.length);
    return `${bar}  ${step.text}`;
  }

  start(): void {
    this.spinner.start();
  }

  nextStep(): void {
    const prevStep = this.steps[this.currentStep];
    this.spinner.stopAndPersist({
      symbol: chalk.green('✓'),
      text: chalk.dim(prevStep.done)
    });

    this.currentStep++;
    if (this.currentStep < this.steps.length) {
      this.spinner = ora({
        text: this.getStepText(),
        color: 'cyan',
        spinner: {
          interval: 80,
          frames: ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        }
      }).start();
    }
  }

  complete(): void {
    const elapsed = ((Date.now() - this.startTime) / 1000).toFixed(1);
    this.spinner.stopAndPersist({
      symbol: chalk.green('✓'),
      text: chalk.dim(this.steps[this.currentStep]?.done || '完成')
    });

    // 安裝成功 - 不用框線
    console.log();
    console.log(chalk.green('  ══════════════════════════════════'));
    console.log(chalk.bold.green('    安裝成功！'));
    console.log(chalk.green('  ══════════════════════════════════'));
    console.log(chalk.dim(`  完成時間: ${elapsed}s`));
  }

  fail(message: string): void {
    this.spinner.fail(chalk.red(message));
  }
}

/**
 * 模擬延遲（用於更好的視覺效果）
 */
export function animatedDelay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 簡單的進度指示器
 */
export function showProgress(text: string): ReturnType<typeof ora> {
  return ora({
    text,
    color: 'cyan',
    spinner: {
      interval: 80,
      frames: ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    }
  }).start();
}

/**
 * 打字機效果
 */
export async function typeWriter(text: string, delay: number = 30): Promise<void> {
  for (const char of text) {
    process.stdout.write(char);
    await animatedDelay(delay);
  }
  console.log();
}

/**
 * 成功訊息框（自動處理中英文寬度）
 */
export function successBox(title: string, lines: string[]): void {
  // 計算所有行的最大顯示寬度
  const maxDisplayWidth = Math.max(
    getDisplayWidth(title),
    ...lines.map(l => getDisplayWidth(l))
  );
  const innerWidth = maxDisplayWidth + 2; // 左右各留 1 格

  console.log();
  console.log(chalk.green('  ╔' + '═'.repeat(innerWidth) + '╗'));
  console.log(chalk.green('  ║') + ' ' + chalk.bold.white(padEndDisplay(title, innerWidth - 2)) + ' ' + chalk.green('║'));
  console.log(chalk.green('  ╟' + '─'.repeat(innerWidth) + '╢'));

  for (const line of lines) {
    console.log(chalk.green('  ║') + ' ' + padEndDisplay(line, innerWidth - 2) + ' ' + chalk.green('║'));
  }

  console.log(chalk.green('  ╚' + '═'.repeat(innerWidth) + '╝'));
  console.log();
}

/**
 * 訊息框（自動處理中英文寬度）
 */
export function box(title: string, color: typeof chalk.green = chalk.cyan): void {
  const displayWidth = getDisplayWidth(title);
  const innerWidth = displayWidth + 2;

  console.log();
  console.log(color('  ┌' + '─'.repeat(innerWidth) + '┐'));
  console.log(color('  │') + ' ' + title + ' ' + color('│'));
  console.log(color('  └' + '─'.repeat(innerWidth) + '┘'));
  console.log();
}

/**
 * 平台列表動畫
 */
export async function animatedList(items: { name: string; desc: string }[], delay: number = 50): Promise<void> {
  for (const item of items) {
    console.log(`  ${chalk.cyan('●')} ${chalk.bold(item.name.padEnd(12))} - ${chalk.dim(item.desc)}`);
    await animatedDelay(delay);
  }
}
