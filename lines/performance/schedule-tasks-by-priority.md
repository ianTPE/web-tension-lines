---
guide: schedule-tasks-by-priority
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/schedule-tasks-by-priority.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依優先序排程工作

%% line-start id="mwg:schedule-tasks-by-priority" %%
## 用 `scheduler.postTask()` 把工作分成 user-blocking／user-visible／background 三級
- 做法：輸入處理、關鍵渲染用 `priority: 'user-blocking'`；可見但不擋操作的內容用預設的 `user-visible`；分析、預取用 `background`；不支援時條件載入 `scheduler-polyfill`
- 對手：指南只說目前畫面的工作比送分析、預取資源重要，要讓瀏覽器對使用者輸入保持回應，沒說不分優先序時在哪個時刻出問題（引用："Completing tasks for the current view is more important than sending analytics or prefetching assets."）
- 退路：保住主要行為——Safari 條件載入 `scheduler-polyfill` 仍能維持任務優先序，只須多載腳本
- 解鎖：用 `scheduler.postTask()` 將工作依急迫性分為三級排程，確保背景工作不卡住輸入

經過：分析、預取和畫面更新原本都在同一條佇列裡先到先做。分三級之後，背景工作只在閒下來時跑；Safari 得靠 polyfill。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：Scheduler API：Limited availability。Supported by: Chrome 129, Edge 129, Firefox 142。Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：筆記或文件編輯器可以把「打字回應」排最前、「預覽重繪」排中間、「建搜尋索引與同步」丟背景，同一條主執行緒上也不會打字卡頓。Safari 要靠 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
