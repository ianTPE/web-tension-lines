---
guide: size-aware-styling
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/size-aware-styling.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依可用空間調整樣式

%% line-start id="mwg:size-aware-styling" %%
## 用 container queries 讓元件看自己的空間，而不是整個螢幕
- 做法：在外層設 `container-type: inline-size`，元件用 `@container (min-width: 400px)` 切換並排版面、顯示或隱藏額外細節
- 對手：同一個卡片或導覽元件可能放進窄側欄或寬主欄，用視窗寬度的 media query 得事先知道元件會放在哪，替每種版面各寫一組（引用："You do not need to know where the component will live or write complex media queries to handle every possible layout."）
- 退路：不需要——尺寸容器查詢已 Widely，不必退路
- 解鎖：元件可依容器寬度切換版面，不必為各放置位置寫 media query

經過：卡片在主欄夠寬可以並排，同一張卡片搬進側欄就該堆疊，但視窗寬度並沒有變。改看容器寬度後，元件不用知道自己被放在哪。不支援的瀏覽器先給安全的堆疊版面，再用 media query 粗略增強。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Container queries (size)：Widely（2023-02-14）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
