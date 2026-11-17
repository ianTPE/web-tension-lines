---
guide: interactions-in-complex-layouts
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/interactions-in-complex-layouts.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 最佳化複雜版面中的互動

%% line-start id="mwg:interactions-in-complex-layouts" %%
## 用 content-visibility: auto 的 containment 把一欄的變動關在那一欄裡
- 做法：對看板的每一欄、大型資料格的各區塊這類自成一體的版面單位加 `content-visibility: auto` 與 `contain-intrinsic-size`；不支援時以 `@supports not` 退回 `contain: layout style paint`
- 對手：在複雜版面裡改動一個項目（拖一張卡、改一格），會引發連鎖的樣式與排版計算，迫使整頁重排，造成掉幀與高 INP（引用："performing a minor change to a single item—such as dragging a card or editing a cell—can trigger a chain reaction of style and layout calculations that forces the browser to reflow the entire page."）
- 退路：保住主要行為——不支援時以 `@supports` 退回 `contain: layout style paint`，仍能隔離整頁重排
- 解鎖：（缺）

經過：把卡片從一欄拖到另一欄，整個看板一起重排，拖曳一卡一卡的。每欄劃成 containment 邊界後，瀏覽器知道欄內的變動影響不到外面，只重排那一欄。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：content-visibility：Newly available（2025-09-15）。Supported by: Chrome 108, Edge 108, Firefox 130, Safari 26
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯（可見元素的好處全來自 containment，指南給的 fallback `contain` 就能達到類似效果，並非以前做不到）
- 另有 1 個糾錯提醒未拆（要配 `contain-intrinsic-size`，同 mwg:defer-rendering-heavy-content:2）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
