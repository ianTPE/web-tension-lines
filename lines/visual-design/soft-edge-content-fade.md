---
guide: soft-edge-content-fade
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/soft-edge-content-fade.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

> 上游已刪除（2026-11-25，v1.0.2）。同一版新增的 `teaser` 接手「內容結尾淡出」，捲動提示見 `scrollability-affordance-hints`。

# 內容邊緣柔和淡出

%% line-start id="mwg:soft-edge-content-fade" %%
## 用 `mask-image` 漸層讓內容本身淡出，不再蓋一層半透明疊層
- 做法：在可捲動容器或要截斷的文字區塊上設 `mask-image: linear-gradient(to bottom, black 80%, transparent 100%)`，同時寫 `-webkit-mask-image`；上下都要淡出時用一條多停點漸層
- 對手：用半透明疊層假造淡出時，要先知道背景色，而且疊層會擋住文字選取與點擊（引用："it requires knowing the background color and may interfere with text selection unless `pointer-events: none` is used."）
- 退路：不需要——遮罩功能已 Widely，不必另設退路
- 解鎖：（缺）

經過：捲動清單底部想用一道漸層暗示「下面還有」，疊一層白色漸層在深色主題下立刻露餡，壓在最後幾行字上也選不起來。改成遮罩後，淡出的是字本身，換什麼背景都對。
%% line-end %%

### 細節（不索引）
- 對手組：手工重現瀏覽器渲染
- 支援狀態：Masks：Baseline Widely available（2023-12-07 起）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-25（v1.0.2）上游已刪除
