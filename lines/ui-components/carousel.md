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
- 做法：循環時用 `--current` 與 CSS `order` 把首或尾一張「停」到旁邊，只改視覺順序，不複製也不搬動投影片；點標記跳頁時先把 `--current` 設回 `initial`，讓捲動照序列方向走
- 對手：複製投影片或在 DOM 裡搬動來做無限循環，和框架衝突，輔助技術也會讀到重複內容（引用："Do not clone slides or move them in the DOM, which conflicts with frameworks and duplicates content for assistive technology."）
- 退路：保住主要行為——不支援 `sibling-count()` 時由腳本設 `--children-count` 補上張數，照常循環
- 解鎖：用 CSS `order` 暫停首尾投影片即可循環，不必複製或搬動 DOM

經過：無限輪播最常見的做法是頭尾各複製一份，螢幕閱讀器因此讀到兩次同樣的投影片。指南改成只把一張投影片在視覺上停到另一端，DOM 順序仍是閱讀與焦點順序，沒有投影片被設成 inert 或 aria-hidden。另外，指南要求「暫時」不要用 `::scroll-button()`／`::scroll-marker`，但沒有說原因。
%% line-end %%

### 細節（不索引）
- 對手組：重複內容干擾輔助技術
- 支援狀態：Scroll snap：Widely（2020-01-15）；scrollend：Newly（2025-12-12）；sibling-count() and sibling-index()：Newly（2026-08-18）；Scroll-driven animations：Newly（2026-10-27）；overscroll-behavior：Limited（Chrome 144、Edge 144、Firefox 150；Safari 不支援，指南說是漸進增強、不需退路，未拆線）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：無限循環的輪播不用複製投影片：用 CSS order 暫停一張、捲動停下後再補償位移。內容只有一份，框架和讀屏都不會打架
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2；2026-11-18（v1.0.1）上游改為不支援 `sibling-count()` 時由腳本補張數、照常循環，退路由「失去主要好處」改為「保住主要行為」（戰報仍為部分改善）；停放的投影片不再設 `inert`
