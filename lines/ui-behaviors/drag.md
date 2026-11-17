---
guide: drag
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/drag.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 製作可拖曳元素

%% line-start id="mwg:drag" %%
## 記住抓取偏移並夾在視窗內，拖曳時元素不跳、不跑丟
- 做法：浮動面板用 `position: fixed`；只接受主按鍵，在 `pointerdown` 記下指標相對元素的偏移，`setPointerCapture()` 讓指標離開把手後仍持續拖曳；指標與方向鍵移動都經過同一個夾限函式，視窗或元素尺寸變了再夾一次
- 對手：沒記偏移時，從角落以外的地方抓起元素會跳一下；沒有夾限時元素可能被拖到看不到、拿不回來（引用："so the element does not jump when grabbed away from its corner … so the element stays reachable"）
- 退路：不需要——指針與座標夾限皆屬既有能力，若無 JS 則讓元件留在預設位置照常顯示與操作
- 解鎖：（缺）

經過：拖曳的第一個瑕疵通常是「一抓就跳」，第二個是「拖出畫面就救不回來」。偏移和夾限都在同一個函式處理，鍵盤路徑也共用。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：Pointer events／pointer capture：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:drag:2" %%
## 拖曳樣式只套在把手上，不套整個元素
- 做法：`cursor: grab`、`touch-action: none`、`-webkit-user-select: none` 與 `user-select: none` 只放在專用的拖曳把手上，把手用可聚焦、名稱有提到方向鍵的 `<button>`
- 對手：套在整個可拖曳元素上時，裡面的文字不能選、觸控手勢失去平常的行為；Safari 不認無前綴的 `user-select`（引用："so text outside it remains selectable and touch gestures retain their usual behavior"）
- 退路：保住主要行為——加上 -webkit-user-select: none 前綴後，Safari 也能在拖曳時正常抑制選到文字
- 解鎖：（缺）

經過：為了拖曳順手把整個面板設成不可選取、不可觸控捲動，面板裡的筆記和連結就跟著失效。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：user-select：Limited availability，Supported by: Chrome 54, Edge 79, Firefox 69；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 4 個糾錯提醒未拆：把手要是專用按鈕而非把標頭寫成可拖；提供不需拖曳的單指操作替代（移到某欄、停靠選單）；用 live region 播報描述性位置而非座標；沒有 JS 時不顯示無作用的把手
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
