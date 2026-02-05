import chalk from 'chalk';

export const logger = {
  title(text: string): void {
    console.log(chalk.bold.cyan(`\n🇹🇼 ${text}\n`));
  },

  info(text: string): void {
    console.log(chalk.cyan('ℹ'), text);
  },

  success(text: string): void {
    console.log(chalk.green('✓'), text);
  },

  warn(text: string): void {
    console.log(chalk.yellow('⚠'), text);
  },

  error(text: string): void {
    console.log(chalk.red('✗'), text);
  },

  dim(text: string): void {
    console.log(chalk.dim(text));
  },

  box(text: string): void {
    const lines = text.split('\n');
    const maxLen = Math.max(...lines.map(l => l.length));
    const border = '─'.repeat(maxLen + 4);

    console.log(chalk.cyan(`┌${border}┐`));
    lines.forEach(line => {
      const padding = ' '.repeat(maxLen - line.length);
      console.log(chalk.cyan('│'), ` ${line}${padding} `, chalk.cyan('│'));
    });
    console.log(chalk.cyan(`└${border}┘`));
  },

  list(items: string[]): void {
    items.forEach(item => {
      console.log(`  ${chalk.green('●')} ${item}`);
    });
  },

  step(current: number, total: number, text: string): void {
    console.log(chalk.dim(`[${current}/${total}]`), text);
  },
};
