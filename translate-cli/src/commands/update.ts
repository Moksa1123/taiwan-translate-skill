import chalk from 'chalk';
import { logger } from '../utils/logger.js';
import { detectAIType, getAITypeDescription } from '../utils/detect.js';
import { generatePlatformFiles } from '../utils/template.js';
import { InstallProgress, INSTALL_STEPS, animatedDelay } from '../utils/progress.js';

interface UpdateOptions {
  force?: boolean;
}

export async function updateCommand(options: UpdateOptions): Promise<void> {
  logger.title('更新技能包');

  const { detected } = detectAIType();

  if (detected.length === 0) {
    logger.warn('找不到已安裝的技能包');
    console.log();
    console.log(chalk.dim('請先執行 init 命令安裝：'));
    console.log(chalk.dim('  npx taiwan-translate-skill init'));
    console.log();
    return;
  }

  console.log(chalk.bold('偵測到已安裝的平台：'));
  detected.forEach(platform => {
    console.log(`  ${chalk.cyan('●')} ${getAITypeDescription(platform)}`);
  });
  console.log();

  const progress = new InstallProgress(INSTALL_STEPS);
  progress.start();

  try {
    await animatedDelay(300);
    progress.nextStep();

    const targetDir = process.cwd();
    const updatedFolders: string[] = [];

    for (const platform of detected) {
      const folders = await generatePlatformFiles(targetDir, platform, false);
      updatedFolders.push(...folders);
    }

    progress.nextStep();
    await animatedDelay(200);
    progress.nextStep();
    await animatedDelay(150);
    progress.nextStep();
    await animatedDelay(150);

    progress.complete();

    console.log();
    console.log(chalk.bold('已更新的資料夾：'));
    const uniqueFolders = [...new Set(updatedFolders)];
    uniqueFolders.forEach(folder => {
      console.log(`  ${chalk.green('●')} ${folder}`);
    });

    console.log();
    logger.success('技能包更新完成！');
    console.log(chalk.dim('請重新啟動你的 AI 助手以套用更新。'));
    console.log();

  } catch (error) {
    progress.fail('更新失敗');
    if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
}
