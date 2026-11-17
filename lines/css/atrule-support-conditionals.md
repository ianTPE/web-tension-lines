---
guide: atrule-support-conditionals
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/atrule-support-conditionals.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依 at-rule 支援與否套用 CSS

%% line-start id="mwg:atrule-support-conditionals" %%
## 用 @supports at-rule() 在 CSS 裡偵測 at-rule
- 做法：用 `@supports at-rule(@property) { … }` 包住只有在該 at-rule 可用時才合理的規則或宣告（可搭配巢狀寫在選擇器裡）
- 對手：（缺）指南只說沒有 `at-rule()` 時要改用屬性／選擇器偵測、註冊屬性技巧，最後才用 JS，沒說這些做法在哪個時刻出問題（引用："When `at-rule()` is not an option, either due to browser support or because deeper detection is needed, you can use the guidance below."）
- 退路：保住主要行為——改用屬性、選擇器或 JS 偵測，保留條件分支但寫法較繞
- 解鎖：CSS 可直接依某個 at-rule 是否受支援來套用規則

經過：以前要知道 `@property`、`@function` 能不能用，只能繞路偵測，或在 JS 檢查 `CSSFunctionRule` 再加 class。新語法讓 CSS 直接分支。但它只能依**名稱**偵測，不能偵測前導語法或描述符；也不要用它包住被偵測的 at-rule 本身，因為不認得的規則本來就會被忽略。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：at-rule()：Limited（Chrome 148、Edge 148、Firefox 157；Safari 不支援）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：依賴 `@property` 或自訂函式的動畫與主題，可以在樣式表裡自帶「不支援就用平面版」的分支，不必在 JS 裡偵測再切 class；元件庫能把漸進增強完全寫在 CSS。Safari 尚未支援
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:atrule-support-conditionals:2" %%
## 偵測 style query 支援要用「永遠為真」的查詢
- 做法：用 `@container style(--a: 1) or (not (style(--a: 1))) { … }` 包住只在 style queries 可用時才套用的規則
- 對手：用 `@supports at-rule(@container style(--a: 1))` 或 `@supports (container-type: style)` 偵測 style queries，兩者都不會成立（引用："IMPORTANT: Do NOT try `@supports (container-type: style)` to detect support for style queries, as this will not work."）
- 退路：沒說——指南未交代不支援 style query 時怎麼辦
- 解鎖：（缺）

經過：其他 container query 類型都能用 `container-type` 的值偵測，偏偏 style queries 沒有對應值，直覺寫法會靜默失敗。指南給的恆真查詢不管用什麼屬性名稱都成立，只要前後兩段相同。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：Container style queries：Newly（2026-05-19，資料取自上游 design-token-reactivity 指南；本指南未給）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

未拆：「不要用 `CSS.registerProperty` 偵測 `@property`，它的支援範圍較廣」——指南沒說誤判後的可觀察現象。
