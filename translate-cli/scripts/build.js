const esbuild = require('esbuild');
const path = require('path');

esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  platform: 'node',
  target: 'node18',
  outfile: 'dist/index.js',
  format: 'cjs',
  define: { __VERSION__: JSON.stringify(require('../package.json').version) },
  external: ['chalk', 'commander', 'ora', 'prompts'],
  banner: {
    js: '#!/usr/bin/env node'
  }
}).then(() => {
  console.log('Build complete!');
}).catch((err) => {
  console.error(err);
  process.exit(1);
});
