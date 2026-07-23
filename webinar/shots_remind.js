const { chromium } = require('/Users/timofeyzinin/hh-outreach-data/node_modules/playwright-core');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file:///Users/timofeyzinin/sarapulov-zinin-ai/webinar/remind.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(2000);
  for (const id of ['f1','f2','f3','f4']) {
    const el = await p.$('#' + id);
    await el.screenshot({ path: `/Users/timofeyzinin/sarapulov-zinin-ai/webinar/remind_${id}.png` });
  }
  const over = await p.$$eval('.frame', els => els.map((e,i)=> e.scrollHeight>1082 ? i+1:null).filter(Boolean));
  console.log('rendered f1-f4 | overflow:', over.length?over.join(','):'none');
  await b.close();
})();
