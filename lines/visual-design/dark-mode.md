---
guide: dark-mode
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/dark-mode.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 深色模式

%% line-start id="mwg:dark-mode" %%
## 在 `<head>` 放 `<meta name="color-scheme">`，減少深色使用者載入時的白閃
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<meta name="color-scheme" content="light dark">` 放在 `<head>`，讓瀏覽器在開始渲染前就知道支援哪些配色
- 被什麼擋：瀏覽器不知道頁面支援深色時，初始畫布是白的，載入時出現未上主題的閃光（引用："To help prevent a "flash of un-themed content" (FOUC), place a `<meta>` tag in your `<head>` to ensure the browser knows which themes you support before it even starts rendering."）
- 戰報：部分改善——初始畫布提早上色；指南也說不一定能在所有瀏覽器與載入條件下完全消除閃光（官方宣稱）

經過：深夜用深色模式點開網站，螢幕先白一下才變黑，刺眼。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：color-scheme：Baseline Widely available（2022-02-03 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode:2" %%
## `color-scheme` 設在 `:root`，不要只設在 `body`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`:root { color-scheme: light dark; }`
- 被什麼擋：瀏覽器看根元素決定整個視窗的主題；只設在 `body` 時，根捲軸與初始畫布背景可能仍是淺色（引用："If applied only to the `body`, these global UI surfaces may remain in light mode because the `body` does not control the window's rendering context."）
- 戰報：勝——視窗捲軸、畫布背景與表單控制項都跟著配色（官方宣稱）

經過：頁面內容都變深色了，右邊的主捲軸卻還是一條白色。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：color-scheme：Widely（2022-02-03 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode:3" %%
## 用 `light-dark()` 定義會自己切換的色彩 token
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：原始色值各放一個自訂屬性，再用 `--color-brand: light-dark(var(--color-brand-light), var(--color-brand-dark))` 組成 token；`accent-color`、`scrollbar-color`、`::selection` 等也能用 `light-dark()`
- 被什麼擋：缺——指南只說 `light-dark()` 省掉重複的媒體查詢，沒說用媒體查詢在哪個時刻出錯
- 戰報：部分改善——顏色依元素計算出的 `color-scheme` 自動選擇，包括子樹改了配色的地方；light-dark() 為 Newly，不支援時用 `prefers-color-scheme` 切換自訂屬性（官方宣稱）

經過：每個元件都要寫一段深色媒體查詢。把淺深兩個值寫進同一個 token 之後，元件只引用 token，配色交給 `color-scheme`。
%% line-end %%

### 細節（不索引）
- 對手組：樣式邏輯到處重複
- 支援狀態：light-dark()：Baseline Newly available（2024-05-13 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前深色模式要在每個元件重寫一份顏色 → 現在設計系統只維護一份「成對」token，嵌在淺色頁裡的深色程式碼區塊、地圖、播放器只要改 `color-scheme` 就整塊換色
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode:4" %%
## JS 讀 `prefers-color-scheme` 時一定要聽 `change` 事件
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：配色分支盡量放在 CSS；必須用 `matchMedia("(prefers-color-scheme: dark)")` 時，同時處理它的 `change` 事件
- 被什麼擋：系統配色隨時可能改變，只讀一次 `.matches` 的程式會停在舊配色（引用："MUST also handle its `change` event as the system preference can change at any time."）
- 戰報：勝——系統切換深淺色時頁面跟著更新（官方宣稱）

經過：傍晚系統自動切成深色，CSS 都換了，用 JS 畫的圖表卻還是淺色底。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode:5" %%
## 深淺色各用一張圖：`light-dark()` 直接接受圖片值
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`background-image: light-dark(url(hero-light.png), url(hero-dark.png))`；不支援時在 `:root` 定義 `--light-type`／`--dark-type`，用 `image-set()` 加 `type("image/do-not-use")` 讓非作用中的選項被丟棄
- 被什麼擋：沒有圖片值時，每張圖都要自己的媒體查詢分支，手動切換開關也得逐一翻轉（引用："every image needs its own media query branch, and a manual toggle must flip each one."）
- 戰報：部分改善——圖片和顏色一樣跟著 `color-scheme` 切換、子樹改配色也跟著換；light-dark() 圖片值為 Newly，`image-set()` 退路只下載被選中的那張，但不跟隨子樹的 `color-scheme`（官方宣稱）

經過：首頁大圖、插圖、圖示各有深淺兩版，每張都寫一段媒體查詢，加了手動切換後又得每張再改一次。
%% line-end %%

### 細節（不索引）
- 對手組：樣式邏輯到處重複
- 支援狀態：light-dark() image values：Baseline Newly available（2026-09-14 起），Supported by: Chrome 150, Edge 150, Firefox 150, Safari 27
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前深淺色插圖要逐張寫分支 → 現在插畫風格的網站、地圖底圖、產品截圖都能一行宣告兩版，元件放進深色區塊時圖片也自己換
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode:6" %%
## `image-set()` 開關的作用中選項要給空值，不要寫 `type("")`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：作用中的那一組自訂屬性設成空值（`--light-type: ;`），讓它成為沒有 `type()` 的普通選項；只有非作用中的設成不支援的 MIME 類型
- 被什麼擋：瀏覽器把空字串的 `type("")` 視為不支援，所有選項一起被丟掉（引用："Browsers treat the empty string as unsupported and drop every option."）
- 戰報：部分改善——退路正常選出一張圖；這個退路服務的是尚未支援 Newly 圖片值的瀏覽器（官方宣稱）

經過：為了「看起來比較清楚」把作用中的型別寫成 `type("")`，結果深色淺色兩張大圖都不見了。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：light-dark() image values：Newly（2026-09-14 起）；image-set() 本篇未給支援資料
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 6 個糾錯提醒未拆：Safari 的 `accent-color` 指示色不一定有足夠對比（同 `mwg:checkbox:2`）；`scrollbar-color` 不要過渡、macOS 要搭 `scrollbar-width`（同 `mwg:adapt-scrollbar-to-contrast-preferences:2`、`:3`）；Safari iframe 不依嵌入端配色（同 `mwg:component-specific-light-dark-theme:4`）；子樹改 `color-scheme` 後繼承的顏色屬性要重設（同 `mwg:component-specific-light-dark-theme:2`）；`light-dark()` 兩個值要同型別，顏色配圖片要用 `image()`（無瀏覽器支援，改用單色 `linear-gradient`）；不要為了換外觀重做原生控制項
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
