---
guide: scrollability-affordance-hints
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/scrollability-affordance-hints.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 可捲動提示

%% line-start id="mwg:scrollability-affordance-hints" %%
## 用 scroll-state 查詢與捲動驅動的遮罩提示「還有內容」
- 做法：陰影版：捲動容器設 `container-type: scroll-state`，用它自己的 `::before`／`::after` 以 sticky 貼在兩端，`@container scroll-state(scrollable: block-start／block-end)` 時顯示；淡出版：在容器上用 `mask` 挖出兩端的漸層帶，以 `animation-timeline: scroll(self inline)` 驅動帶寬。內容需要清楚到邊（長文、表格、表單）用陰影，橫向的一排項目或非單色背景用淡出
- 對手：指南只說兩種提示都不需要 scroll 監聽器，也不需要額外元素，沒說監聽器或額外元素在哪個時刻出問題（引用："Both need no scroll listeners and no extra elements in the markup."）
- 退路：保住主要行為——不支援時改用背景陰影或 IntersectionObserver，保留邊緣提示
- 解鎖：CSS 可在仍有內容的方向顯示陰影或淡出，到達邊界時自動消失

經過：「這裡還能往下捲」的提示，以前要監聽捲動或插哨兵元素去判斷。現在容器自己知道哪一端還有東西，偽元素直接問它。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Container scroll-state queries：Limited availability。Supported by: Chrome 144, Edge 144。Unsupported in: Firefox, Safari。Scroll-driven animations：Newly（2026-10-27）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「還能捲」的陰影要寫捲動監聽或哨兵 → 現在對話框內文、側欄清單、橫向標籤列可以純 CSS 在邊緣出現陰影或淡出、到底自動消失；捲軸被隱藏的設計也有替代線索
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scrollability-affordance-hints:2" %%
## 淡出遮罩只遮兩端，聚焦項目不要停在淡出帶裡
- 做法：遮罩寫成「整層不透明減去兩條漸層帶」，不用單一漸層；容器有捲動吸附或內含可聚焦項目時，`scroll-padding-inline`（或 `-block`）設成淡出寬度
- 對手：單一漸層遮罩裁到邊框盒，會連捲動容器的焦點外框一起遮掉；聚焦或吸附的項目也可能停在淡出帶裡（引用："including a focus outline on the scroller, which a single gradient clipped to the border box would hide."）
- 退路：保住主要行為——不支援時改用背景陰影或 IntersectionObserver，保留邊緣提示
- 解鎖：（缺）

經過：淡出效果做得漂亮，代價可能是鍵盤使用者看不到自己聚焦在哪：外框被遮罩吃掉，或聚焦的那顆標籤剛好半透明。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：Scroll-driven animations：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scrollability-affordance-hints:3" %%
## 淡出寬度的自訂屬性要先註冊才能平滑變化
- 做法：用 `@property` 把 `--fade-start`、`--fade-end` 註冊成 `<length>`、`inherits: false`、`initial-value: 0px`
- 對手：沒註冊的自訂屬性不會內插，淡出帶的寬度會直接跳（引用："Unregistered custom properties do not interpolate, so the fades would jump."）
- 退路：沒說——指南未交代不支援 `@property` 時怎麼處理淡出帶的寬度過渡
- 解鎖：（缺）

經過：關鍵影格裡改的是自訂屬性，瀏覽器不知道它是長度，就只能在 0 和 3rem 之間切換。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Scroll-driven animations：Newly（本指南未給 `@property` 支援資料）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「沒說」、解鎖改為缺

%% line-start id="mwg:scrollability-affordance-hints:4" %%
## 右到左內容要翻轉淡出的漸層方向
- 做法：在 `:dir(rtl)` 裡翻轉 `--fade-dir`，並交換兩條漸層帶的位置
- 對手：捲動時間軸跟著書寫方向，但漸層方向與遮罩位置是實體方向，右到左內容不翻轉就對不上（引用："The scroll timeline follows the writing direction, but gradient directions and mask positions are physical."）
- 退路：保住主要行為——不支援時改用背景陰影或 IntersectionObserver，保留邊緣提示
- 解鎖：（缺）

經過：動畫的起點會跟著語言方向調換，漸層卻不會。阿拉伯文介面裡，該淡出的那一端反而清楚，不該淡的那一端反而淡掉。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Scroll-driven animations：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：拿掉捲軸時，提示必須與相鄰顏色有 3:1 對比，且一定要有退路；IntersectionObserver 退路遇到比容器還大的單一子元素會永遠顯示兩端提示，要改觀察哨兵元素
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
