import { Command } from 'commander';
import { initCommand } from './commands/init.js';
import { listCommand } from './commands/list.js';
import { infoCommand } from './commands/info.js';
import { versionsCommand } from './commands/versions.js';
import { updateCommand } from './commands/update.js';

const program = new Command();

program
  .name('tw-translate')
  .description('🇹🇼 台灣正體中文翻譯技能包安裝工具')
  .version('1.1.0');

program
  .command('init')
  .description('安裝翻譯技能到 AI 助手')
  .option('-a, --ai <type>', 'AI 平台類型')
  .option('-f, --force', '強制覆蓋已存在的檔案')
  .option('-g, --global', '全域安裝（所有專案都能用）')
  .action(initCommand);

program
  .command('list')
  .description('列出支援的 AI 平台')
  .action(listCommand);

program
  .command('info')
  .description('顯示版本資訊')
  .action(infoCommand);

program
  .command('versions')
  .description('檢查可用版本')
  .action(versionsCommand);

program
  .command('update')
  .description('更新已安裝的技能包')
  .option('-f, --force', '強制覆蓋')
  .action(updateCommand);

// 預設顯示 help
if (process.argv.length === 2) {
  program.help();
}

program.parse();
