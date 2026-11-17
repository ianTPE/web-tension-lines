---
guide: scrollytelling
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/scrollytelling.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 捲動敘事

%% line-start id="mwg:scrollytelling" %%
## 用具名 `view-timeline` 加 `timeline-scope`，讓一組段落驅動另一組元素的動畫
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在被追蹤的段落上設 `view-timeline: --tl-1 block` 等具名時間軸，在共同祖先（常用 `html`）設 `timeline-scope` 公開這些名稱，另一組被動畫的元素用 `animation-timeline: --tl-1` 綁上，再用 `animation-range` 精確指定區段
- 被什麼擋：指南沒說舊做法哪裡壞，只說可以不靠 JavaScript、動畫跟著捲動位置而不是時鐘走（引用："The animations are controlled by the scroll position, not a time-based clock, which ensures they are always in sync with the user's scroll."）
- 戰報：部分改善——純 CSS 讓文字段落驅動另一側的圖像進出場；Scroll-driven animations 為 Newly，退路是 IntersectionObserver 加多段門檻（官方宣稱）

經過：報導左邊是文字、右邊是隨段落變換的圖。文字段落當時間軸、圖當動畫，兩者不必是父子關係，靠 timeline-scope 牽在一起。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Baseline Newly available（2026-10-27 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前「讀到這段、旁邊的圖就換」要掛 scrollama 之類的函式庫 → 現在年度回顧、產品導覽、資料新聞可以讓每段文字驅動一個固定圖層的變化，捲回去自動倒帶
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scrollytelling:2" %%
## 偵測要加 `animation-range: 0% 100%`，濾掉部分支援
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：寫成 `@supports ((animation-timeline: scroll()) and (animation-range: 0% 100%))`
- 被什麼擋：只偵測 `animation-timeline` 會讓部分支援的瀏覽器通過（引用："The `(animation-range: 0% 100%)` check **MUST** be included here, to filter out browsers with only partial support."）
- 戰報：部分改善——部分支援的瀏覽器改走退路（官方宣稱）

經過：偵測說支援，但區段設定被忽略，圖在錯的段落才出現。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scrollytelling:3" %%
## `animation-timeline` 寫在 `animation` 簡寫之後
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：先寫 `animation` 簡寫，再寫 `animation-timeline` 與 `animation-range`
- 被什麼擋：簡寫會把時間軸重設掉（引用："declare `animation-timeline` and `animation-range` *after* it to prevent the shorthand from resetting the timeline."）
- 戰報：部分改善——順序正確時時間軸保留（官方宣稱）

經過：每個段落的動畫在載入時就自己播完了。
%% line-end %%

### 細節（不索引）
- 對手組：簡寫或屬性連動重設
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scrollytelling:4" %%
## 退路腳本沒跑、或使用者要求減少動態時，內容必須保持可見
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：退路的「先隱藏」樣式只掛在腳本加上的 `.scroll-fallback` 類別上；`prefers-reduced-motion: reduce` 時強制 `opacity: 1`、`transform: none`
- 被什麼擋：預設就把段落藏起來等動畫，腳本沒跑時內容永遠看不到（引用："The CSS only hides the sections once this class is set, so they stay visible if the script doesn't run"）
- 戰報：部分改善——腳本失敗或減少動態時，敘事內容照樣完整可讀（官方宣稱）

經過：腳本被擋或載入失敗，右側整欄空白，故事少了一半。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：不要用 `scroll-timeline-polyfill` 當退路
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
