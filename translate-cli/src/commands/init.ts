import chalk from 'chalk';
import prompts from 'prompts';
import type { AIType } from '../types/index.js';
import { AI_TYPES } from '../types/index.js';
import { detectAIType, getAITypeDescription } from '../utils/detect.js';
import { InstallProgress, INSTALL_STEPS, animatedDelay, showBanner } from '../utils/progress.js';
import { generatePlatformFiles, generateAllPlatformFiles } from '../utils/template.js';

interface InitOptions {
  ai?: AIType;
  force?: boolean;
  global?: boolean;
}

export async function initCommand(options: InitOptions): Promise<void> {
  // 顯示 Banner
  showBanner(true);

  let aiType = options.ai;

  // Auto-detect or prompt for AI type
  if (!aiType) {
    const { detected, suggested } = detectAIType();

    if (detected.length > 0) {
      console.log(chalk.dim('  偵測到已安裝的平台:'));
      detected.forEach(t => {
        console.log(`    ${chalk.green('●')} ${chalk.cyan(getAITypeDescription(t))}`);
      });
      console.log();
    }

    const choices = AI_TYPES.map(type => ({
      title: getAITypeDescription(type),
      value: type,
    }));

    const response = await prompts([
      {
        type: 'select',
        name: 'aiType',
        message: '你想裝在哪個 AI 助手？',
        choices,
        initial: suggested ? AI_TYPES.indexOf(suggested) : 0,
      },
      {
        type: (prev) => prev !== 'all' && prev !== 'windsurf' ? 'toggle' : null,
        name: 'global',
        message: '要全域安裝嗎？（所有專案都能用）',
        initial: false,
        active: '要',
        inactive: '不要',
      },
      {
        type: 'toggle',
        name: 'force',
        message: '檔案如果已經存在要覆蓋嗎？',
        initial: false,
        active: '要',
        inactive: '不要',
      },
    ]);

    if (!response.aiType) {
      console.log();
      console.log(chalk.yellow('  安裝已取消'));
      console.log();
      return;
    }

    aiType = response.aiType as AIType;

    if (options.global === undefined && response.global !== undefined) {
      options.global = response.global;
    }
    if (options.force === undefined && response.force !== undefined) {
      options.force = response.force;
    }
  }

  const targetDir = process.cwd();

  console.log();
  console.log(chalk.cyan('  目標平台:'), chalk.bold(getAITypeDescription(aiType)));
  if (options.global) {
    console.log(chalk.cyan('  安裝模式:'), chalk.bold('全域安裝'));
  }
  console.log();

  let copiedFolders: string[] = [];

  try {
    const progress = new InstallProgress(INSTALL_STEPS);
    progress.start();

    // Step 1: Loading templates
    await animatedDelay(400);
    progress.nextStep();

    // Step 2: Generating skill files
    if (aiType === 'all') {
      copiedFolders = await generateAllPlatformFiles(targetDir);
    } else {
      copiedFolders = await generatePlatformFiles(targetDir, aiType, options.global);
    }
    progress.nextStep();
    await animatedDelay(300);

    // Step 3-5: File installation steps
    progress.nextStep(); // references
    await animatedDelay(200);
    progress.nextStep(); // scripts
    await animatedDelay(200);
    progress.nextStep(); // data files
    await animatedDelay(200);

    progress.complete();

    // Summary
    const uniqueFolders = [...new Set(copiedFolders)];

    console.log();
    console.log(chalk.dim('  已安裝到:'));
    uniqueFolders.forEach(folder => {
      console.log(`    ${chalk.green('●')} ${folder}`);
    });

    // 下一步提示 - 不用框線
    console.log();
    console.log(chalk.green('  ══════════════════════════════════'));
    console.log(chalk.bold.white('    下一步'));
    console.log(chalk.green('  ══════════════════════════════════'));
    console.log();
    console.log('    1. 重新啟動你的 AI 助手');
    console.log('    2. 試試看: /tw-translate plugin');
    console.log('    3. 或使用: /tw-translate "Hello World"');
    console.log();

    // Interactive tutorial
    const tutorialResponse = await prompts({
      type: 'toggle',
      name: 'showTutorial',
      message: '要看快速上手指南嗎？',
      initial: true,
      active: '要',
      inactive: '不用',
    });

    if (tutorialResponse.showTutorial) {
      console.log();
      console.log(chalk.cyan('  ══════════════════════════════════'));
      console.log(chalk.bold.white('    快速上手指南'));
      console.log(chalk.cyan('  ══════════════════════════════════'));
      console.log();

      console.log(chalk.bold('  功能:'));
      console.log(chalk.dim('    - 詞彙搜尋（2,300+ 詞彙）'));
      console.log(chalk.dim('    - 文字翻譯'));
      console.log(chalk.dim('    - PO/POT 檔案翻譯'));
      console.log();

      console.log(chalk.bold('  常見使用範例:'));
      console.log(`    ${chalk.cyan('$')} /tw-translate plugin`);
      console.log(`    ${chalk.cyan('$')} /tw-translate "Please select a theme"`);
      console.log(`    ${chalk.cyan('$')} /tw-translate file.pot`);
      console.log();

      console.log(chalk.bold('  Python 腳本（進階）:'));
      console.log(`    ${chalk.cyan('$')} python scripts/search.py <關鍵字>`);
      console.log(`    ${chalk.cyan('$')} python scripts/lookup.py "<文字>"   # 詞彙查詢`);
      console.log(`    ${chalk.cyan('$')} python scripts/po.py extract <檔案>  # 抽出未翻譯`);
      console.log(`    ${chalk.cyan('$')} python scripts/po.py validate <檔案> # 翻譯把關`);
      console.log();

      console.log(chalk.green('  提示: 重啟 AI 助手後，直接用 /tw-translate 就可以開始使用了！'));
      console.log();
    }

  } catch (error) {
    console.log();
    console.log(chalk.red('  ══════════════════════════════════'));
    console.log(chalk.bold.white('    安裝失敗'));
    console.log(chalk.red('  ══════════════════════════════════'));
    if (error instanceof Error) {
      console.log(chalk.dim(`  錯誤: ${error.message}`));
    }
    console.log();
    process.exit(1);
  }
}
