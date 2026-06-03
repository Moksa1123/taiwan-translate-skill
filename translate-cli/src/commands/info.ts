import chalk from 'chalk';
import * as path from 'path';
import * as fs from 'fs';
import { logger } from '../utils/logger.js';
import { detectAIType, getAITypeDescription } from '../utils/detect.js';

export async function infoCommand(): Promise<void> {
  logger.title('台灣正體中文翻譯技能包');

  // 讀取 package.json 取得版本
  const packagePath = path.join(__dirname, '..', '..', 'package.json');
  let version = '1.1.0';
  try {
    const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
    version = pkg.version;
  } catch {}

  console.log(chalk.bold('版本：'), chalk.cyan(version));
  console.log();

  // 偵測已安裝的平台
  const { detected } = detectAIType();

  console.log(chalk.bold('功能特色：'));
  console.log(`  ${chalk.green('●')} 2,300+ 詞彙（WordPress 台灣社群官方詞彙表）`);
  console.log(`  ${chalk.green('●')} 14 種 AI 平台支援`);
  console.log(`  ${chalk.green('●')} BM25 智能搜尋引擎`);
  console.log(`  ${chalk.green('●')} 自動翻譯工具`);
  console.log(`  ${chalk.green('●')} PO/POT 檔案支援`);
  console.log();

  if (detected.length > 0) {
    console.log(chalk.bold('偵測到的平台：'));
    detected.forEach(platform => {
      console.log(`  ${chalk.cyan('●')} ${getAITypeDescription(platform)}`);
    });
    console.log();
  }

  console.log(chalk.bold('CLI 命令：'));
  console.log(chalk.dim('  init      - 安裝技能包'));
  console.log(chalk.dim('  list      - 列出支援的平台'));
  console.log(chalk.dim('  info      - 顯示版本資訊'));
  console.log(chalk.dim('  versions  - 檢查可用版本'));
  console.log();

  console.log(chalk.bold('詞彙表來源：'));
  console.log(chalk.dim('  https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary'));
  console.log();

  console.log(chalk.bold('問題回報：'));
  console.log(chalk.dim('  https://github.com/Moksa1123/taiwan-translate-skill/issues'));
  console.log();
}
