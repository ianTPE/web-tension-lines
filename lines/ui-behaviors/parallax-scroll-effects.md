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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：外層 `overflow: clip` 並設 `view-timeline: --wrapper`，各層 `animation: parallax linear both; animation-timeline: --wrapper;`，用 `translateY(calc(100px * sibling-index()))` 錯開位移，或用 `animation-range: entry 25% exit calc(100% / sibling-count() * sibling-index())` 錯開範圍
- 被什麼擋：指南只說原生實作比 scroll 監聽或 IntersectionObserver 退路更有效率，沒說退路在哪個時刻出問題（引用："In browsers with built-in support for scroll-driven animations, ALWAYS use the native CSS implementation as those are more performant."）
- 戰報：部分改善——各層依捲動位置以不同速度移動，層數多也不必逐層寫值；捲動驅動動畫與 `sibling-index()` 皆為 Newly，裝飾性效果在舊瀏覽器直接不顯示（官方宣稱）

經過：視差以前是 scroll 事件裡逐層算位移。現在每層綁同一條視圖時間軸，速度差由自己的序號決定。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Newly（2026-10-27），Supported by: Chrome 115, Edge 115, Firefox 159, Safari 26；sibling-index()：本指南未給支援資料（見 mwg:dynamic-sibling-animations，Newly）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前多層視差要 scroll 監聽逐層計算 → 現在活動頁、產品故事頁、互動繪本可以任意加層，層數變了速度自動重新分配，純 CSS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:parallax-scroll-effects:2" %%
## 偵測捲動驅動動畫時要加 `(animation-range: entry)`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `@supports ((animation-timeline: view()) and (animation-range: entry))` 偵測
- 被什麼擋：只偵測 `animation-timeline` 會讓只有部分支援的瀏覽器通過（引用："The `(animation-range: entry)` check **MUST** be included here, to filter out browsers with only partial support."）
- 戰報：部分改善——部分支援的瀏覽器走退路，不會跑出殘缺的效果（官方宣稱）

經過：時間軸支援了、範圍卻不支援的瀏覽器，用單一條件偵測會被當成完全支援。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:parallax-scroll-effects:3" %%
## `animation-timeline`、`animation-range` 寫在 `animation` 簡寫之後
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：先寫 `animation` 簡寫，再寫 `animation-timeline` 與 `animation-range`
- 被什麼擋：簡寫寫在後面會把時間軸重設掉（引用："declare `animation-timeline` and `animation-range` *after* it to prevent the shorthand from resetting the timeline"）
- 戰報：部分改善——時間軸設定保得住（官方宣稱）

經過：和 mwg:scroll-progress-indicator:2 同一個坑。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:parallax-scroll-effects:4" %%
## JS 視差退路要自己檢查減少動態偏好
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：退路腳本先用 `matchMedia('(prefers-reduced-motion: reduce)')` 檢查，偏好減少動態時不執行
- 被什麼擋：CSS 的 `prefers-reduced-motion` 管不到腳本設的行內樣式，退路照樣讓各層移動（引用："The `prefers-reduced-motion` media query in the CSS doesn't affect the inline styles the script sets"）
- 戰報：部分改善——舊瀏覽器裡偏好減少動態的人也不會看到視差（官方宣稱）

經過：CSS 版乖乖關掉了，JS 版卻因為寫在行內樣式而繞過偏好設定。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：Scroll-driven animations：Newly（退路針對不支援的瀏覽器）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：不要用 `scroll-timeline-polyfill`（功能不完整、已知問題多）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
