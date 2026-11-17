---
guide: carousel
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/carousel.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 輪播（Carousel）

%% line-start id="mwg:carousel" %%
## 循環輪播不複製投影片，改用 order 暫停一張
- 做法：循環時用 `--current` 與 CSS `order` 把首或尾一張「停」到旁邊並設為 `inert`，不複製也不搬動投影片
- 對手：複製投影片或在 DOM 裡搬動來做無限循環，和框架衝突，輔助技術也會讀到重複內容（引用："Do not clone slides or move them in the DOM, which conflicts with frameworks and duplicates content for assistive technology."）
- 退路：失去主要好處——不支援 `sibling-index()` 時改為有限輪播，末端按鈕停用
- 解鎖：用 CSS `order` 暫停首尾投影片即可循環，不必複製或搬動 DOM

經過：無限輪播最常見的做法是頭尾各複製一份，螢幕閱讀器因此讀到兩次同樣的投影片。指南改成只把一張投影片在視覺上停到另一端並設 inert，Tab 順序與無障礙樹都和畫面一致。另外，指南要求「暫時」不要用 `::scroll-button()`／`::scroll-marker`，但沒有說原因。
%% line-end %%

### 細節（不索引）
- 對手組：重複內容干擾輔助技術
- 支援狀態：Scroll snap：Widely（2020-01-15）；scrollend：Newly（2025-12-12）；Scroll-driven animations：Newly（2026-10-27）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：無限循環的輪播不用複製投影片：用 CSS order 暫停一張、捲動停下後再補償位移。內容只有一份，框架和讀屏都不會打架
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
