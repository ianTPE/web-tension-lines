---
guide: spinner
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/spinner.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 載入轉圈

%% line-start id="mwg:spinner" %%
## 用沒有 `value` 的 `<progress>` 做轉圈，`@property` 決定要不要加伸縮弧線
- 做法：`<progress aria-label="Loading">` 不設 `value` 即為不確定狀態；`conic-gradient()` 畫拖尾、`background-clip: border-area` 挖成圓環、`rotate` 旋轉；以 `@property` 註冊 `--arc-start`／`--arc-end`，並讓 `--progress-dash-animation` 的 `initial-value` 帶入伸縮動畫，不支援 `@property` 時自動只剩旋轉
- 對手：缺——指南只說原生 `<progress>` 確保讀屏正確播報，沒說自製轉圈在哪個時刻出錯
- 退路：保住主要行為——不支援時用 mask 挖空圓環並只旋轉，失去伸縮弧線
- 解鎖：無 `value` 的 `<progress>` 可同時提供不確定進度語義與自訂轉圈外觀

經過：常見的轉圈是一個空 `<div>` 加動畫，讀屏什麼也不知道。換成 `<progress>` 之後，同一個元素既是畫面上的圈，也是讀屏聽到的「載入中」。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：background-clip: border-area：Limited availability，Supported by: Chrome 150, Edge 150, Safari 18.2；Unsupported in: Firefox。Registered custom properties：Newly（2024-07-09 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「支援就多一層動畫、不支援就簡化」要靠 JS 偵測 → 現在用 `@property` 的 `initial-value` 當開關，任何裝飾動畫都能在 CSS 裡自動分級；按鈕內的小轉圈、整頁載入圈都直接是可播報的進度元素
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:spinner:2" %%
## 強制色彩模式下用 `forced-color-adjust: none` 加系統色重畫轉圈
- 做法：`@media (forced-colors: active)` 裡設 `forced-color-adjust: none`，`--spinner-color: CanvasText`、`--track-color: Canvas`
- 對手：強制色彩模式移除背景漸層，轉圈整個消失（引用："Forced colors mode removes background gradients, so in `@media (forced-colors: active)`, opt the spinner out with `forced-color-adjust: none` and draw it with system colors, or the spinner disappears."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：高對比模式的使用者按下送出，畫面什麼都沒變，不知道系統正在處理。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:spinner:3" %%
## 減少動態時把轉圈放慢、拿掉伸縮，不要完全停住
- 做法：`prefers-reduced-motion: reduce` 下，在同一個選擇器裡把內部的 `--_used-spinner-duration` 設成 6s、清空 `--progress-dash-animation`、固定 `--arc-end`
- 對手：完全停止動畫後，使用者看不出處理還在進行（引用："Slow down the animation significantly rather than stopping it entirely, so the user still knows that the process is active."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：開了減少動態後轉圈變成一個靜止的圓弧，使用者以為頁面當掉了。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
