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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：點擊欄位標題的 `<button>` 後，在 `<tbody>` 內搬動既有 `<tr>`，用 `aria-sort` 標出目前排序欄
- 被什麼擋：排序時用 `innerHTML` 或重新 render 重建 `<tbody>`，焦點與列內狀態丟失、view transition 失效（引用："DO NOT re-render the `<tbody>` or `<table>` on sort; it discards focus and state and breaks view transitions."）
- 戰報：勝——搬動既有列用的是成熟的 DOM 操作，焦點留在標題按鈕上；動畫為選用（官方宣稱）

經過：這是 dynamic-sort 的表格版。指南另外要求按鈕放在 `<th>` 裡而不是讓 `<th>` 可點、`aria-sort` 只放在一欄、按鈕文字保持欄名而不改成「升冪排序」。Invoker commands 被推薦用來取代每顆按鈕各綁 click，但這一點沒說舊寫法具體出了什麼問題。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：Invoker commands：Newly（2025-12-12）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:sortable-table:2" %%
## 依欄位型別比對，不比格式化後的字串
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `data-type` 宣告每欄型別，數字與日期依原始值比較
- 被什麼擋：直接比對畫面上格式化過的字串，數字與日期排出錯誤順序（引用："DO NOT sort formatted strings when the underlying values are numbers or dates."）
- 戰報：勝——依型別比較後順序正確；不涉及新功能（官方宣稱）

經過：「1,200」排在「950」前面、「2026/1/10」排在「2025/12/3」前面，都是比字串的結果。指南要求每欄宣告型別，不要從內容猜。
%% line-end %%

### 細節（不索引）
- 對手組：比對錯型別
- 支援狀態：—
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
