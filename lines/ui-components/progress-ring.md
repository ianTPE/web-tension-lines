---
guide: progress-ring
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/progress-ring.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 環形進度

%% line-start id="mwg:progress-ring" %%
## 用 `<progress>` 加 `conic-gradient()` 與 `attr()` 畫環形進度，不用 SVG 加 ARIA
- 做法：`<progress value max aria-label>` 本身就是圓環：`--value: attr(value type(<number>))` 讀屬性、`conic-gradient()` 畫填色、`background-clip: border-area` 配透明邊框挖空中心；隱藏原生進度條偽元素，中心數字另放一層
- 對手：缺——指南只說優於只用 SVG 的做法，因為用的是語意元素而非 ARIA、也更容易融入版面與設計系統，沒說 SVG 做法在哪個時刻出錯
- 退路：保住主要行為——不支援時用 mask 與 MutationObserver 補上圓環及數值同步
- 解鎖：原生 `<progress>` 可直接畫成圓環，CSS 也能讀取 `value` 屬性

經過：儀表板的卡片要放圓形進度。以前畫 SVG 圓弧、再手動維護 `aria-valuenow`；現在進度條還是那個 `<progress>`，只是長成圓的。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：background-clip: border-area：Limited availability，Supported by: Chrome 150, Edge 150, Safari 18.2；Unsupported in: Firefox。attr()：Limited availability，Supported by: Chrome 133, Edge 133, Firefox 155；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前圓形進度得自己畫 SVG 又要同步 ARIA → 現在儀表板的配額圓環、課程完成度、檔案上傳的小圓圈都是一行 HTML，數值寫在屬性上 CSS 自己讀。目前 Firefox 缺 border-area、Safari 缺 typed attr()，要 mask 與 MutationObserver 補
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress-ring:2" %%
## 強制色彩模式下用 `forced-color-adjust: none` 加系統色重畫圓環
- 做法：`@media (forced-colors: active)` 裡設 `forced-color-adjust: none`，填色改 `CanvasText`、軌道改 `Canvas`
- 對手：強制色彩模式會移除背景漸層，圓環整個消失（引用："Forced colors mode removes background gradients, so in `@media (forced-colors: active)`, opt the ring out with `forced-color-adjust: none` and draw it with system colors, or the ring disappears."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：Windows 高對比模式下，儀表板上的進度圓環全部不見，只剩中間的百分比。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress-ring:3" %%
## 中心數字對輔助技術隱藏，改用 `aria-valuetext` 提供同樣的文字
- 做法：中心內容加 `aria-hidden="true"`；若中心顯示的是「3 / 5 個檔案」這類格式，每次更新時把同樣文字寫進 `<progress>` 的 `aria-valuetext`
- 對手：`<progress>` 已經暴露數值，中心文字不藏起來會被唸兩次；反之若只藏不補，讀屏只拿到數字（引用："The `<progress>` element already exposes its value, so screen readers would otherwise announce it twice."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：讀屏唸「75%，進度列 75」；中心改成「3 / 5 個檔案」後，讀屏卻只唸「60」。
%% line-end %%

### 細節（不索引）
- 對手組：重複內容干擾輔助技術
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress-ring:4" %%
## 用 `@property` 註冊 `--value` 讓圓環平滑轉動，預設 0 秒、沒有減少動態偏好才加長
- 做法：`@property --value { syntax: '<number>'; ... }`，`transition: --value 0s`，在 `prefers-reduced-motion: no-preference` 下改成 0.4s
- 對手：沒有註冊時圓環直接跳到新值，沒有過渡（引用："If `@property` is not supported, the ring will jump to the new value instantly instead of transitioning smoothly."）
- 退路：保住主要行為——不支援 `@property` 時直接跳到新值，失去平滑過渡
- 解鎖：註冊數值型自訂屬性後，進度值變更可平滑過渡

經過：進度從 40% 更新到 75%，圓弧一下子跳過去，看不出是增加了。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Registered custom properties：Baseline Newly available（2024-07-09 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：`<progress>` 內的替代文字不會被輔助技術使用
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
