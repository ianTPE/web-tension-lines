---
guide: optimize-script-priority
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/optimize-script-priority.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 最佳化腳本優先序

%% line-start id="mwg:optimize-script-priority" %%
## 用 `<script fetchpriority>` 讓關鍵腳本先下載、非必要腳本讓路
- 做法：對影響 INP 的關鍵 `async`/`defer` 腳本加 `fetchpriority="high"`；分析、廣告、首屏以下小工具的腳本，以及 body 尾端會阻擋解析的腳本，加 `fetchpriority="low"`
- 對手：瀏覽器依位置與 `async`/`defer` 屬性給腳本預設優先序，body 尾端的腳本會和更關鍵的資源搶頻寬（引用："Use `fetchpriority="low"` on parser-blocking scripts at the end of the body to prevent them from contending for bandwidth with more critical resources."）
- 退路：失去主要好處——不支援時忽略 `fetchpriority`，退回瀏覽器預設排程而失去手動調度
- 解鎖：用 `<script fetchpriority>` 明確調度關鍵與非必要腳本的下載優先序

經過：分析腳本和 app 主程式都是 `async`，瀏覽器分不出誰重要，一起下載、一起搶。標上 high／low 之後，順序由開發者決定；這是漸進增強，舊瀏覽器只是照原樣排。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Fetch priority：Newly available（2024-10-29）。Supported by: Chrome 103, Edge 103, Firefox 132, Safari 17.2
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：塞了聊天外掛、分析、A/B 測試腳本的頁面，可以只用 HTML 屬性讓主程式的互動腳本先到，不必把第三方腳本改成延後手動注入
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:optimize-script-priority:2" %%
## `fetchpriority="high"` 給太多支腳本，大家又一起搶
- 做法：`fetchpriority="high"` 最多只給 1～2 支關鍵腳本；不要每個 `<script>` 都標，只在已知瀏覽器預設不理想時才改
- 對手：high 標太多會造成網路互搶、稀釋提升效果（引用："Only use `fetchpriority="high"` on at most 1-2 critical scripts to avoid network contention and diluting the priority boost."）
- 退路：保住主要行為——不支援時自動忽略 `fetchpriority`，控制標記數量不影響預設載入
- 解鎖：（缺）

經過：每支都標 high，等於每支都沒標；限量之後，優先序才有意義。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Fetch priority：Newly available（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆（不要用已棄用的 `importance` 屬性）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
