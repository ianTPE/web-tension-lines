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
- 做法：`<select>` 與 `::picker(select)` 設 `appearance: base-select`，對 picker 的 `opacity`、`height`、`display`、`overlay` 做過渡，配 `transition-behavior: allow-discrete` 與 `@starting-style`；箭頭用 `:open::picker-icon` 旋轉
- 對手：原生下拉選單的介面畫在頁面可控範圍之外，以前根本無法做動畫（引用："Previously, animating native select dropdowns was impossible because their UI was rendered outside the accessible viewport constraints."）
- 退路：失去主要好處——退回標準作業系統下拉選單，仍無法自訂開合動畫
- 解鎖：以前原生下拉選單的介面畫在頁面外，根本沒辦法做動畫；現在 picker 像一般元素一樣可以過渡

經過：想讓選單從觸發鈕淡入、長高，原生 `<select>` 做不到，只能整個換成 JS 套件。`base-select` 讓 picker 變成頁面上的一般元素，進出 top layer 的動畫用純 CSS 寫。指南同時要求用 `prefers-reduced-motion` 關掉動畫。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Customizable <select>：Limited（Supported by: Chrome 135 (Apr 2025), Edge 135 (Apr 2025), and Safari 27 (Sep 2026). Unsupported in: Firefox.）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前原生下拉選單一按就瞬間彈出，要動畫就得放棄原生元件 → 主題切換、語言選單這類小下拉可以保留原生 `<select>` 的表單行為，同時有和設計系統一致的展開動畫與旋轉箭頭。Firefox 退回系統選單
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:animated-select-picker:2" %%
## allow-discrete 另寫一條 transition-behavior，不塞進 transition 簡寫
- 做法：`transition` 簡寫只寫屬性與時間，另外寫一條 `transition-behavior: allow-discrete`
- 對手：把 `allow-discrete` 寫進 `transition` 簡寫，舊瀏覽器會忽略整條 `transition` 宣告（引用："it will make older browsers ignore the entire `transition` declaration."）
- 退路：保住主要行為——舊瀏覽器只丟掉 `transition-behavior` 那條，過渡照常，只是少了離場動畫
- 解鎖：（缺）

經過：為了讓 picker 在 `display: none` 之間也能過渡，加上 `allow-discrete` 是必要的，但順手寫進簡寫，舊瀏覽器就連 opacity 的過渡都不做了。拆成兩條，新語法壞掉時只壞自己那一條。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Customizable <select>：Limited；`transition-behavior` 本指南未給支援資料
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:animated-select-picker:3" %%
## 不要在 ::picker(select) 上設 overflow: hidden
- 做法：picker 做高度動畫時保持可捲動，不在 `::picker(select)` 加 `overflow: hidden`
- 對手：放大檢視或視窗很矮時選項放不下，picker 若不能捲動，超出的選項就到不了（引用："The picker must stay scrollable so that options that don't fit in the available space, for example at high zoom or in a short viewport, can still be reached."）
- 退路：保住主要行為——不支援時退回系統選單，本來就可捲動，放大後的選項還是選得到
- 解鎖：（缺）

經過：做 `height: 0 → auto` 的展開動畫，很自然會想加 `overflow: hidden` 讓內容不外露，結果放大到 200% 的使用者看不到、也捲不到後半的選項。picker 要維持能捲動。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Customizable <select>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:animated-select-picker:4" %%
## 減少動態偏好下關掉選單與箭頭動畫
- 做法：在 `@media (prefers-reduced-motion: reduce)` 裡把 `::picker(select)` 與 `::picker-icon` 的 transition 關掉
- 對手：選單縮放、淡入與箭頭旋轉會讓有動暈症的使用者不適（引用："Always wrap animation constraints in a `prefers-reduced-motion` media query to ensure accessible environments for those affected by motion sickness."）
- 退路：保住主要行為——退回系統選單本來就沒有動畫，選擇功能照常
- 解鎖：（缺）

經過：裝飾動畫不是每個人都想要，系統已經表達減少動態，頁面就不該再播放。Firefox 本來就退回無動畫的系統選單。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：Customizable <select>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:animated-select-picker:5" %%
## base-select 的觸發鈕要自行限制寬度
- 做法：開啟 `appearance: base-select` 後給 `<select>` 固定寬度，或用 flex／grid 約束尺寸
- 對手：`base-select` 移除瀏覽器依最長選項決定寬度的預設行為，選中內容改變時會造成版面位移（引用："Setting `appearance: base-select` removes the default browser behavior of sizing the select based on its longest option width. You may need to set a fixed width or use flex/grid constraints to prevent layout shifts."）
- 退路：保住主要行為——退回系統選單會照最長選項自動量寬度，不會有版面位移
- 解鎖：（缺）

經過：原生選單會先量最長選項，自訂版不再代量。動畫再平滑，觸發鈕寬度跟著選項跳仍會破壞版面。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：Customizable <select>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

「不要自行鎖捲動」沒有指出可觀察的後果，不另拆。
