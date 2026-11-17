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
- 做法：`<select>` 與 `::picker(select)` 設 `appearance: base-select`，在 `select:open::picker(select)` 上用 `display: grid` 排欄，`<option>` 裡放圖片或 SVG 做成卡片，用 `option:checked` 與 `::checkmark` 標示選中項
- 對手：（缺）只說可以擺脫傳統的直向清單、不必寫自訂 JS，沒說直向清單或自訂 JS 在哪個時刻出錯（引用："break away from the traditional stacked vertical list and create a rich visual experience without custom JS."）
- 退路：保住主要行為——退回作業系統的下拉選單，選單功能與表單送出照常，只是選項只能直向排列
- 解鎖：以前原生下拉只能排成直向清單，要格狀或圖像化就得自己寫元件；現在 picker 能用 grid 排成卡片、行為仍是原生的

經過：色票、emoji、商品款式這類選項，排成格子比一長串文字好挑，以往只能放棄 `<select>` 自己做。現在 picker 可以用 grid 排版，表單送出與值仍是原生的。但原生 select 只認上下鍵，格狀排列需要另外處理鍵盤方向。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Customizable <select>：Limited（Supported by: Chrome 135 (Apr 2025), Edge 135 (Apr 2025), and Safari 27 (Sep 2026). Unsupported in: Firefox.）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前選項只能是一列文字，要圖像化就得自己寫元件 → 顏色、尺寸、貼圖、方案比較這類選擇可以做成格狀卡片的原生 `<select>`，直接參與表單送出。Firefox 退回純文字選單；左右鍵導覽與讀屏的格狀語意仍有限制
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-select-picker-layouts:2" %%
## picker 的版面樣式只掛在 :open 上
- 做法：`display: grid` 等版面樣式寫在 `select:open::picker(select)`，不直接寫在 `select::picker(select)`
- 對手：直接對 `select::picker(select)` 設 `display`，選單關著時 picker 也會顯示出來（引用："If you style `select::picker(select)`, it will make the picker visible even when the select is closed!"）
- 退路：保住主要行為——不支援時退回系統選單，本來就沒有選單版面可套
- 解鎖：（缺）

經過：照一般元素的直覺寫 `::picker(select) { display: grid }`，選單還沒打開，選項格就攤在畫面上。picker 的版面樣式要等選單打開才套。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Customizable <select>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-select-picker-layouts:3" %%
## <selectedcontent> 一定要包在 <button> 裡
- 做法：要在觸發鈕顯示選中項的豐富內容時，把 `<selectedcontent>` 放在 `<select>` 內的 `<button>` 裡
- 對手：`<selectedcontent>` 沒有被 `<button>` 包住時，只會變成 picker 裡的一般內容（引用："the `<selectedcontent>` will just become part of the picker, like any other content element."）
- 退路：保住主要行為——不支援時退回系統選單，觸發鈕照樣顯示選中的文字
- 解鎖：（缺）

經過：想讓關起來的下拉選單顯示所選顏色的色塊，直接放了 `<selectedcontent>`，結果它跑進選項清單裡，觸發鈕還是只有文字。它必須在觸發鈕 `<button>` 裡才有作用。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Customizable <select>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-select-picker-layouts:4" %%
## base-select 的觸發鈕要自行限制寬度
- 做法：開啟 `appearance: base-select` 後給 `<select>` 固定寬度，或用 flex／grid 約束尺寸
- 對手：`base-select` 移除依最長選項決定寬度的預設行為，選中內容改變時會造成版面位移（引用："Setting `appearance: base-select` removes the default browser behavior of sizing the select based on its longest option width. You may need to set a fixed width or use flex/grid constraints to prevent layout shifts."）
- 退路：保住主要行為——退回系統選單會照最長選項自動量寬度，不會有版面位移
- 解鎖：（缺）

經過：格狀卡片選單的選項寬度差異通常更大，不先限制觸發鈕，選一個長名稱就會推動整列表單。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：Customizable <select>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-select-picker-layouts:5" %%
## 格狀選單用實際幾何補左右鍵，上下鍵仍走完整清單
- 做法：攔截左右方向鍵，用 `getBoundingClientRect()` 找 pressed direction 最近的選項；保留上下鍵的線性導覽，不把 picker 改成 `role="grid"`
- 對手：原生 `<select>` 只處理上下鍵，格狀 picker 裡左右鍵沒有作用；若只補二維方向而拿掉線性順序，讀屏使用者可能走不完所有選項（引用："A native `<select>` only handles linear Up/Down arrow navigation, so Left/Right do nothing in the open picker and Up/Down still navigate items sequentially, regardless of rows and columns."）
- 退路：保住主要行為——退回系統選單時本來就是直向清單，上下鍵的線性導覽照常
- 解鎖：現在能攔截左右方向鍵、用實際幾何量測把焦點送到最近選項，格狀排列也有方向鍵導覽

經過：視覺上是兩欄色票，鍵盤左右卻完全沒反應。幾何量測比解析 `grid-template-columns` 字串可靠，也能處理 subgrid、RTL 與不規則排列。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Customizable <select>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
