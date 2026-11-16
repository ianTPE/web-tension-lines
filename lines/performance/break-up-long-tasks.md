---
guide: break-up-long-tasks
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/break-up-long-tasks.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 拆開長任務

%% line-start id="mwg:break-up-long-tasks" %%
## 用 scheduler.yield() 把長迴圈切段，讓點擊不必等迴圈跑完
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 async 的長迴圈裡設 50ms 的時間預算，超過就 `await scheduler.yield()` 把主執行緒還給瀏覽器，再重設預算繼續處理
- 被什麼擋：大量運算或長迴圈占住主執行緒，事件處理被延後，INP 變差（引用："Heavy computations or long loops can block the main thread, delaying event handlers and causing poor Interaction to Next Paint (INP) responsiveness."）
- 戰報：部分改善——支援的瀏覽器會在每段之間先處理使用者輸入與繪製；Safari 不支援，必須以 `setTimeout(resolve, 0)` 當 fallback 讓出主執行緒（官方宣稱）

經過：一次處理整個大陣列，期間使用者點什麼都要等迴圈結束才有反應。每 50ms 讓出一次，輸入和繪製就能插隊進來。指南沒有說明 `setTimeout` fallback 比 `scheduler.yield()` 差在哪，只要求一定要有。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：Scheduler API：Limited availability。Supported by: Chrome 129, Edge 129, Firefox 142；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：在瀏覽器裡解析大型 CSV、建全文索引、批次處理照片時，介面仍能捲動、能按取消，不必搬到 Worker 也不會整頁卡死。Safari 退回 setTimeout
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
