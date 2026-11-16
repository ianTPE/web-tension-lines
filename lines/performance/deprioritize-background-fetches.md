---
guide: deprioritize-background-fetches
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/deprioritize-background-fetches.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 降低背景請求的優先序

%% line-start id="mwg:deprioritize-background-fetches" %%
## 用 fetch() 的 priority: 'low' 讓分析與預取讓路給使用者要的資料
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：對分析、記錄、背景同步、預取「以後可能用到」的資料，在 `fetch()` 選項加 `priority: 'low'`；對使用者體驗關鍵的請求不加
- 被什麼擋：同時發出的多個請求搶同一段頻寬，使用者觸發的關鍵請求因此變慢（引用："When a page performs multiple simultaneous network requests, they often compete for the same bandwidth."）
- 戰報：部分改善——標成低優先的請求不再拖慢關鍵請求；不支援的瀏覽器忽略此選項，以預設優先序送出，不需 fallback（官方宣稱）

經過：使用者點了一下，畫面要的資料和同時送出的分析事件、背景同步擠在同一條線上。把背景請求降到低優先，瀏覽器就先把頻寬給使用者正在等的那一個。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Fetch priority：Newly available（2024-10-29）。Supported by: Chrome 103, Edge 103, Firefox 132, Safari 17.2
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：可以大方地在背景預取下一章、下一頁的資料或縮圖，不怕拖慢使用者當下的搜尋或送出；閱讀器、相簿這類「猜你下一步」的介面成本變低
- 另有 1 個糾錯提醒未拆（不要用已棄用的 `importance` 鍵）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
