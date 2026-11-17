---
guide: light-dismiss-a-dialog
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/light-dismiss-a-dialog.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 點外面關閉對話框

%% line-start id="mwg:light-dismiss-a-dialog" %%
## 用 `closedby="any"` 讓模態對話框點背景就關
- 做法：`<dialog closedby="any">` 並以 `showModal()` 開啟；不支援時用退路腳本：只在 `event.target` 是 dialog 本身時，再比對點擊座標是否落在 dialog 的矩形外才 `close()`
- 對手：手寫點外面關閉時，點在 dialog 自己的背景或 padding 上，事件目標同樣是 dialog 本身，只看目標會把對話框誤關（引用："This distinguishes between a click on the backdrop vs a click on the dialog's background/padding."）
- 退路：保住主要行為——偵測缺少 closedBy 時監聽點擊並比對對話框矩形座標，Safari 也能點背景關閉不誤關
- 解鎖：只寫 HTML 屬性就能替模態對話框啟用點背景與 Esc 關閉，不必自己寫點擊座標判斷來分辨邊距與遮罩

經過：點背景關閉看似一行判斷，但 backdrop 和 dialog 的 padding 在事件上長得一樣，手寫版常常點內容邊緣就關掉。交給瀏覽器就沒有這個分辨問題。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：<dialog closedby>：Limited availability，Supported by: Chrome 134, Edge 134, Firefox 141；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前點外面關閉要自己算座標 → 現在圖片燈箱、快速預覽、設定面板可以只寫屬性就有和原生 app 一樣的關閉手感。Safari 仍需退路腳本
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:light-dismiss-a-dialog:2" %%
## 對話框裡會用 Esc 的元件要自己攔住 Esc
- 做法：模態對話框裡有選單、combobox 這類用 Esc 的元件時，讓它們聚焦時自己處理 Esc
- 對手：元件想用 Esc 收起清單，結果整個對話框被意外關掉（引用："this may lead to the dialog being inadvertently closed"）
- 退路：不需要——模態對話框的 Esc 關閉行為皆已支援，由內層元件聚焦時攔截 Esc 即可避免誤關
- 解鎖：（缺）

經過：在對話框的下拉選單裡按 Esc 想取消選擇，填到一半的表單整個消失。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：模態 dialog 的 Esc 行為：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:light-dismiss-a-dialog:3" %%
## `closedby` 只對 `showModal()` 開的對話框有用
- 做法：要點背景關閉時一律用 `showModal()` 開啟；非模態（`show()`）的對話框不依賴 `closedby`
- 對手：用 `show()` 開的非模態對話框沒有背景，不會觸發點外面關閉（引用："as they do not have a backdrop and won't trigger light-dismiss"）
- 退路：保住主要行為——點背景關閉原本只用於模態 dialog，不支援 closedby 的 Safari 亦由座標退路涵蓋
- 解鎖：（缺）

經過：屬性寫了、點外面卻沒反應，原因是對話框根本沒有「外面」那層。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：<dialog closedby>：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：保留一顆看得到的關閉按鈕；對話框要有可及名稱；關閉前要做的事聽 `close`／`cancel` 而非 `click`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
