---
guide: drag-and-drop
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/drag-and-drop.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 拖放重新排序

%% line-start id="mwg:drag-and-drop" %%
## 搬真的 DOM 節點，不用 CSS order 假裝重排
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：拖放結束時用 `container.moveBefore(item, ref)` 一次搬動既有節點，讓視覺、鍵盤、閱讀順序一致
- 被什麼擋：用 CSS `order` 或 `flex-direction: *-reverse` 改變畫面順序，DOM 順序沒變，Tab 鍵與螢幕閱讀器仍照舊順序走（引用："Reorder the real children in the DOM (not via CSS `order` or `flex-direction: *-reverse`) so visual, keyboard, and reading order stay aligned."）
- 戰報：部分改善——真的搬節點解決了順序脫鉤；但保留內部狀態要靠 `moveBefore()`，Safari 不支援，fallback `before()` 會讓項目內焦點等狀態流失（官方宣稱）

經過：拖放清單最省事的實作是改 `order`，畫面看起來對了，鍵盤使用者卻在舊順序裡跳。指南要求放開時才搬一次真節點，並用 `moveBefore()` 保住焦點與 iframe 狀態。複雜版面裡視覺與 DOM 順序真的無法對齊時，改用 `reading-flow`，但它只有 Chrome/Edge 支援。
%% line-end %%

### 細節（不索引）
- 對手組：視覺順序與DOM順序脫鉤
- 支援狀態：moveBefore()：Limited（Chrome 133、Edge 133、Firefox 144；Safari 不支援）；reading-flow：Limited（Chrome/Edge 137；Firefox、Safari 不支援）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：可以把正在播放的影片、iframe 小工具、輸入到一半的表單整塊搬到別的位置而狀態不重置。以前一搬就重新載入，所以「可重排的即時儀表板」做起來很痛
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:drag-and-drop:2" %%
## 拖曳途中只畫落點標記，放開才搬
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：拖曳中保持原項目在原位、用 `::before`/`::after` 畫落點標記，`pointerup` 時才移動
- 被什麼擋：拖曳時即時重排，兄弟項目跟著位移，畫面抖動（引用："Don't reorder while the pointer moves: shifting siblings feel jittery."）
- 戰報：勝——落點標記取代即時位移，抖動不再出現；用到的 pointer capture、fixed 定位都是成熟功能（官方宣稱）

經過：很多拖放實作在 `pointermove` 時就重排，每經過一個項目整列就跳一下。指南改成拖曳中只顯示一條落點線，放開時搬一次，並對每次移動補動畫讓項目「走過去」而不是跳過去。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：Pointer events：Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
