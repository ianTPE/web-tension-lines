---
guide: carousel-slide-effects
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/carousel-slide-effects.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 輪播投影片效果

%% line-start id="mwg:carousel-slide-effects" %%
## 用 `view()` 時間軸讓投影片隨捲動位置縮放、淡出
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每張投影片套一段 0%→50%→100% 的關鍵影格（例如 `scale` 0.5→1→0.5），`animation-timeline: view(inline)`（或具名的 `view-timeline`）讓動畫進度跟著投影片穿過捲動區的位置走；外層包 `prefers-reduced-motion: no-preference` 與 `@supports`，可搭配 scroll snap 停在正中
- 被什麼擋：指南只說原生實作比 scroll 監聽器加 Web Animations 的退路更有效率，而且退路不一定能重現每種效果，沒說舊做法在哪個時刻出問題（引用："In browsers with built-in support for scroll-driven animations, ALWAYS use the native CSS implementation as those are more performant."）
- 戰報：部分改善——一段連續動畫涵蓋進場、置中、離場，不寫 JS；scroll-driven animations 2026-10 才成為 Baseline，舊瀏覽器要用 scroll 監聽器逐張推進暫停中的動畫，或把效果當裝飾直接不給（官方宣稱）

經過：投影片滑到中間放大、往兩邊縮小變淡，以前得在每次捲動時量每張投影片的位置。現在把「位置」直接當成動畫的時間軸。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Newly available（2026-10-27）。Supported by: Chrome 115, Edge 115, Firefox 159, Safari 26
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前封面流這種「中間大、兩側小」的輪播要在 scroll 事件裡逐張計算 → 現在相簿、商品輪播、時間軸可以純 CSS 做出隨捲動連續變化的縮放與淡出
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:carousel-slide-effects:2" %%
## `animation-timeline` 要寫在 `animation` 簡寫之後
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：先寫 `animation` 簡寫，再寫 `animation-timeline` 與 `animation-range`
- 被什麼擋：簡寫寫在後面會把時間軸重設掉（引用："declare `animation-timeline` and `animation-range` *after* it to prevent the shorthand from resetting the timeline."）
- 戰報：部分改善——順序對了，時間軸與範圍不會被簡寫蓋回預設（官方宣稱）

經過：`animation` 簡寫會把它涵蓋的所有子屬性都重設一遍，`animation-timeline` 也在其中。寫反順序，動畫就退回按時間跑。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：同 mwg:carousel-slide-effects，記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:carousel-slide-effects:3" %%
## 沒有可聚焦內容的捲動容器要自己能取得焦點
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：投影片裡沒有可聚焦元素時，捲動容器加 `tabindex="0"` 與可及名稱；`<ul>` 本身有 list 角色可以直接命名，`<div>` 要加 `role="region"` 之類支援命名的角色
- 被什麼擋：不是每個瀏覽器都讓捲動容器可以用鍵盤聚焦，鍵盤使用者就捲不動投影片（引用："because not every browser makes a scroll container keyboard-focusable."）
- 戰報：勝——容器可聚焦又有名稱，鍵盤使用者能聚焦後用方向鍵捲動（官方宣稱）

經過：滑鼠和觸控都能拖，鍵盤卻連進都進不去。給容器一個 Tab 停點和名字就補上了。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：tabindex、role：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：`@supports` 要加 `(animation-range: entry)` 才能排除只部分支援的瀏覽器（指南沒說部分支援時會怎樣）；不要用 `scroll-timeline-polyfill`；要尊重 `prefers-reduced-motion`、只動畫 `transform`／`opacity`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
