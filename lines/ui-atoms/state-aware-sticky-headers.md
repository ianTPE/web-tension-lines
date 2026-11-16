---
guide: state-aware-sticky-headers
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/state-aware-sticky-headers.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 知道自己是否黏住的 sticky 標頭

%% line-start id="mwg:state-aware-sticky-headers" %%
## 用 `scroll-state(stuck: top)` 讓 sticky 標頭黏住時換樣式
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `position: sticky` 的元素本身（不是它的捲動祖先）設 `container-type: scroll-state` 與 `container-name`；`@container section-header scroll-state(stuck: top)` 裡改子元素的背景、文字色、陰影（容器無法用自己的查詢改自己）；可用 `stuck: block-start` 支援不同書寫方向
- 被什麼擋：傳統做法用 JS scroll 監聽器，指南只說「可能造成效能問題」，沒指出具體現象（引用："Traditional solutions required JavaScript scroll listeners, which can cause performance issues."）
- 戰報：僵持——僅 Chrome／Edge 144；不支援時標頭照樣黏住、只是不變樣式；若黏住後的樣式攸關可讀性，要用 IntersectionObserver 切 `.is-stuck` class 並複製一份樣式（官方宣稱）

經過：標頭黏住後疊在內容上，常需要加底色或陰影才讀得清楚。「現在黏住了沒」以前只能靠腳本推算，新查詢讓樣式直接知道。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Container scroll-state queries：Limited availability。Supported by: Chrome 144, Edge 144。Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前「黏住才變樣」要用監聽或 observer 切 class → 現在長文件的章節標頭、表格的分組標題可以黏住時自動加底色、陰影或縮成精簡版，讓人一眼看出現在在哪一節。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:state-aware-sticky-headers:2" %%
## 黏住時要改尺寸，就在父層關掉捲動錨定
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 sticky 元素的直接父層設 `overflow-anchor: none`（不要設在 `:root` 或 `body`）；貼在底部的元素不要在黏住狀態改盒模型
- 被什麼擋：黏住時改高度、padding、字級，下方流內內容的捲動錨定會補償位移，把元素推回非黏住狀態，來回振盪閃爍（引用："Scroll anchoring on the in-flow content below the sticky element adjusts the scroll offset to compensate for the layout change, which pushes the element back out of its stuck position and triggers an oscillation."）
- 戰報：部分改善——關掉父層的捲動錨定後，黏住狀態可以自由改盒模型與 transform；但對貼在底部的元素沒有效果（官方宣稱）

經過：標頭一黏住就縮小，縮小讓內容往上補，瀏覽器為了穩住畫面又往回捲，標頭就脫離黏住、變回原尺寸，然後再黏住。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：同 mwg:state-aware-sticky-headers，記 Limited（本指南未給 `overflow-anchor` 支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:state-aware-sticky-headers:3" %%
## 捲動區的 `scroll-padding-top` 要至少等於 sticky 標頭高度
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在捲動區（例如 `html`）設 `scroll-padding-top: var(--header-height)`，值等於或大於 sticky 元素的高度
- 被什麼擋：沒有預留時，取得焦點的控制項可能被 sticky 標頭完全蓋住，不符 WCAG 2.4.11（引用："This approach should ensure that when controls receive focus, they'll be consistently visible below the sticky content"）
- 戰報：勝——聚焦的控制項一律出現在 sticky 內容下方（官方宣稱）

經過：鍵盤使用者 Tab 到的位置，正好被黏住的標頭擋著。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：scroll-padding：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：巢狀容器查詢時一律命名，否則「unnamed containers will collide」（沒說具體後果）；若沒有變樣的黏住比不黏還糟，就把 `position: sticky` 也包進 `@supports`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
