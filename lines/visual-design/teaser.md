---
guide: teaser
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/teaser.md
first_seen: 2026-11-25（v1.0.2）
license: CC-BY-4.0（上游指南）
---

# 內容試閱片段的淡出與模糊

%% line-start id="mwg:teaser" %%
## 用 `mask-image` 讓試閱片段的結尾淡出，不蓋半透明疊層
- 做法：在來源端就截斷的試閱區塊上設 `mask-image: linear-gradient(to top, transparent, black 3lh)`，不加 `-webkit-mask-image`；直書時把漸層方向改成區塊方向
- 對手：（缺）指南只說半透明疊層會限制背景與互動的設計，沒指出在哪個時刻出錯（引用："NOT a semi-transparent overlay which imposes design constraints on the background and interaction."）
- 退路：不需要——遮罩已 Widely，不必退路
- 解鎖：（缺）

經過：付費文章的前幾段要淡出到背景裡。指南要的是讓字自己變透明，而不是在上面疊一層接近背景色的漸層。這裡談的是來源端就截斷的內容，捲動容器的「下面還有」提示另有指南。
%% line-end %%

### 細節（不索引）
- 對手組：手工重現瀏覽器渲染
- 支援狀態：Masks：Widely（2023-12-07）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 缺
- 類型：糾錯
- 註：與已從上游刪除的 `mwg:soft-edge-content-fade` 同一主題；舊指南對疊層的具體說法（要知道背景色、擋文字選取）沒有搬過來
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:teaser:2" %%
## 淡出長度用 `lh` 算行數，不用百分比
- 做法：漸層停點寫成 `black 3lh` 這種以行為單位的長度
- 對手：百分比會跟著內容變長，摘錄一長，大半篇都變淡（引用："a percentage grows with the content, so a long excerpt would be mostly faded"）
- 退路：不需要——`lh` 單位已 Widely，不必退路
- 解鎖：（缺）

經過：同一條 `black 80%` 套在兩段的摘錄上剛好，換成二十段的長摘錄時，尾端好幾段都看不清楚。改用行高當單位，不論摘錄多長都只淡掉最後幾行。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：lh unit：Widely（2023-11-21）；Masks：Widely（2023-12-07）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:teaser:3" %%
## 淡出的那一段不要留連結或控制項
- 做法：淡出區裡不放連結與控制項；訂閱鈕這類行動呼籲放在加了遮罩的元素後面
- 對手：遮罩和模糊只改繪製，內容還在 DOM、無障礙樹、頁內搜尋與複製貼上裡，淡掉的連結看不清卻仍能聚焦（引用："DO NOT leave links or controls in the faded part: they stay focusable while they are unreadable."）
- 退路：不需要——遮罩已 Widely，不必退路
- 解鎖：（缺）

經過：鍵盤使用者一路 Tab，焦點落在一段幾乎透明的文字上，不知道自己停在哪個連結。遮罩擋不住讀取，所以真正要收費的內容得在來源端截斷，訂閱鈕也要放到遮罩外面才不會一起淡掉。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：Masks：Widely（2023-12-07）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:teaser:4" %%
## 付費牆的模糊用外層偽元素的 `backdrop-filter`，不寫在淡出的元素裡
- 做法：外層 `.teaser-blur` 設 `position: relative`，在它的 `::after` 設 `backdrop-filter: blur(0.1em)` 蓋住尾端幾行，並用 `mask-image: linear-gradient(to top, black 5lh, transparent)` 讓模糊漸進；淡出的遮罩留在內層 `.teaser`
- 對手：把 `backdrop-filter` 寫在加了遮罩的元素裡面，那個元素的文字不會變模糊（引用："A `backdrop-filter` inside a masked element does not blur that element's text."）
- 退路：保住主要行為——不支援 `backdrop-filter` 時文字不模糊，但仍會淡出
- 解鎖：試閱尾端可以漸進變模糊，讀者看得出還有文字但讀不到

經過：想讓付費文章的最後幾行又淡又糊，直覺是在同一個元素上加偽元素，結果字還是清楚的。把模糊層提到外層後才蓋得到，遮罩又讓模糊慢慢加重，看不出從哪一行開始。
%% line-end %%

### 細節（不索引）
- 對手組：新屬性的隱藏前提
- 支援狀態：backdrop-filter：Newly（2024-09-16），Supported by: Chrome 76, Edge 79, Firefox 103, Safari 18
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「看得到有字、看不清內容」的試閱多半要疊圖或另做模糊版 → 現在付費文章、課程講義、電子報存檔頁可以直接用真文字做漸進模糊的結尾，換背景、換主題都不必重做。模糊擋不住複製與讀屏，真正的內容仍要在伺服器端截斷
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:teaser:5" %%
## 模糊層要往左右與底部多伸出至少一個模糊半徑
- 做法：偽元素用負的 `inset-inline` 與 `inset-block-end` 往外伸 `--bleed`，取模糊半徑的兩倍（至少一倍）
- 對手：`backdrop-filter` 只畫在自己的元素範圍內，不外伸時模糊的字在文字邊緣被切成一條直線（引用："without this bleed the blurred text is cut off in a straight line at the edges of the text."）
- 退路：保住主要行為——不支援 `backdrop-filter` 時沒有模糊，也沒有切邊，文字照樣淡出
- 解鎖：（缺）

經過：模糊會把字往外暈開，但濾鏡只在方框裡畫，於是左右兩側像被刀切過。往外多留一點，暈開的部分才畫得完。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：backdrop-filter：Newly（2024-09-16）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:teaser:6" %%
## 淡出要比模糊早開始
- 做法：淡出範圍寫得比模糊長，例如淡出 9lh、模糊 5lh；但也不能長到模糊那段幾乎透明
- 對手：同樣的不透明度下模糊的字看起來比清晰的字重，兩者從同一點開始時，文字在模糊起點反而更搶眼，然後才淡掉（引用："If both start at the same point, the text gets more prominent where the blur begins, then fades."）
- 退路：保住主要行為——不支援 `backdrop-filter` 時沒有模糊，文字照樣淡出
- 解鎖：（缺）

經過：淡出和模糊設成同樣長度，畫面上卻在倒數第五行出現一道較黑的帶子。先讓字淡下來，再開始糊，重量才會一路遞減。
%% line-end %%

### 細節（不索引）
- 對手組：新屬性的隱藏前提
- 支援狀態：backdrop-filter：Newly（2024-09-16）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:teaser:7" %%
## 單層模糊的半徑要小，想越來越糊就疊 4～6 層
- 做法：單一模糊層只用很小的半徑（例如 `0.1em`）；要讓半徑往結尾遞增時，疊 4～6 個元素，各用更大的 `blur()`（例如 `1px`、`2px`、`4px`、`8px`）並以重疊的 `mask-image` 帶狀銜接
- 對手：遮罩是在清晰字與模糊字之間交叉淡化，半徑一大，清晰的字會像鬼影一樣透過模糊顯現（引用："a large radius shows a ghost of the sharp text through the blur."）
- 退路：保住主要行為——不支援 `backdrop-filter` 時沒有模糊，文字照樣淡出
- 解鎖：（缺）

經過：把模糊調到 8px 想藏得徹底一點，過渡區裡反而同時看到糊的字和清楚的字。疊層能避開，代價是每一步多一個元素與一次合成。
%% line-end %%

### 細節（不索引）
- 對手組：新屬性的隱藏前提
- 支援狀態：backdrop-filter：Newly（2024-09-16）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:teaser:8" %%
## 不用 SVG 濾鏡的 `backdrop-filter: url(…)` 省元素
- 做法：漸進模糊用多層 `backdrop-filter: blur()`，不為了少幾個元素改用 `backdrop-filter: url(…)` 引用 SVG 濾鏡
- 對手：Safari 與 Firefox 的 `backdrop-filter` 不套用 SVG 濾鏡，用 SVG 做的模糊在那裡完全沒有效果（引用："`backdrop-filter` does not apply SVG filter references (`url(…)`) in Safari and Firefox, so an SVG-based blur renders no blur at all there."）
- 退路：保住主要行為——不支援 `backdrop-filter` 時沒有模糊，文字照樣淡出
- 解鎖：（缺）

經過：一個 SVG 濾鏡就能畫出漸變模糊，在 Chrome 裡看起來很省事，換到 Safari 卻整段都是清楚的字。指南寧可多花幾個元素。
%% line-end %%

### 細節（不索引）
- 對手組：沒防護不支援的瀏覽器
- 支援狀態：backdrop-filter：Newly（2024-09-16）；SVG 濾鏡引用 `url(…)` 在 Safari、Firefox 不套用
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：由 CSS 截斷摘錄時用 `max-block-size` 加 `overflow: clip`，以免變成捲動容器（同 `mwg:css-layout:11`）；直書時只換漸層方向的變數，不整條重寫
- 變更紀錄：2026-11-25（v1.0.2）首次拆出
