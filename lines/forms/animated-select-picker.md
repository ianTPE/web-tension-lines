---
guide: animated-select-picker
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/animated-select-picker.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 有動畫的下拉選單

%% line-start id="mwg:animated-select-picker" %%
## 用 appearance: base-select 加 @starting-style 讓原生下拉選單有開合動畫
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<select>` 與 `::picker(select)` 設 `appearance: base-select`，對 picker 的 `opacity`、`height`、`display`、`overlay` 做過渡，配 `transition-behavior: allow-discrete` 與 `@starting-style`；箭頭用 `:open::picker-icon` 旋轉
- 被什麼擋：原生下拉選單的介面畫在頁面可控範圍之外，以前根本無法做動畫（引用："Previously, animating native select dropdowns was impossible because their UI was rendered outside the accessible viewport constraints."）
- 戰報：部分改善——Customizable `<select>` 為 Limited（Chrome／Edge 135、Safari 27，Firefox 不支援）；不支援時退回作業系統的下拉選單，選擇功能照常、只是沒有動畫（官方宣稱）

經過：想讓選單從觸發鈕淡入、長高，原生 `<select>` 做不到，只能整個換成 JS 套件。`base-select` 讓 picker 變成頁面上的一般元素，進出 top layer 的動畫用純 CSS 寫。指南同時要求用 `prefers-reduced-motion` 關掉動畫。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Customizable <select>：Limited（Supported by: Chrome 135 (Apr 2025), Edge 135 (Apr 2025), and Safari 27 (Sep 2026). Unsupported in: Firefox.）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前原生下拉選單一按就瞬間彈出，要動畫就得放棄原生元件 → 主題切換、語言選單這類小下拉可以保留原生 `<select>` 的表單行為，同時有和設計系統一致的展開動畫與旋轉箭頭。Firefox 退回系統選單
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:animated-select-picker:2" %%
## allow-discrete 另寫一條 transition-behavior，不塞進 transition 簡寫
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`transition` 簡寫只寫屬性與時間，另外寫一條 `transition-behavior: allow-discrete`
- 被什麼擋：把 `allow-discrete` 寫進 `transition` 簡寫，舊瀏覽器會忽略整條 `transition` 宣告（引用："it will make older browsers ignore the entire `transition` declaration."）
- 戰報：部分改善——分開宣告後，不認得 `allow-discrete` 的瀏覽器只丟掉那一條，其他過渡照常；但整個動畫所依附的 customizable select 本身仍是 Limited（官方宣稱）

經過：為了讓 picker 在 `display: none` 之間也能過渡，加上 `allow-discrete` 是必要的，但順手寫進簡寫，舊瀏覽器就連 opacity 的過渡都不做了。拆成兩條，新語法壞掉時只壞自己那一條。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Customizable <select>：Limited；`transition-behavior` 本指南未給支援資料
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:animated-select-picker:3" %%
## 不要在 ::picker(select) 上設 overflow: hidden
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：picker 做高度動畫時保持可捲動，不在 `::picker(select)` 加 `overflow: hidden`
- 被什麼擋：放大檢視或視窗很矮時選項放不下，picker 若不能捲動，超出的選項就到不了（引用："The picker must stay scrollable so that options that don't fit in the available space, for example at high zoom or in a short viewport, can still be reached."）
- 戰報：部分改善——保持可捲動，所有選項都選得到；這個陷阱只出現在支援 base-select 的瀏覽器（Limited）（官方宣稱）

經過：做 `height: 0 → auto` 的展開動畫，很自然會想加 `overflow: hidden` 讓內容不外露，結果放大到 200% 的使用者看不到、也捲不到後半的選項。picker 要維持能捲動。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Customizable <select>：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 2 條未拆：動畫要包在 `prefers-reduced-motion` 裡（動暈）；`base-select` 不再依最長選項決定寬度，需要固定寬度以免版面位移。「不要自行鎖捲動」一條沒有說明可觀察的後果，不另拆。
