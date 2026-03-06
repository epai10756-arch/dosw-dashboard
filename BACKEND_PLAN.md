# 臺北市政府社會局儀表板 — 後端資料架構規劃建議

> 文件性質：技術規劃建議書（供局長及 IT 同仁參考）
> 撰寫時間：115 年 2 月

---

## 一、問題盤點

| 痛點 | 說明 |
|------|------|
| 資料分散 | 數據散落在各科室承辦人電腦，無統一入口 |
| 更新費力 | 需人工蒐集、整理、更新，高度依賴特定人員 |
| 格式不統一 | Excel、Word、PDF 各式各樣 |
| 時效性差 | 月報、季報、年報發布時間不同步 |
| 無 API 介面 | 官網以靜態 PDF/公告為主，不易自動抓取 |

---

## 二、建議架構（三層式，由輕到重）

### ★ 方案 A：輕量靜態 JSON 架構（建議優先採用）

```
儀表板前端 (index.html)
      ↕
  JSON 資料檔案 (data/*.json)
      ↕  ← 人工 or 半自動更新
  各科室 Excel 表單 → 統一轉檔工具
```

**優點：** 無需伺服器、部署簡單、成本低
**適用：** 資料更新頻率低（每月 / 每季），先期快速上線

**實作步驟：**

1. 建立標準化資料範本（Excel → JSON 轉換腳本）：
   ```
   data/
   ├── childcare.json      # 育兒服務指標
   ├── disability.json     # 身障服務指標
   ├── elderly.json        # 高齡照顧指標
   ├── welfare.json        # 弱勢扶助指標
   ├── protection.json     # 保護服務指標
   ├── budget.json         # 預算資料
   └── population.json     # 人口資料
   ```

2. 每份 JSON 格式統一：
   ```json
   {
     "last_updated": "2025-12-31",
     "data_period": "114年12月",
     "source_dept": "婦幼科",
     "metrics": {
       "公辦民營托嬰機構家數": 92,
       "準公共化供給率": 0.81,
       "收托人數": 2008
     }
   }
   ```

3. 提供給各科室的 **「一鍵更新工具」**（Python 腳本）：
   ```
   update_tool/
   ├── update.bat          # Windows 一鍵執行
   ├── excel_to_json.py    # 讀取標準 Excel → JSON
   └── templates/          # 各科室填報範本 Excel
   ```

---

### 方案 B：後端 API 架構（中期建議）

```
儀表板前端 (React/Vue)
      ↕ REST API
  Node.js / Python FastAPI 後端
      ↕
  PostgreSQL 資料庫
      ↕
  定時任務排程 (Scheduler)
  ├── 爬蟲：社會局官網 PDF 解析
  ├── 爬蟲：臺北市政府開放資料平台
  └── 人工上傳介面（各科室）
```

**資料庫設計建議（主要資料表）：**

```sql
-- 核心指標表
CREATE TABLE metrics (
  id          SERIAL PRIMARY KEY,
  category    VARCHAR(50),    -- 'childcare', 'disability', ...
  metric_key  VARCHAR(100),
  metric_name VARCHAR(200),
  value       NUMERIC,
  unit        VARCHAR(50),
  period_year INT,
  period_type VARCHAR(20),    -- 'month', 'quarter', 'year'
  updated_at  TIMESTAMP DEFAULT NOW(),
  source_dept VARCHAR(100)
);

-- 時間序列資料表（趨勢圖）
CREATE TABLE metrics_history (
  metric_id   INT REFERENCES metrics(id),
  period_date DATE,
  value       NUMERIC,
  PRIMARY KEY (metric_id, period_date)
);

-- 更新日誌
CREATE TABLE update_logs (
  id          SERIAL PRIMARY KEY,
  updated_by  VARCHAR(100),
  metric_id   INT,
  old_value   NUMERIC,
  new_value   NUMERIC,
  updated_at  TIMESTAMP DEFAULT NOW()
);
```

---

### 方案 C：整合開放資料平台（長期目標）

臺北市政府「臺北市政府資料開放平台」（data.taipei.gov.tw）已有部分社政資料，長期可：

1. **申請資料上架**：將社會局定期統計資料上架至開放資料平台
2. **API 串接**：前端直接呼叫官方 API，確保資料時效性
3. **官網自動解析**：針對已知結構的 PDF 報表（如月份統計表）開發自動解析程式

---

## 三、降低人工負荷的具體建議

### 3.1 統一填報介面

建立一個簡單的 **Web 填報後台**，各科承辦人每月登入後只需：
- 填入當月主要指標數字（10 個以內的核心 KPI）
- 上傳原始 Excel 附件

系統自動更新儀表板，並記錄更新時間及承辦人。

### 3.2 自動化爬蟲（可行度高的項目）

| 資料項目 | 來源 | 可行度 |
|----------|------|--------|
| 嬰幼兒照顧服務統計（月報 PDF） | 社會局官網公告 | ★★★★ |
| 統計資料發布時程表 | 社會局官網 | ★★★★ |
| 臺北市人口統計 | 臺北市民政局開放資料 | ★★★★★ |
| 身心障礙者統計 | 衛福部身障統計 | ★★★★ |
| 低收入戶統計 | 臺北市政府開放資料平台 | ★★★ |

### 3.3 統計發布日曆提醒

根據社會局統計資料發布時程（114-115 年），建議系統自動：
- 在預定發布日前 3 天，發送 Email/LINE 通知給相關科室
- 逾期未更新則在儀表板標記「資料待更新」警示

---

## 四、建議實施路徑

```
第 1 個月：建立 JSON 資料架構，完成前端儀表板上線
     ↓
第 2–3 個月：開發 Excel → JSON 轉換工具，各科室試跑填報
     ↓
第 4–6 個月：建立後端 API + 資料庫，遷移現有資料
     ↓
第 7–12 個月：開發自動爬蟲，整合開放資料平台
```

---

## 五、技術選型建議

| 層次 | 建議技術 | 理由 |
|------|----------|------|
| 前端 | 純 HTML/CSS/JS（現行） | 無需建置環境，可直接在瀏覽器執行 |
| 資料 | JSON 靜態檔（初期） | 最低建置成本 |
| 後端 API | Python FastAPI | 輕量、語法友善、政府 IT 人員熟悉 |
| 資料庫 | PostgreSQL | 穩定、免費、政府機關常用 |
| 部署 | 市府內部 IIS / Nginx | 符合資安要求 |
| 爬蟲 | Python (requests + pdfplumber) | 可解析 PDF 報表 |

---

## 六、資安注意事項

1. 儀表板本身僅呈現**已公開之彙整統計數據**，不含個資
2. 填報後台需整合市府 SSO 登入驗證
3. 資料傳輸應使用 HTTPS
4. 各科室僅有權更新自己負責的指標，避免誤操作

---

*本文件為初步規劃建議，具體實施細節可依 IT 部門評估調整。*
