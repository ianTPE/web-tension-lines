---
guide: reduce-style-repetition
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/reduce-style-repetition.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 CSS 函式減少樣式重複

%% line-start id="mwg:reduce-style-repetition" %%
## 用 @function 把重複的樣式邏輯包成帶參數的函式
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `@function --名稱(--參數 <型別>, --參數: 預設值)` 定義函式，以 `result` 回傳值；把漸層 token、依 `@media` 切換的欄數這類邏輯包起來，在屬性值裡呼叫
- 被什麼擋：（缺）只說大型樣式表容易累積重複邏輯，沒說重複在哪個時刻造成什麼可觀察的問題（引用："Maintaining large stylesheets often leads to repetitive logic, especially when dealing with design system tokens like gradients or responsive layout patterns."）
- 戰報：僵持——`@function` 僅 Chrome／Edge 139 起支援，Firefox 與 Safari 不支援；不支援時整個值無效，得先寫一個 fallback 值，或改用 Sass 這類預處理器（官方宣稱）

經過：同一條漸層、同一套「窄螢幕堆疊、寬螢幕 N 欄」的規則在樣式表裡到處複製。`@function` 讓它們變成一個帶型別、帶預設值的函式，函式內的 `result` 依層疊規則取最後符合條件的那個。兩大瀏覽器還沒跟上，跨瀏覽器的專案仍得靠預處理器。
%% line-end %%

### 細節（不索引）
- 對手組：樣式邏輯到處重複
- 支援狀態：@function：Limited（Supported by: Chrome 139 (Aug 2025) and Edge 139 (Aug 2025). Unsupported in: Firefox and Safari.）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前樣式表裡的「公式」只能靠預處理器在建置時展開 → 設計系統可以在瀏覽器端提供 `--fancy-gradient(色1, 色2)`、`--grid-template(欄數)` 這種函式，還能在函式裡依 media 或 container 條件回傳不同值，執行期才決定。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
