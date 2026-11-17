---
guide: autofill-highlight-inputs
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/autofill-highlight-inputs.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 自訂自動填入欄位的樣式

%% line-start id="mwg:autofill-highlight-inputs" %%
## 用 :autofill 加一個非顏色的標示，不只靠瀏覽器的底色
- 做法：以 `input:autofill` 加至少一個不靠顏色的指示，例如較粗的內框 `box-shadow: inset 0 0 0 2px …`
- 對手：瀏覽器預設的自動填入標示只有顏色（引用："The browser's default highlight is color only."）
- 退路：保住主要行為——不支援時保留瀏覽器預設底色，欄位照常自動填入，只是沒有非顏色標示
- 解鎖：以前只能忍受瀏覽器預設的顏色底；現在能用 `:autofill` 改掉自動填入欄位的外觀，並加上不靠顏色的指示

經過：分辨不出底色差異的使用者，看不出哪些欄位是瀏覽器幫忙填的。加一圈內框，形狀上也看得出來。Firefox 其他欄位沒有解法，指南也明說不要用 JavaScript 補。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：:autofill：Limited（Supported by: Chrome 110 (Feb 2023), Edge 110 (Feb 2023), and Safari 15 (Sep 2021). Unsupported in: Firefox.）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-highlight-inputs:2" %%
## 自動填入樣式用到 outline 時，聚焦外框要在顏色以外也不同
- 做法：不移除焦點外框；若 autofill 樣式本身用了 `outline`，就給 `:autofill:focus-visible` 一個粗細、樣式或偏移不同的外框
- 對手：自動填入與聚焦都用外框、只差顏色時，看不出哪一欄正在聚焦（引用："give `:autofill:focus-visible` an outline that differs in more than color (e.g. thickness, style, or offset) so focus remains perceivable."）
- 退路：保住主要行為——退回瀏覽器預設標示，焦點仍看得見，只是自動填入與聚焦的區分只剩顏色
- 解鎖：（缺）

經過：一整排欄位都被自動填入、都套上同樣的外框，鍵盤使用者 Tab 過去時，焦點那一欄只差一點顏色，等於沒有焦點框。讓焦點框在粗細或偏移上不同，才分得出來。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：:autofill：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-highlight-inputs:3" %%
## 自動填入樣式不要改 border-width 或 padding
- 做法：`:autofill` 只改不影響版面的屬性（內陰影、邊框顏色），不動 `border-width`、`padding`
- 對手：自動填入狀態會隨使用者操作切換，改到影響版面的屬性，內容就會跟著位移（引用："the state toggles with user activity so that would shift content."）
- 退路：保住主要行為——退回瀏覽器預設標示，本來就沒有自動填入狀態造成的版面位移
- 解鎖：（缺）

經過：使用者一選自動填入建議，欄位邊框變粗、整張表單往下擠；一編輯欄位，狀態解除又縮回去。用內陰影畫框，視覺上一樣明顯，幾何不變。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：:autofill：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-highlight-inputs:4" %%
## 覆寫自動填入顏色時要保留焦點陰影與游標顏色
- 做法：優先保留瀏覽器底色；必須覆寫時用 `inset 0 0 0 100vmax` 陰影蓋背景、`-webkit-text-fill-color` 改文字，另設 `caret-color`，並把原本的焦點 `box-shadow` 重列在同一宣告
- 對手：瀏覽器以 `!important` 設定自動填入的背景與文字色，一般宣告壓不過；用陰影繞路又會取代原本的 `box-shadow` 焦點環（引用："All browsers also set `background-color`, `background-image`, and `color` on autofilled fields with `!important` in their user agent stylesheets, so overriding them relies on workarounds."）
- 退路：保住主要行為——不支援時保留瀏覽器預設底色，自動填入照常，只是改不成自己的配色
- 解鎖：以前改不動瀏覽器的自動填入底色；現在能用 inset 陰影蓋過去、用 `-webkit-text-fill-color` 改文字並另設游標色

經過：品牌底色蓋上去了，焦點環卻消失，因為兩者共用 `box-shadow`。文字繞路只改繪製顏色，`color` 與 `currentColor` 仍是瀏覽器的 `FieldText`，明暗配色也要分別確認。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：:autofill：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
