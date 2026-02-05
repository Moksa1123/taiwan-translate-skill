import chalk from 'chalk';
import * as path from 'path';
import * as fs from 'fs';
import { logger } from '../utils/logger.js';

interface NpmVersion {
  version: string;
  date: string;
}

export async function versionsCommand(): Promise<void> {
  logger.title('版本資訊');

  // 讀取當前版本
  const packagePath = path.join(__dirname, '..', '..', 'package.json');
  let currentVersion = '1.0.0';
  try {
    const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
    currentVersion = pkg.version;
  } catch {}

  console.log(chalk.bold('當前版本：'), chalk.cyan(currentVersion));
  console.log();

  // 嘗試從 npm registry 取得最新版本
  console.log(chalk.dim('正在檢查更新...'));

  try {
    const response = await fetch('https://registry.npmjs.org/taiwan-translate-skill');

    if (response.ok) {
      const data = await response.json() as any;
      const latestVersion = data['dist-tags']?.latest;

      if (latestVersion) {
        console.log(chalk.bold('最新版本：'), chalk.green(latestVersion));

        if (latestVersion !== currentVersion) {
          console.log();
          console.log(chalk.yellow('有新版本可用！'));
          console.log(chalk.dim('更新方式：'));
          console.log(chalk.dim('  npm update -g taiwan-translate-skill'));
          console.log(chalk.dim('  或'));
          console.log(chalk.dim('  npx taiwan-translate-skill@latest init'));
        } else {
          console.log();
          console.log(chalk.green('你已經是最新版本！'));
        }
      }

      // 顯示最近的版本歷史
      const versions = Object.keys(data.versions || {}).slice(-5).reverse();
      if (versions.length > 1) {
        console.log();
        console.log(chalk.bold('最近版本：'));
        versions.forEach((v, i) => {
          const time = data.time?.[v];
          const date = time ? new Date(time).toLocaleDateString('zh-TW') : '';
          const marker = v === currentVersion ? chalk.cyan('●') : chalk.dim('○');
          console.log(`  ${marker} ${v} ${chalk.dim(date)}`);
        });
      }
    } else {
      console.log(chalk.dim('無法取得 npm 版本資訊（套件可能尚未發布）'));
    }
  } catch (error) {
    console.log(chalk.dim('無法連線到 npm registry'));
  }

  console.log();
}
