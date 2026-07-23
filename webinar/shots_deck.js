const { chromium } = require('/Users/timofeyzinin/hh-outreach-data/node_modules/playwright-core');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  const url = 'file:///Users/timofeyzinin/sarapulov-zinin-ai/webinar/deck.html';
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.waitForTimeout(2500);
  const s = await p.$$('.slide');
  for (let i = 0; i < s.length; i++) {
    await s[i].screenshot({ path: `/Users/timofeyzinin/sarapulov-zinin-ai/webinar/deck_${String(i+1).padStart(2,'0')}.png` });
  }
  const over = await p.$$eval('.slide', els => els.map((e,i)=> e.scrollHeight>722 ? i+1:null).filter(Boolean));
  console.log('slides:', s.length, '| overflow:', over.length?over.join(','):'none');
  const p2 = await b.newPage();
  await p2.goto(url, { waitUntil: 'networkidle' });
  await p2.waitForTimeout(1500);
  await p2.pdf({ path: '/Users/timofeyzinin/sarapulov-zinin-ai/webinar/Zinin-Sarapulov-webinar.pdf', width:'1280px', height:'720px', printBackground:true, pageRanges:'1-17' });
  console.log('pdf done');
  await b.close();
})();
