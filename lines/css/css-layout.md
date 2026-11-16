---
guide: css-layout
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/css-layout.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# CSS 版面與響應式設計

%% line-start id="mwg:css-layout" %%
## 替換元素的縫隙用 display: block 消掉，不用 overflow: hidden 遮
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：對 `<img>`、`<canvas>`、`<svg>`、`<video>`、`<iframe>` 改用區塊外部顯示值（`display: block`／`grid`／`flex`），從源頭移除縫隙
- 被什麼擋：這些替換元素預設是 `display: inline`，在某些版面會多出一條縫（引用："certain replaced elements like `<canvas>`, `<img>`, `<svg>`, `<video>`, `<iframe>` use `display: inline` by default, which can add a gap in certain layouts."）
- 戰報：勝——改成區塊顯示，縫隙直接消失，不必再靠裁切掩蓋（官方宣稱）

經過：圖片底下莫名多幾 px，常見的「修法」是在父層加 `overflow: hidden` 把它切掉，但這只是把版面問題藏起來。指南的原則是不用 `overflow: hidden` 掩飾版面問題，要從源頭修。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：—（display 指南未給支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:css-layout:2" %%
## 用 aspect-ratio 先替媒體留位置
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：媒體元素設 `aspect-ratio`（例如 `16 / 9`），搭配 `inline-size: 100%; block-size: auto`
- 被什麼擋：圖片、影片載入前沒有預留空間，載入後把下方內容往下推，造成版面位移（引用："Use `aspect-ratio` to reserve space for media and prevent layout shift before assets load."）
- 戰報：勝——比例先決定高度，資源載入前後版面不動（官方宣稱）

經過：讀到一半文字突然往下跳，是因為上方圖片剛載入完成。先宣告比例，瀏覽器在圖片抵達前就知道要留多高。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：—（aspect-ratio 指南未給支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:css-layout:3" %%
## 可能放不下的 flex 列要開 flex-wrap: wrap
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只要有溢出的可能，flex 容器就設 `flex-wrap: wrap`；含長網址、程式碼的項目另設 `min-inline-size: 0`
- 被什麼擋：`nowrap` 又沒有 `overflow: auto/hidden`，窄視窗下項目會溢出容器（引用："`nowrap` without `overflow: auto/hidden` will spill on narrow viewports."）
- 戰報：勝——換行後項目留在容器內（官方宣稱）

經過：桌面寬度下看起來好好的一列按鈕，到手機上就衝出畫面。指南另外建議在 `wrap` 後面疊一行 `flex-wrap: balance` 讓各列平均、避免最後一列只剩一個孤兒項目，但那是 Limited 的新功能，不在這條線的範圍。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：—（flex-wrap: wrap 指南未給支援資料；同節的 flex-wrap: balance 為 Limited，Chrome 150、Edge 150）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有十餘條未拆（清單式指南），例如：`flex-wrap: balance` 防止最後一列孤兒項目（Limited）、`order`／`*-reverse`／`grid-auto-flow: dense` 讓 Tab 順序和畫面不符、`100vw` 忽略捲軸寬造成水平溢出、`container-type: size` 沒給高度時子元素塌陷、`overflow: hidden` 建立可被程式捲動的容器、grid lanes（masonry）尚無瀏覽器支援。
