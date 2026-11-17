---
guide: sortable-table
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/sortable-table.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 可排序表格

%% line-start id="mwg:sortable-table" %%
## 排序時搬 <tr>，不重建 tbody
- 做法：點擊欄位標題的 `<button>` 後，在 `<tbody>` 內搬動既有 `<tr>`，用 `aria-sort` 標出目前排序欄
- 對手：排序時用 `innerHTML` 或重新 render 重建 `<tbody>`，焦點與列內狀態丟失、view transition 失效（引用："DO NOT re-render the `<tbody>` or `<table>` on sort; it discards focus and state and breaks view transitions."）
- 退路：不需要——搬動既有列與 aria-sort 屬廣泛能力，缺新版搬移／轉場／指令鈕時亦可照樣完成排序
- 解鎖：（缺）

經過：這是 dynamic-sort 的表格版。指南另外要求按鈕放在 `<th>` 裡而不是讓 `<th>` 可點、`aria-sort` 只放在一欄、按鈕文字保持欄名而不改成「升冪排序」。Invoker commands 被推薦用來取代每顆按鈕各綁 click，但這一點沒說舊寫法具體出了什麼問題。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：Invoker commands：Newly（2025-12-12）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:sortable-table:2" %%
## 依欄位型別比對，不比格式化後的字串
- 做法：用 `data-type` 宣告每欄型別，數字與日期依原始值比較
- 對手：直接比對畫面上格式化過的字串，數字與日期排出錯誤順序（引用："DO NOT sort formatted strings when the underlying values are numbers or dates."）
- 退路：不需要——依 data-type 以數值或 Intl.Collator 比對原始資料屬既有標準，所有瀏覽器皆可正確排序
- 解鎖：（缺）

經過：「1,200」排在「950」前面、「2026/1/10」排在「2025/12/3」前面，都是比字串的結果。指南要求每欄宣告型別，不要從內容猜。
%% line-end %%

### 細節（不索引）
- 對手組：比對錯型別
- 支援狀態：—
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
