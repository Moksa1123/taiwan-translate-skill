import chalk from 'chalk';
import { AI_DISPLAY_NAMES } from '../types/index.js';
import { detectAIType } from '../utils/detect.js';
import { animatedDelay } from '../utils/progress.js';

export async function listCommand(): Promise<void> {
  // 標題 - 不用框線避免對齊問題
  console.log();
  console.log(chalk.cyan('  ══════════════════════════════════'));
  console.log(chalk.bold.white('    支援的 AI 平台（共 14 種）'));
  console.log(chalk.cyan('  ══════════════════════════════════'));
  console.log();

  const { detected } = detectAIType();

  const platforms = Object.entries(AI_DISPLAY_NAMES);
  const maxKeyLen = Math.max(...platforms.map(([k]) => k.length));

  // 動畫顯示平台列表
  for (const [key, name] of platforms) {
    const padding = ' '.repeat(maxKeyLen - key.length);
    const isDetected = detected.includes(key as any);
    const marker = isDetected ? chalk.green('●') : chalk.dim('○');
    const displayKey = isDetected ? chalk.cyan(key) : chalk.dim(key);
    const displayName = isDetected ? chalk.bold(name) : chalk.dim(name);
    console.log(`    ${marker} ${displayKey}${padding}  ${displayName}`);
    await animatedDelay(30);
  }

  console.log();
  console.log(`    ${chalk.yellow('★')} ${chalk.yellow('all')}${' '.repeat(maxKeyLen - 3)}  ${chalk.yellow('安裝到所有平台')}`);

  if (detected.length > 0) {
    console.log();
    console.log(chalk.green(`  已偵測到 ${detected.length} 個平台:`));
    detected.forEach(d => {
      console.log(`    ${chalk.green('→')} ${chalk.cyan(AI_DISPLAY_NAMES[d] || d)}`);
    });
  }

  console.log();
  console.log(chalk.dim('  使用方式:'));
  console.log(`    ${chalk.cyan('$')} npx taiwan-translate-skill init`);
  console.log(`    ${chalk.cyan('$')} npx taiwan-translate-skill init --ai claude`);
  console.log(`    ${chalk.cyan('$')} npx taiwan-translate-skill init --ai all`);
  console.log();
}
