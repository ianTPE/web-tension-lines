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
- 做法：在 `input[type="range"]` 上用 `attr(min type(<number>))`、`attr(max …)` 讀屬性，`progress(var(--control-value), min, max)` 算出百分比，餵給 WebKit 軌道的漸層；Firefox 用 `::-moz-range-progress`
- 對手：WebKit／Blink 沒有對應「已填部分」的偽元素，要讓軌道已填和未填兩段不同色，只能自己同步數值（引用："WebKit/Blink do not provide an equivalent pseudo-element, so sync the live input value to `--control-value` on `input` events"）
- 退路：保住主要行為——不支援時改用 `calc()` 算比例、並由 JS 同步 min／max，填色照常，但比例不再由 CSS 直接讀屬性算出
- 解鎖：以前 min／max 只能寫死在樣式裡或靠 JS 同步，現在能直接從 `input` 的屬性讀出、再用 `progress()` 在 CSS 算出填色比例

經過：品牌滑桿要左邊填色、右邊灰色，Firefox 有偽元素，Chrome 和 Safari 沒有，只能把數值丟進自訂屬性再畫漸層。typed `attr()` 和 `progress()` 把比例計算搬進 CSS，JS 只負責回報目前值。Safari 尚不支援 typed `attr()`，仍要退回整套 JS 同步。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：progress()：Newly（2026-09-01）；attr()：Limited availability。Supported by: Chrome 133, Edge 133, Firefox 155；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：任何「依數值填色」的原生控制項（音量、評分門檻、預算分配條）都能把比例計算留在 CSS，換 min／max 只改 HTML 屬性。目前 Safari 不支援 typed attr()，要靠 JS 補
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:slider:2" %%
## WebKit 與 Firefox 的滑桿偽元素分開寫，不要放同一個選擇器清單
- 做法：`::-webkit-slider-thumb` 與 `::-moz-range-thumb`（以及 track）各寫一個規則區塊
- 對手：把兩家前綴偽元素用逗號放在同一條規則，瀏覽器遇到不認得的那個會丟掉整條規則（引用："browsers drop the entire rule if an unrecognized vendor pseudo-element is encountered."）
- 退路：不需要——不涉及瀏覽器功能支援，各引擎各寫自己的前綴偽元素本來就是通行做法
- 解鎖：（缺）

經過：為了少寫幾行把 thumb 樣式合併成一條，結果 Chrome 不認得 `-moz-`、Firefox 不認得 `-webkit-`，兩邊都整條失效，滑桿退回系統樣式。拆成兩個區塊就各自生效。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：不適用（指南未附前綴偽元素的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 3 個糾錯提醒未拆：用原生 `<input type="range">` 而非 div 自製（指南只說原生保有鍵盤、觸控與可及性，沒說自製版在哪個時刻出錯）；不要在滑桿偽元素上用 `::before`／`::after`（生成內容在表單控制項上不可互通）；拿掉原生外觀後要補可見的焦點樣式。
