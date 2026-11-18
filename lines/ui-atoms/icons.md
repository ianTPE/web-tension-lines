---
guide: icons
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/icons.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 使用與管理圖示

%% line-start id="mwg:icons" %%
## 把圖示當成 CSS 自訂屬性，由串接決定顯示哪一個
- 做法：每個圖示是一個存著圖像的自訂屬性（`--icon-trash`），元素設 `--icon-start`／`--icon-end` 就顯示；`@container style(--icon-start)` 偵測有值時在 `::before` 以 `mask` 加 `currentColor` 畫出；狀態切換只是覆寫屬性（`[aria-expanded="true"]` 換成另一個圖示）；大小、顏色、間距由可繼承的 `--icon-style-*` 從祖先統一調整
- 對手：用 `<img>` 加 CSS filter 替圖示改色，filter 無法可靠地套用任意 CSS 顏色值，改色麻煩又死板（引用："Filters can't reliably apply an arbitrary CSS color value to the image, so recoloring is cumbersome and inflexible."）
- 退路：保住主要行為——不支援 style query 時用 class 或元件選擇器掛上圖示
- 解鎖：圖示可做成參與串接的 CSS token，依選擇器或狀態自動切換

經過：圖示一直是「另一張圖」，要變色就得濾鏡或換檔，要換狀態就得藏一個露一個。把圖示變成屬性之後，它跟顏色、字級一樣走串接。
%% line-end %%

### 細節（不索引）
- 對手組：圖示樣式管不到
- 支援狀態：Container style queries：Newly available（2026-05-19），Supported by: Chrome 111, Edge 111, Firefox 151, Safari 18；Registered custom properties：Newly available（2024-07-09）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前圖示的顏色與狀態要靠濾鏡、換檔或切 class → 現在設計系統可以把整套圖示做成 token：外部連結自動帶外連圖示、展開鈕依 `aria-expanded` 換箭頭、工具列一處調整所有圖示的大小與顏色，HTML 不用改
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:icons:2" %%
## 圖示屬性要註冊成不繼承
- 做法：`@property --icon-start { syntax: "*"; inherits: false; }`（`--icon-end` 同理），在樣式查詢區塊內用 `--icon-start: inherit` 明確轉給偽元素；不支援 `@property` 時在查詢裡把子孫重設為 `initial`
- 對手：沒註冊成不繼承，按鈕上設的圖示會一路繼承，每個子孫都畫出一個圖示（引用："without it, an icon set on a button would inherit into every descendant, and each of them would render the icon too."）
- 退路：保住主要行為——不支援 `@property` 時在查詢中把子孫的圖示屬性重設為 `initial`
- 解鎖：（缺）

經過：自訂屬性預設會繼承，這對 token 是好事，對「這個元素要有圖示」卻是災難：按鈕裡的 span 也以為自己要畫一個。
%% line-end %%

### 細節（不索引）
- 對手組：繼承範圍不符預期
- 支援狀態：Registered custom properties：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：解鎖改為缺

%% line-start id="mwg:icons:3" %%
## 圖示 token 用根相對網址或 data URI
- 做法：圖示 token 的網址用根相對路徑（`url("/icons/trash.svg")`）或 data URI；非用相對網址不可時，以 `<url>` 開頭的語法註冊、在 `:root` 宣告實際網址；圖示多時用 `CSS.registerProperty` 批次註冊
- 對手：透過自訂屬性使用相對網址，可能相對於「使用」它的樣式表而非「定義」它的樣式表解析，兩者在不同目錄時指到錯的檔案；把網址放在註冊屬性的 `initial-value` 只在 Firefox 有效（引用："If those stylesheets are in different directories, the URL may resolve to the wrong file."）
- 退路：保住主要行為——改用根相對網址或 data URI，保留圖示 token 的正確解析
- 解鎖：（缺）

經過：同一個 token 在 A 目錄的樣式表定義、在 B 目錄的樣式表使用，瀏覽器可能拿 B 的路徑去找檔案，圖示就破了。
%% line-end %%

### 細節（不索引）
- 對手組：相對網址解析基準錯
- 支援狀態：Registered custom properties：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「相對網址解析基準錯」

%% line-start id="mwg:icons:4" %%
## 圖示偽元素加 `flex: none`，不讓長標籤把它擠掉
- 做法：畫圖示的 `::before`／`::after` 設 `flex: none`
- 對手：空的偽元素最小尺寸是 0，在 flex 按鈕裡標籤一長，圖示最先被壓縮，甚至縮到不見（引用："inside a flex button it is the first thing to shrink when the label is long, potentially to nothing."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：翻譯成德文之後按鈕標籤變長，垃圾桶圖示就悄悄消失了。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：flex：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:icons:5" %%
## 用 mask 畫的圖示要加 `forced-color-adjust: none`
- 做法：畫圖示的偽元素設 `forced-color-adjust: none`，填色用 `currentColor`
- 對手：強制色彩模式會取代 `background-color`，用 mask 畫的圖示整個消失（引用："In forced-colors mode the browser otherwise replaces `background-color`, making a masked icon disappear."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：mask 圖示的「顏色」其實是背景色，而強制色彩模式第一個拿掉的就是背景色。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：forced-color-adjust：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:icons:6" %%
## SVG 第一次內嵌，之後用 `<use href="#id">` 重複引用
- 做法：圖示第一次出現時內嵌 SVG，之後同頁用 `<use href="#id">` 引用；外部 sprite（`<use href="/icons.svg#id">`）只留給跨多頁共用、且同源的圖示；`viewBox` 放在 `<symbol>` 上；內嵌 sprite 的 symbol id 加命名空間
- 對手：`<use>` 的外部參照只限同源，跨來源的 sprite 會靜默失敗（引用："External references are same-origin only; cross-origin sprites fail silently."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：把圖示 sprite 放到 CDN 上似乎很合理，結果每個 `<use>` 都是空白，主控台也沒有錯誤。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：SVG `<use>`：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:icons:7" %%
## 在 symbol 裡預留自訂屬性，讓 `<use>` 的圖示可以從外面調
- 做法：自己掌控的 symbol 預留掛鉤：`fill="var(--icon-accent, currentColor)"`、`stroke-width="var(--icon-stroke, 2)"`，甚至對某條路徑用 CSS `d: var(--icon-path, path(…))`；不掌控來源的圖示就直接內嵌 SVG
- 對手：`<use>` 引用的內容被複製進 shadow tree，頁面 CSS 選不到裡面的元素（引用："With `<use>`, the referenced content is cloned into a shadow tree, so page CSS cannot select its elements."）
- 退路：保住主要行為——Safari 不能用 CSS `d` 改路徑，但填色與線寬等掛鉤照常可用
- 解鎖：symbol 可預留 CSS 變數掛鉤，讓 `<use>` 從外部改顏色、線寬或路徑

經過：`<use>` 很省，代價是頁面樣式碰不到裡面。只要圖示本身留好變數，從外面還是能調顏色、線寬，在大部分瀏覽器連形狀都能換。
%% line-end %%

### 細節（不索引）
- 對手組：圖示樣式管不到
- 支援狀態：css.properties.d：Limited availability。Supported by: Chrome 52, Edge 79, Firefox 97。Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前 `<use>` 的圖示只能改顏色 → 現在一個 symbol 可以靠 CSS 變數換線寬，甚至換路徑：播放／暫停、勾／叉共用同一個 `<use>`，狀態一變形狀就跟著換。改路徑目前 Safari 不支援
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 退路經交叉核對與仲裁更正為「保住主要行為」

%% line-start id="mwg:icons:8" %%
## 針對 Safari 的兩個渲染錯誤加補丁
- 做法：用只命中 Safari 的 `@supports` 對 `::before`／`::after` 套一個空的關鍵影格動畫，放進 `@layer`；在 Safari 把 `--icon-start` 改註冊為可繼承，並在樣式查詢裡把子孫重設為 `initial`
- 對手：WebKit 的錯誤可能讓圖示在使用者互動前都不出現；另一個錯誤讓 hover 時直接覆寫 `--icon-start` 不生效（引用："can prevent them from appearing until user interaction"）
- 退路：沒說——指南提供 Safari 錯誤補丁，未交代其他不支援情況
- 解鎖：（缺）

經過：同一套圖示在 Chrome 好好的，在 Safari 要點一下頁面才冒出來。這是瀏覽器的錯，但得由頁面來繞。
%% line-end %%

### 細節（不索引）
- 對手組：瀏覽器實作有缺陷
- 支援狀態：Container style queries、Registered custom properties：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 4 個糾錯提醒未拆：圖示對背景在明暗兩種配色下都要有 3:1 對比；`vertical-align: middle` 會讓圖示偏低，改用 `0.5cap` 置中；偽元素加 `pointer-events: none`；只有圖示的按鈕要用 `aria-label` 或 `--icon-style-alt` 給名稱
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「瀏覽器實作有缺陷」
