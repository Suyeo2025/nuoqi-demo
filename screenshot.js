const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const filePath = `file://${path.resolve('index.html')}`;
  
  // Desktop screenshot
  const desktopPage = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await desktopPage.goto(filePath, { waitUntil: 'networkidle' });
  await desktopPage.waitForTimeout(2000);
  await desktopPage.screenshot({ path: '/tmp/nuoqi-v14-desktop.png', fullPage: true });
  console.log('Desktop screenshot saved');
  
  // Mobile screenshot
  const mobilePage = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
  await mobilePage.goto(filePath, { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(2000);
  await mobilePage.screenshot({ path: '/tmp/nuoqi-v14-mobile.png', fullPage: true });
  console.log('Mobile screenshot saved');
  
  // Pet section close-up
  const petPage = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await petPage.goto(filePath, { waitUntil: 'networkidle' });
  await petPage.waitForTimeout(1000);
  const teamSection = await petPage.$('#team');
  if (teamSection) {
    await teamSection.scrollIntoViewIfNeeded();
    await petPage.waitForTimeout(1000);
    await teamSection.screenshot({ path: '/tmp/nuoqi-v14-team-section.png' });
    console.log('Team section screenshot saved');
  }
  
  await browser.close();
  console.log('All screenshots complete');
})();
