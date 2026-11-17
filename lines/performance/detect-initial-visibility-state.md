---
guide: detect-initial-visibility-state
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/detect-initial-visibility-state.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 偵測頁面一開始是否在背景

%% line-start id="mwg:detect-initial-visibility-state" %%
## 用 visibility-state 效能條目判斷頁面是不是在背景分頁裡載入
- 做法：讀 `performance.getEntriesByType('visibility-state')`，第一筆是 `hidden` 就代表頁面在背景載入，並用第一筆 `hidden` 的 `startTime` 當進入背景的時間，把這類頁面從效能分析中濾掉
- 對手：在腳本執行時才讀 `document.visibilityState` 有競態：頁面在背景開啟、腳本載完前被切到前景，讀到的是 `visible`，誤判成前景載入（引用："When your script finally runs, `document.visibilityState` will synchronously read as `'visible'`, and you will incorrectly assume the page was loaded in the foreground, completely missing its initial hidden state."）
- 退路：失去主要好處——Firefox 與 Safari 退回 `document.visibilityState`，仍有競態漏判且時間精度低
- 解鎖：查 `visibility-state` 效能條目取得完整前景背景歷史，非同步腳本也不會漏判背景載入

經過：背景開啟的分頁渲染被延後，FCP 這類指標被拉長，混進統計就把數字弄歪。非同步載入的分析腳本常在使用者切回來之後才跑，只看當下狀態就漏掉了。只有 Chromium 能拿到正確答案。
%% line-end %%

### 細節（不索引）
- 對手組：效能量測失真或有盲點
- 支援狀態：Page visibility state performance entries：Limited availability。Supported by: Chrome 115, Edge 115；Unsupported in: Firefox, Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：自架的 RUM 可以自動把「背景開啟」的造訪標記出來另外統計，載入時間的中位數不再被中鍵開分頁的人拉高。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
