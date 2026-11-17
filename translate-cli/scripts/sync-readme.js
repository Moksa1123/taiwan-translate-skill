// Copy the repo README into the npm package so npmjs.com shows the same page.
// Relative links are rewritten to GitHub URLs because the package has no docs/ or LICENSE path above it.
const fs = require('fs');
const path = require('path');

const REPO = 'https://github.com/Moksa1123/taiwan-translate-skill';
const src = path.join(__dirname, '..', '..', 'README.md');
const dst = path.join(__dirname, '..', 'README.md');

const absolute = (link) => {
  if (/^(https?:|#|mailto:)/.test(link)) return link;
  return `${REPO}/blob/main/${link.replace(/^\.\//, '')}`;
};

const text = fs.readFileSync(src, 'utf8')
  .replace(/\]\(([^)\s]+)\)/g, (m, link) => `](${absolute(link)})`)
  .replace(/(href|src)="([^"]+)"/g, (m, attr, link) => `${attr}="${absolute(link)}"`);

fs.writeFileSync(dst, text);
console.log('README synced from repo root');
