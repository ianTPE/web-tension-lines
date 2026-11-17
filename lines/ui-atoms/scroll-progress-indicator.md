---
guide: scroll-progress-indicator
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/scroll-progress-indicator.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 捲動進度指示

%% line-start id="mwg:scroll-progress-indicator" %%
## 用 `scroll()` 時間軸做閱讀進度條
- 做法：一個固定在頂端的元素套 `scaleX(0)`→`scaleX(1)` 的關鍵影格，`animation-timeline: scroll()`（追蹤最近的祖先捲動容器，這裡是根）或在 `:root` 定義具名 `scroll-timeline`；包在 `prefers-reduced-motion: no-preference` 與 `@supports (animation-timeline: scroll())` 裡
- 對手：指南只說原生實作比 scroll 監聽器的退路更有效率，沒說舊做法在哪個時刻出問題（引用："In browsers with built-in support for scroll-driven animations, ALWAYS use the native CSS implementation as those are more performant."）
- 退路：失去主要好處——退回 scroll 監聽更新進度，保留指示器但失去原生效能優勢
- 解鎖：進度條動畫可直接由捲動位置驅動，不必手寫捲動計算

經過：進度條本質上就是「捲了幾成」，以前每次捲動都要重算一次。現在讓捲動位置本身驅動動畫。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Newly available（2026-10-27）。Supported by: Chrome 115, Edge 115, Firefox 159, Safari 26
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前閱讀進度條要掛 scroll 監聽 → 現在長文、教學、條款頁可以純 CSS 加進度條；一頁裡每個可捲動的區塊（程式碼、對話紀錄）也能各自帶自己的進度
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-progress-indicator:2" %%
## `animation-timeline` 要寫在 `animation` 簡寫之後
- 做法：先寫 `animation` 簡寫，再寫 `animation-timeline`
- 對手：簡寫寫在後面會把時間軸重設掉（引用："declare `animation-timeline` *after* it to prevent the shorthand from resetting the timeline."）
- 退路：保住主要行為——不支援時用 scroll 監聽更新進度，保留指示器
- 解鎖：（缺）

經過：同一組宣告換個順序，進度條就從「捲到哪長到哪」變成載入後自己長滿。
%% line-end %%

### 細節（不索引）
- 對手組：簡寫或屬性連動重設
- 支援狀態：同 mwg:scroll-progress-indicator，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：不要用 `scroll-timeline-polyfill`；含文字或圖的指示器加 `aria-hidden="true"`；尊重 `prefers-reduced-motion`、只動畫 `transform`／`opacity`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
