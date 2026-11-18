---
guide: carousel-snap-highlights
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/carousel-snap-highlights.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 輪播吸附項目高亮

%% line-start id="mwg:carousel-snap-highlights" %%
## 用 `scroll-state(snapped)` 查詢標亮吸附到位的項目
- 做法：捲動容器設 `scroll-snap-type: x mandatory`，每個項目設 `container-type: scroll-state`，再用 `@container scroll-state(snapped: x)` 改項目內部卡片的樣式；效果包在 `prefers-reduced-motion: no-preference` 裡
- 對手：指南只說不必依賴 IntersectionObserver 或 scroll 監聽器，沒說那些做法在哪個時刻出問題（引用："without relying on JavaScript intersection observers or scroll event listeners"）
- 退路：失去主要好處——Firefox 與 Safari 退回無高亮基本版，或改用 `IntersectionObserver` 腳本而失去純 CSS 做法
- 解鎖：用 `@container scroll-state(snapped)` 純 CSS 標亮吸附到位的輪播項目，免寫捲動或觀察器腳本

經過：輪播停在哪一張，以前要用 observer 監看中間那條細縫才知道。現在吸附本身就是可查詢的狀態，CSS 直接接手；但 Firefox、Safari 還看不到。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Container scroll-state queries：Limited availability，Supported by: Chrome 144, Edge 144；Unsupported in: Firefox, Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「停在中間的那張」要 JS 監看 → 現在相簿、商品輪播、時間軸可以純 CSS 讓停下來的那張放大上色。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:carousel-snap-highlights:2" %%
## 吸附高亮不能拿來當「選取」
- 做法：吸附高亮只當視覺效果；不讓使用者靠捲動吸附來選擇，高亮外觀也不能暗示「作用中」或「已聚焦」，焦點框要和高亮分得開
- 對手：吸附狀態不在無障礙樹裡；容器內有互動元素時，焦點移入會帶動捲動、換掉吸附的項目，吸附到的不一定是聚焦的那個（引用："the snapped item is not exposed to the accessibility tree … This will likely be a source of confusion for users"）
- 退路：保住主要行為——Firefox 與 Safari 即便改用 `IntersectionObserver` 高亮，仍應維持不當選取與分開焦點框
- 解鎖：（缺）

經過：「轉到哪張就是選了哪張」看起來很直覺，但只有看得到的人知道選了什麼；鍵盤一移焦點，吸附又跳到別張。
%% line-end %%

### 細節（不索引）
- 對手組：只改外觀沒改語意或焦點
- 支援狀態：Container scroll-state queries：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「只改外觀沒改語意或焦點」

%% line-start id="mwg:carousel-snap-highlights:3" %%
## 沒被標亮的項目也要保持足夠對比
- 做法：非吸附項目維持足夠對比，不用「灰階加低不透明度、吸附後才清楚」的做法
- 對手：沒被標亮的內容變得難以辨識，使用者也看不出還有其他內容可以往下看（引用："don't make the non-highlighted items in a gallery greyscale with a low opacity … to allow people to understand that there is more content that they can navigate to"）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：為了突顯中間那張，把其他張壓暗是最常見的做法，代價是旁邊的內容看起來像不存在。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：對比要求：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：高亮的閃色效果在減少動態偏好下整個關掉；捲動容器加 `tabindex="0"`、`role="region"` 與可及名稱（同 mwg:carousel-slide-effects:3）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
