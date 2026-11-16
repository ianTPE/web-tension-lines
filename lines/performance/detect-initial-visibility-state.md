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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：讀 `performance.getEntriesByType('visibility-state')`，第一筆是 `hidden` 就代表頁面在背景載入，並用第一筆 `hidden` 的 `startTime` 當進入背景的時間，把這類頁面從效能分析中濾掉
- 被什麼擋：在腳本執行時才讀 `document.visibilityState` 有競態：頁面在背景開啟、腳本載完前被切到前景，讀到的是 `visible`，誤判成前景載入（引用："When your script finally runs, `document.visibilityState` will synchronously read as `'visible'`, and you will incorrectly assume the page was loaded in the foreground, completely missing its initial hidden state."）
- 戰報：僵持——Chrome／Edge 的時間軸不論腳本何時執行都記得完整的可見性歷史；Firefox 與 Safari 只能退回 `document.visibilityState`，指南直說那對判斷初始背景狀態「highly inaccurate」（官方宣稱）

經過：背景開啟的分頁渲染被延後，FCP 這類指標被拉長，混進統計就把數字弄歪。非同步載入的分析腳本常在使用者切回來之後才跑，只看當下狀態就漏掉了。只有 Chromium 能拿到正確答案。
%% line-end %%

### 細節（不索引）
- 對手組：效能量測失真或有盲點
- 支援狀態：Page visibility state performance entries：Limited availability。Supported by: Chrome 115, Edge 115；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：自架的 RUM 可以自動把「背景開啟」的造訪標記出來另外統計，載入時間的中位數不再被中鍵開分頁的人拉高。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
