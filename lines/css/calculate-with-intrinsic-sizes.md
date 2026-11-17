---
guide: calculate-with-intrinsic-sizes
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/calculate-with-intrinsic-sizes.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用固有尺寸做計算

%% line-start id="mwg:calculate-with-intrinsic-sizes" %%
## 用 calc-size() 在內容尺寸上加減、夾範圍，還能動畫
- 做法：用 `calc-size(<基準>, <算式>)` 對 `auto`／`min-content`／`fit-content` 做運算（例如 `calc-size(auto, size + 2rem)`、`calc-size(fit-content, min(size + …, …))`），前一行先寫一般關鍵字當 fallback
- 對手：瀏覽器預設無法在長度和固有尺寸關鍵字之間插值，例如 `0px` 到 `auto`（引用："By default, browsers cannot interpolate between a length (e.g., `0px`) and an intrinsic keyword (e.g., `auto`)."）
- 退路：失去主要好處——退回一般尺寸關鍵字或長度，失去固有尺寸運算與平滑過渡
- 解鎖：`calc-size()` 可對固有尺寸加減、設限制，並與固定長度互相過渡

經過：以前「內容寬度再多 2rem」或「內容高度但不超過某值」都只能靠 JS 量測。`calc-size()` 讓固有尺寸成為可運算、可插值的值。指南明確區分：只是 `0` 到 `auto` 的動畫用 `interpolate-size`，要做數學才用 `calc-size()`；也提醒算式裡的百分比是對容器、不是對 `size`。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：calc-size()：Limited（Chrome 129、Edge 129）；interpolate-size：Limited（Chrome 129、Edge 129）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：「跟內容一樣寬再留一點呼吸空間、但有上限」的標籤、按鈕、浮動面板可以純 CSS 寫出，展開時還會平滑長大。例如滑過時從圖示伸展成「圖示＋文字」的按鈕。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:calculate-with-intrinsic-sizes:2" %%
## 收合到 0 高度時一併設 visibility: hidden
- 做法：收合狀態設 `visibility: hidden`、展開狀態設 `visible`，並把 `visibility` 放進 transition，讓內容在收合動畫結束前保持可見
- 對手：只把 `block-size` 收到 0，內容只是視覺上消失，讀屏照唸，裡面的連結與控制項也還在 Tab 順序裡（引用："Collapsing to zero size (`block-size: 0` or `height: 0`) hides content only visually: screen readers still read it, and its links and controls stay in the tab order."）
- 退路：不需要——`visibility` 已 Widely，不必退路
- 解鎖：（缺）

經過：高度動畫做得很漂亮，鍵盤使用者卻會 Tab 進一個看不見的面板。把 `visibility` 一起過渡，就能同時保留收合動畫和正確的可及性狀態。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：—（visibility 指南未給支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

未拆：`prefers-reduced-motion` 一段只說大範圍尺寸動畫對前庭障礙者「disruptive」，沒有指到可觀察現象；fallback 段提到 JS 量測可能造成 layout thrashing，屬於退路建議，不另拆。
