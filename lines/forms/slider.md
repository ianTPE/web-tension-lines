---
guide: slider
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/slider.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 品牌一致的範圍滑桿

%% line-start id="mwg:slider" %%
## 用 progress() 與 attr() 在 CSS 裡算出滑桿的填色比例
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `input[type="range"]` 上用 `attr(min type(<number>))`、`attr(max …)` 讀屬性，`progress(var(--control-value), min, max)` 算出百分比，餵給 WebKit 軌道的漸層；Firefox 用 `::-moz-range-progress`
- 被什麼擋：WebKit／Blink 沒有對應「已填部分」的偽元素，要讓軌道已填和未填兩段不同色，只能自己同步數值（引用："WebKit/Blink do not provide an equivalent pseudo-element, so sync the live input value to `--control-value` on `input` events"）
- 戰報：部分改善——min／max 由 CSS 從屬性讀出、比例由 `progress()` 計算，腳本只剩一行同步目前值；`attr()` 不支援時（Safari）連 min／max 也要由 JS 同步，`progress()` 不支援時改用 `calc()`（官方宣稱）

經過：品牌滑桿要左邊填色、右邊灰色，Firefox 有偽元素，Chrome 和 Safari 沒有，只能把數值丟進自訂屬性再畫漸層。typed `attr()` 和 `progress()` 把比例計算搬進 CSS，JS 只負責回報目前值。Safari 尚不支援 typed `attr()`，仍要退回整套 JS 同步。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：progress()：Newly（2026-09-01）；attr()：Limited availability。Supported by: Chrome 133, Edge 133, Firefox 155；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：任何「依數值填色」的原生控制項（音量、評分門檻、預算分配條）都能把比例計算留在 CSS，換 min／max 只改 HTML 屬性。目前 Safari 不支援 typed attr()，要靠 JS 補
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:slider:2" %%
## WebKit 與 Firefox 的滑桿偽元素分開寫，不要放同一個選擇器清單
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`::-webkit-slider-thumb` 與 `::-moz-range-thumb`（以及 track）各寫一個規則區塊
- 被什麼擋：把兩家前綴偽元素用逗號放在同一條規則，瀏覽器遇到不認得的那個會丟掉整條規則（引用："browsers drop the entire rule if an unrecognized vendor pseudo-element is encountered."）
- 戰報：勝——分開寫後，每個引擎只忽略自己不認得的那一塊，樣式在兩邊都生效（官方宣稱）

經過：為了少寫幾行把 thumb 樣式合併成一條，結果 Chrome 不認得 `-moz-`、Firefox 不認得 `-webkit-`，兩邊都整條失效，滑桿退回系統樣式。拆成兩個區塊就各自生效。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：不適用（指南未附前綴偽元素的支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 3 個糾錯提醒未拆：用原生 `<input type="range">` 而非 div 自製（指南只說原生保有鍵盤、觸控與可及性，沒說自製版在哪個時刻出錯）；不要在滑桿偽元素上用 `::before`／`::after`（生成內容在表單控制項上不可互通）；拿掉原生外觀後要補可見的焦點樣式。
