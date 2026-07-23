const { chromium } = require('/Users/timofeyzinin/hh-outreach-data/node_modules/playwright-core');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file:///Users/timofeyzinin/sarapulov-zinin-ai/webinar/zoom_bg.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500);
  await p.screenshot({ path: '/Users/timofeyzinin/sarapulov-zinin-ai/webinar/zoom_bg_sarapulov.png' });
  await b.close();
  console.log('done');
})();
