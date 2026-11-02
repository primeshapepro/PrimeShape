// Génère le PDF d'impression et les aperçus PNG du flyer PrimeShape.
// Usage, depuis la racine du dépôt : node flyer/rendre.js
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const dir = __dirname;
  const hasPhoto = fs.existsSync(path.join(dir, 'photo-andy.jpg'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 3, viewport: { width: 700, height: 900 } });
  await page.goto('file://' + path.join(dir, 'flyer-a5.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: path.join(dir, 'primeshape-flyer-a5.pdf'), preferCSSPageSize: true, printBackground: true });

  // Aperçus au format fini (sans le fond perdu)
  await page.emulateMedia({ media: 'screen' });
  for (const id of ['recto', 'verso']) {
    const trim = await page.$(`#${id} [data-trim]`);
    await trim.screenshot({ path: path.join(dir, `apercu-${id}.png`) });
  }
  await browser.close();
  console.log(`PDF et aperçus générés ${hasPhoto ? 'avec' : 'sans'} photo-andy.jpg.`);
})();
