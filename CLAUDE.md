# 臺北市政府社會局 — 業務綜覽儀表板

## 專案概述

這是臺北市政府社會局的業務綜覽儀表板，用於呈現社會局各科室的統計數據與 KPI。
目前為純前端靜態網頁，資料直接寫在 HTML 中。

## 專案結構

```
index.html              # 儀表板主頁（純 HTML/CSS/JS，含 Chart.js 圖表）
generate-pdf.js         # 用 Puppeteer 將 index.html 輸出為 A4 橫式 PDF
extract_stats.py        # 從工作報告 .docx 中擷取統計表格資料
package.json            # Node.js 依賴（puppeteer）
BACKEND_PLAN.md         # 後端資料架構規劃建議書
stats_table_extract.txt # extract_stats.py 的輸出結果
```

## 技術棧

- **前端**：純 HTML / CSS / JavaScript（無框架）
- **圖表**：Chart.js 4.x（CDN 引入）
- **字型**：Noto Sans TC（Google Fonts）
- **PDF 產出**：Puppeteer（Node.js）
- **資料擷取**：Python（zipfile + xml.etree）

## 設計風格

- 暖色系（amber / orange 主色調）
- 背景色 `#FFF8F0`，圓角卡片式佈局
- 頂部 sticky 導覽列 + 分頁標籤
- 資料基準：114 年 12 月底

## 常用指令

```bash
# 產生 PDF
node generate-pdf.js

# 從 .docx 擷取統計表格
python extract_stats.py

# 安裝依賴（換電腦時執行）
npm install
```

## 開發注意事項

- index.html 是單一檔案，所有 CSS、JS、資料都內嵌其中
- 修改資料數字時，直接搜尋對應的中文標籤即可定位
- Chart.js 圖表在 `<script>` 區塊最下方初始化
- PDF 輸出為 A4 橫式，有頁首頁尾
- 專案使用繁體中文（台灣），回應與註解請使用繁體中文
