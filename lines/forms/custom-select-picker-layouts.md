---
guide: custom-select-picker-layouts
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/custom-select-picker-layouts.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 自訂下拉選單的版面

%% line-start id="mwg:custom-select-picker-layouts" %%
## 用 base-select 加 grid 把原生下拉選單排成卡片格
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<select>` 與 `::picker(select)` 設 `appearance: base-select`，在 `select:open::picker(select)` 上用 `display: grid` 排欄，`<option>` 裡放圖片或 SVG 做成卡片，用 `option:checked` 與 `::checkmark` 標示選中項
- 被什麼擋：（缺）只說可以擺脫傳統的直向清單、不必寫自訂 JS，沒說直向清單或自訂 JS 在哪個時刻出錯（引用："break away from the traditional stacked vertical list and create a rich visual experience without custom JS."）
- 戰報：部分改善——Customizable `<select>` 為 Limited（Firefox 不支援）；不支援時退回系統下拉選單，`<option>` 裡的非文字內容被丟掉、只剩文字；鍵盤左右鍵仍要自己用 script 補（官方宣稱）

經過：色票、emoji、商品款式這類選項，排成格子比一長串文字好挑，以往只能放棄 `<select>` 自己做。現在 picker 可以用 grid 排版，表單送出與值仍是原生的。但原生 select 只認上下鍵，格狀排列需要另外處理鍵盤方向。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Customizable <select>：Limited（Supported by: Chrome 135 (Apr 2025), Edge 135 (Apr 2025), and Safari 27 (Sep 2026). Unsupported in: Firefox.）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前選項只能是一列文字，要圖像化就得自己寫元件 → 顏色、尺寸、貼圖、方案比較這類選擇可以做成格狀卡片的原生 `<select>`，直接參與表單送出。Firefox 退回純文字選單；左右鍵導覽與讀屏的格狀語意仍有限制
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:custom-select-picker-layouts:2" %%
## picker 的版面樣式只掛在 :open 上
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`display: grid` 等版面樣式寫在 `select:open::picker(select)`，不直接寫在 `select::picker(select)`
- 被什麼擋：直接對 `select::picker(select)` 設 `display`，選單關著時 picker 也會顯示出來（引用："If you style `select::picker(select)`, it will make the picker visible even when the select is closed!"）
- 戰報：部分改善——加上 `:open` 後，picker 只在打開時套用版面；這個陷阱只出現在支援 base-select 的瀏覽器（Limited）（官方宣稱）

經過：照一般元素的直覺寫 `::picker(select) { display: grid }`，選單還沒打開，選項格就攤在畫面上。picker 的版面樣式要等選單打開才套。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Customizable <select>：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:custom-select-picker-layouts:3" %%
## <selectedcontent> 一定要包在 <button> 裡
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：要在觸發鈕顯示選中項的豐富內容時，把 `<selectedcontent>` 放在 `<select>` 內的 `<button>` 裡
- 被什麼擋：`<selectedcontent>` 沒有被 `<button>` 包住時，只會變成 picker 裡的一般內容（引用："the `<selectedcontent>` will just become part of the picker, like any other content element."）
- 戰報：部分改善——包進 `<button>` 後，觸發鈕會顯示選中項的內容；這個陷阱只出現在支援 base-select 的瀏覽器（Limited）（官方宣稱）

經過：想讓關起來的下拉選單顯示所選顏色的色塊，直接放了 `<selectedcontent>`，結果它跑進選項清單裡，觸發鈕還是只有文字。它必須在觸發鈕 `<button>` 裡才有作用。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Customizable <select>：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 2 條未拆：`base-select` 不再依最長選項決定寬度，需固定寬度以免版面位移；原生 `<select>` 只處理上下鍵，格狀 picker 裡左右鍵沒有作用，要用 `getBoundingClientRect()` 依實際位置補左右導覽，且上下鍵仍須能依序走完所有選項（picker 不能用 `role="grid"`）。
