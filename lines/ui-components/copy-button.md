---
guide: copy-button
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/copy-button.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 複製按鈕

%% line-start id="mwg:copy-button" %%
## 回饋期間不要停用按鈕
- 做法：按下複製後顯示回饋，重複點擊時重設計時器與動畫，而不是把按鈕設為 disabled
- 對手：顯示回饋期間停用按鈕，鍵盤焦點掉出去，還宣告了誤導的「不可用」狀態（引用："DO NOT disable the button while showing feedback: copying is idempotent, and disabling drops keyboard focus, announces a misleading unavailable state"）
- 退路：不需要——Clipboard API 已 Widely，不必退路
- 解鎖：（缺）

經過：怕使用者連點而先 disable 按鈕，是很直覺的防呆，但複製本身重複做也沒有副作用。停用反而讓鍵盤使用者下一次 Tab 從頁首重新開始。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Clipboard.writeText：Widely（2020-03-24）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:copy-button:2" %%
## 用 Invoker Commands 宣告複製目標
- 做法：用 `command` + `commandfor` 宣告按鈕要複製哪個元素，取代每顆按鈕各自接 JavaScript
- 對手：（缺）指南只說要取代 "per-button JavaScript wiring"，沒有指出舊寫法具體在哪個時刻出問題（引用："Declare the target with Invoker Commands (`command` + `commandfor`) instead of per-button JavaScript wiring"）
- 退路：保住主要行為——不支援 Invoker Commands 時改用 click listener 呼叫同一複製函式
- 解鎖：用 `command` 與 `commandfor` 宣告複製目標，不必逐顆按鈕接 JavaScript

經過：同一個推薦也出現在 sortable-table 與 accordion：用宣告式屬性取代 click listener。三份指南都沒說手接 listener 會壞在哪裡，只描述新寫法。這是一條槽 3 與戰報都缺的線，適合當上游回饋。
%% line-end %%

### 細節（不索引）
- 對手組：每顆按鈕手接JS
- 支援狀態：Invoker commands：Newly（2025-12-12）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：按鈕要對另一個元素做什麼可以直接寫在 HTML（`command`/`commandfor`），不寫 JS 接線；自訂 `--指令` 讓一顆按鈕觸發任意行為
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:copy-button:3" %%
## 重複的複製鈕用 opacity 隱藏
- 做法：頁面上大量重複的複製按鈕平時隱藏，hover 或聚焦時顯示，只用 `opacity` 藏
- 對手：用 `display: none` 或 `visibility: hidden` 藏按鈕，按鈕從 Tab 順序中消失，鍵盤使用者永遠到不了（引用："`display: none` and `visibility: hidden` remove the button from the tab order, so keyboard users could never reach it."）
- 退路：不需要——CSS opacity 與 hover 媒體查詢已 Widely，不必退路
- 解鎖：（缺）

經過：每個程式碼區塊都放一顆複製鈕會很吵，所以常見做法是 hover 才顯示。問題在於用哪種方式隱藏：大多數隱藏方式同時把按鈕移出 Tab 順序。指南也禁止用 `aria-hidden` 或 `inert` 來「藏」。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：—
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
