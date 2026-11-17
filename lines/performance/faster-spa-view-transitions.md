---
guide: faster-spa-view-transitions
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/faster-spa-view-transitions.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 以狀態快取加速 SPA 視圖切換

%% line-start id="mwg:faster-spa-view-transitions" %%
## 用 content-visibility: hidden 快取非作用中的視圖，切回來不必重算
- 做法：SPA 裡非作用中的視圖加 `content-visibility: hidden`（可搭 `position: absolute` 不佔版面），切換時移除；以 `@supports not (content-visibility: hidden)` 退回 `display: none`
- 對手：切換視圖時銷毀舊視圖或用 `display: none` 隱藏，使用者切回來時瀏覽器都得重建或重算整份排版與繪製（引用："Both approaches require the browser to recreate or recalculate the full layout and paint when the user returns to that view."）
- 退路：失去主要好處——退回 display:none，切回視圖仍須重算排版與繪製
- 解鎖：用 `content-visibility: hidden` 隱藏非作用中視圖並快取渲染狀態，切回時近乎瞬間顯示

經過：在幾個分頁間來回切，每次都從零排版。改成隱藏但保留快取，CPU 幾乎不花在看不到的視圖上，切回時直接沿用。代價是記憶體，見下一條。
%% line-end %%

### 細節（不索引）
- 對手組：工作花在看不到的地方
- 支援狀態：content-visibility：Newly available（2025-09-15）。Supported by: Chrome 108, Edge 108, Firefox 130, Safari 26
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：三到五個分頁的工具（編輯／預覽／設定、或多個儀表板頁）可以做到切換零等待，捲動位置和展開狀態都留著，不必引入框架的 keep-alive 機制
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:faster-spa-view-transitions:2" %%
## 快取每個視圖會吃光記憶體，動態路由要有淘汰策略
- 做法：只在視圖數量少而固定時全部快取；動態產生大量報表或路由的 app 實作 LRU 之類的淘汰策略，到記憶體門檻就銷毀舊視圖
- 對手：無條件快取每個視圖，最後造成嚴重的記憶體膨脹，低階裝置上可能讓瀏覽器當掉（引用："Doing so will eventually cause severe memory bloat and may crash the browser on low-end devices."）
- 退路：保住主要行為——不支援時退回 `display: none` 仍應依路由規模淘汰舊視圖，避免 DOM 累積
- 解鎖：（缺）

經過：`content-visibility: hidden` 留下所有 DOM、監聽器與狀態，每開一份報表就多一份。路由無上限時，用久了分頁就被撐爆。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：content-visibility：Newly available（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆（切換時對隱藏視圖加 `inert` 並把焦點移到新視圖；指南沒說不做時具體發生什麼）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
