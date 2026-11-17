---
guide: parallax-scroll-effects
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/parallax-scroll-effects.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 捲動視差效果

%% line-start id="mwg:parallax-scroll-effects" %%
## 用 `view-timeline` 加 `sibling-index()` 做多層視差
- 做法：外層 `overflow: clip` 並設 `view-timeline: --wrapper`，各層 `animation: parallax linear both; animation-timeline: --wrapper;`，用 `translateY(calc(100px * sibling-index()))` 錯開位移，或用 `animation-range: entry 25% exit calc(100% / sibling-count() * sibling-index())` 錯開範圍
- 對手：指南只說原生實作比 scroll 監聽或 IntersectionObserver 退路更有效率，沒說退路在哪個時刻出問題（引用："In browsers with built-in support for scroll-driven animations, ALWAYS use the native CSS implementation as those are more performant."）
- 退路：保住主要行為——偵測不支援時用 IntersectionObserver 與 scroll 事件補上位移，純裝飾亦可漸進增強
- 解鎖：純 CSS 用 view-timeline 搭配 sibling-index() 做出多層捲動視差，不必依賴效能較差的捲動監聽器

經過：視差以前是 scroll 事件裡逐層算位移。現在每層綁同一條視圖時間軸，速度差由自己的序號決定。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Newly（2026-10-27），Supported by: Chrome 115, Edge 115, Firefox 159, Safari 26；sibling-index()：本指南未給支援資料（見 mwg:dynamic-sibling-animations，Newly）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前多層視差要 scroll 監聽逐層計算 → 現在活動頁、產品故事頁、互動繪本可以任意加層，層數變了速度自動重新分配，純 CSS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:parallax-scroll-effects:2" %%
## 偵測捲動驅動動畫時要加 `(animation-range: entry)`
- 做法：用 `@supports ((animation-timeline: view()) and (animation-range: entry))` 偵測
- 對手：只偵測 `animation-timeline` 會讓只有部分支援的瀏覽器通過（引用："The `(animation-range: entry)` check **MUST** be included here, to filter out browsers with only partial support."）
- 退路：保住主要行為——加上 animation-range 條件排除半套支援瀏覽器，安全轉入 JS 視差退路或靜態呈現
- 解鎖：（缺）

經過：時間軸支援了、範圍卻不支援的瀏覽器，用單一條件偵測會被當成完全支援。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：Scroll-driven animations：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:parallax-scroll-effects:3" %%
## `animation-timeline`、`animation-range` 寫在 `animation` 簡寫之後
- 做法：先寫 `animation` 簡寫，再寫 `animation-timeline` 與 `animation-range`
- 對手：簡寫寫在後面會把時間軸重設掉（引用："declare `animation-timeline` and `animation-range` *after* it to prevent the shorthand from resetting the timeline"）
- 退路：保住主要行為——寫在簡寫之後避免時間軸被重設，不支援瀏覽器則交由 `@supports` 退路或 JS 補上
- 解鎖：（缺）

經過：和 mwg:scroll-progress-indicator:2 同一個坑。
%% line-end %%

### 細節（不索引）
- 對手組：簡寫或屬性連動重設
- 支援狀態：Scroll-driven animations：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:parallax-scroll-effects:4" %%
## JS 視差退路要自己檢查減少動態偏好
- 做法：退路腳本先用 `matchMedia('(prefers-reduced-motion: reduce)')` 檢查，偏好減少動態時不執行
- 對手：CSS 的 `prefers-reduced-motion` 管不到腳本設的行內樣式，退路照樣讓各層移動（引用："The `prefers-reduced-motion` media query in the CSS doesn't affect the inline styles the script sets"）
- 退路：保住主要行為——退路腳本先檢查減少動態偏好才設樣式，舊瀏覽器也能尊重無障礙設定且視差正常
- 解鎖：（缺）

經過：CSS 版乖乖關掉了，JS 版卻因為寫在行內樣式而繞過偏好設定。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：Scroll-driven animations：Newly（退路針對不支援的瀏覽器）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：不要用 `scroll-timeline-polyfill`（功能不完整、已知問題多）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
