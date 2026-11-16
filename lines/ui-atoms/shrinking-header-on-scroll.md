---
guide: shrinking-header-on-scroll
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/shrinking-header-on-scroll.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 捲動時縮小的標頭

%% line-start id="mwg:shrinking-header-on-scroll" %%
## 用 `scroll(block root)` 加 `animation-range` 讓標頭隨捲動縮小
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：固定在頂端的標頭套縮小高度的關鍵影格，`animation-timeline: scroll(block root)`，`animation-range: 0px 150px`（結束點等於起訖高度差，內容才會和標頭同步捲動）
- 被什麼擋：指南只說原生實作比 scroll 監聽器的退路更有效率，沒說舊做法在哪個時刻出問題（引用："In browsers with built-in support for scroll-driven animations, ALWAYS use the native CSS implementation as those are more performant."）
- 戰報：部分改善——標頭在前 150px 的捲動中平滑縮小，不寫 JS；Newly，舊瀏覽器要用 scroll 監聽器依捲動距離改高度（官方宣稱）

經過：大標頭佔掉手機螢幕三分之一，往下捲時希望它讓位。尺寸和捲動距離一一對應，交給 CSS 時間軸就好。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Newly available（2026-10-27）。Supported by: Chrome 115, Edge 115, Firefox 159, Safari 26
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前縮小標頭要在 scroll 事件裡逐格改高度 → 現在品牌大標頭、活動頁主視覺可以在往下捲的前幾百像素平滑縮成精簡導覽列，往回捲又長回來，純 CSS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:shrinking-header-on-scroll:2" %%
## 固定標頭不要蓋住內容與聚焦的控制項
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：標頭是 sticky 時，捲動區設 `scroll-padding-top` 等於標頭高度（可以用同一條捲動時間軸一起動畫）；`body` 或主內容加等於標頭初始高度的 `padding-top`
- 被什麼擋：取得焦點的元素被顯示在 sticky 標頭底下，不符 WCAG 2.4.11 Focus Not Obscured；標頭也可能蓋住緊接在後的內容（引用："set `scroll-padding-top` to ensure that when elements receive focus, they aren't displayed under the sticky content."）
- 戰報：勝——聚焦的控制項一律出現在標頭下方，開頭的內容也不被蓋住（官方宣稱）

經過：Tab 到下一個連結，瀏覽器把它捲進視野，卻剛好捲到標頭底下。告訴瀏覽器上方有多少空間被佔掉，它就會捲到對的位置。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：scroll-padding：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:shrinking-header-on-scroll:3" %%
## 用百分比範圍時，被縮小的元素不能在文件流裡
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`animation-range` 用百分比時，被動畫的元素不要是 `position: static` 或 `relative`（範例用 `position: fixed`），或改用像素範圍
- 被什麼擋：流內元素一邊縮小，總捲動距離也跟著縮，百分比換算出的位置隨之改變（引用："Shrinking those elements as you scroll, would shrink the total scroll distance, thereby affecting the computed value of — for example — `10%` into the scroll."）
- 戰報：部分改善——元素脫離文件流後，縮小不影響捲動距離，百分比範圍保持穩定（官方宣稱）

經過：動畫依「捲了百分之幾」推進，而動畫本身又在改變總長度，兩者互相牽動。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:shrinking-header-on-scroll:4" %%
## `animation-timeline` 與 `animation-range` 要寫在 `animation` 簡寫之後
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：先寫 `animation` 簡寫，再寫 `animation-timeline` 與 `animation-range`
- 被什麼擋：簡寫寫在後面會把時間軸重設掉（引用："declare `animation-timeline` and `animation-range` *after* it to prevent the shorthand from resetting the timeline."）
- 戰報：部分改善——時間軸與範圍不會被簡寫蓋回預設（官方宣稱）

經過：和其他捲動驅動動畫一樣，簡寫會重設時間軸，順序決定動畫跟著捲動還是跟著時間。
%% line-end %%

### 細節（不索引）
- 對手組：簡寫或屬性連動重設
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：`@supports` 要加 `(animation-range: 0% 100%)` 才能排除只部分支援的瀏覽器（指南沒說部分支援時會怎樣）；不要用 `scroll-timeline-polyfill`；尊重 `prefers-reduced-motion`、盡量只動畫 `transform`／`opacity`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
