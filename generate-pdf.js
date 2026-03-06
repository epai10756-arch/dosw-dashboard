const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const htmlPath = path.resolve(__dirname, 'index.html');
  const pdfPath  = path.resolve(__dirname, '臺北市社會局業務綜覽儀表板.pdf');

  console.log('啟動 Chrome …');
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  });

  const page = await browser.newPage();

  // 設定寬螢幕視窗，確保版面與網頁顯示一致
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });

  console.log('載入頁面 …');
  await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`, {
    waitUntil: 'networkidle0',
    timeout: 60000,
  });

  // 等待 Chart.js 圖表全部渲染完畢
  await page.waitForFunction(() => {
    const canvases = document.querySelectorAll('canvas');
    return canvases.length > 0 &&
      [...canvases].every(c => c.width > 0 && c.height > 0);
  }, { timeout: 20000 });

  // 額外等待動畫與字體
  await new Promise(r => setTimeout(r, 3000));

  console.log('產生 PDF …');
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    landscape: true,
    printBackground: true,
    margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `
      <div style="width:100%;font-size:9px;color:#78716C;padding:0 10mm;display:flex;justify-content:space-between;font-family:sans-serif;">
        <span>臺北市政府社會局 業務綜覽儀表板｜資料基準：114 年 12 月底</span>
        <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
      </div>`,
  });

  await browser.close();
  console.log(`✅ PDF 已儲存：${pdfPath}`);
})();
