---
guide: calculate-total-foreground-time
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/calculate-total-foreground-time.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 計算頁面在前景的總時間

%% line-start id="mwg:calculate-total-foreground-time" %%
## 用 visibility-state 效能條目算出真正在看的時間，不把背景分頁算進去
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `performance.getEntriesByType('visibility-state')` 取得整段可見性歷史，把每段 `visible` 到下一筆狀態變化之間的時間加總
- 被什麼擋：傳統的停留時間把頁面待在背景的時間也算進去（引用："Traditional metrics like time-on-page often incorrectly include time spent with the page in the background."）
- 戰報：僵持——Chrome／Edge 可以從效能時間軸隨時算出前景時間；Firefox 與 Safari 回傳空陣列，fallback 是 `performance.now()`，也就是連背景時間一起算的上限值（官方宣稱）

經過：使用者開了分頁就切走，停留時間照樣一直累積，參與度被灌水。可見性條目把每次切換都記在時間軸上，不必自己監聽 `visibilitychange` 累加。但只有 Chromium 有，其他瀏覽器仍拿到舊的、含背景時間的數字。
%% line-end %%

### 細節（不索引）
- 對手組：效能量測失真或有盲點
- 支援狀態：Page visibility state performance entries：Limited availability。Supported by: Chrome 115, Edge 115；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：部落格或線上課程可以統計每篇文章「真的被看著」的分鐘數，拿來挑出值得改寫的文章，不會被開著不看的分頁灌水。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
