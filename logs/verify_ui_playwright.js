const { chromium } = require('playwright');

async function verifyWebIDE() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);

  await page.waitForSelector('text=Agent IDE', { timeout: 10000 });

  // Playground tab default
  await page.waitForSelector('textarea', { timeout: 10000 });
  await page.getByRole('button', { name: 'Run' }).waitFor({ timeout: 10000 });

  // MCP Builder tab
  await page.getByRole('button', { name: 'MCP Builder' }).click({ force: true });
  await page.waitForTimeout(1500);
  await page.waitForSelector('text=Test Tool', { timeout: 10000 });

  // Agent Builder tab
  await page.getByRole('button', { name: 'Agent Builder' }).click({ force: true });
  await page.waitForTimeout(1500);
  await page.waitForSelector('.react-flow', { timeout: 10000 });

  // DevTools tab
  await page.getByRole('button', { name: 'DevTools' }).click({ force: true });
  await page.waitForTimeout(1500);
  await page.waitForSelector('text=Trace Timeline', { timeout: 10000 });

  await browser.close();
  return true;
}

async function verifyPlayground() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3001', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await page.waitForSelector('text=Playground', { timeout: 10000 });
  await page.waitForSelector('textarea', { timeout: 10000 });
  await page.getByRole('button', { name: 'Run' }).waitFor({ timeout: 10000 });
  await browser.close();
  return true;
}

(async () => {
  const webIdeOk = await verifyWebIDE();
  const playgroundOk = await verifyPlayground();
  console.log('WEB_IDE_OK', webIdeOk);
  console.log('PLAYGROUND_OK', playgroundOk);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
