---
guide: scrollspy
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/scrollspy.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 建立 Scrollspy 導覽

%% line-start id="mwg:scrollspy" %%
## 用 `scroll-target-group` 與 `:target-current` 讓目錄自己標出目前章節
- 做法：導覽容器設 `scroll-target-group: auto`，連結用 `href="#id"` 指向各章節，`nav a:target-current` 標出目前在畫面中的那一節
- 對手：缺——指南只說傳統做法需要 JavaScript 與 `IntersectionObserver`，沒說那種做法在哪個時刻出錯
- 退路：保住主要行為——不支援時改用 IntersectionObserver 與退路類別，保留章節高亮
- 解鎖：目錄可用 CSS 自動標出畫面中的章節，不必用 JavaScript 觀察各節

經過：長篇文件的側欄目錄要跟著捲動亮起。以前要觀察每一節的交會比例再切類別；現在連結自己知道目標是否在畫面中。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：scroll-target-group：Limited availability，Supported by: Chrome 140, Edge 140；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前目錄高亮要為每一節掛觀察器、調門檻 → 現在文件站、單頁產品介紹、長篇報導的章節導覽都能宣告式跟著讀者位置亮起。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scrollspy:2" %%
## `:target-current` 只管外觀，捲動停下時用 `aria-current` 同步給讀屏
- 做法：支援時，載入後與每次 `scrollend` 找出 `nav a:target-current`，把它設 `aria-current="true"`、其他設 `false`
- 對手：`:target-current` 只改視覺，這個狀態不會暴露給螢幕閱讀器（引用："While `:target-current` handles the visual aspect, this is not exposed to screen readers."）
- 退路：保住主要行為——不支援時改用 IntersectionObserver 與退路類別，保留章節高亮
- 解鎖：（缺）

經過：目錄的高亮跟著捲動移動，讀屏使用者逛到目錄時卻聽不出哪一項是目前位置。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：scroll-target-group：Limited availability（Chrome 140, Edge 140）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scrollspy:3" %%
## 原生虛擬類別與退路類別用 `:is()` 合併，不要用逗號並列
- 做法：寫 `nav a:is(:target-current, .target-current)`，退路腳本切換 `.target-current` 類別
- 對手：寫成 `nav a:target-current, nav a.target-current` 時，舊瀏覽器不認得虛擬類別，整條規則失效，退路類別也一起失效（引用："the unrecognized pseudoselector invalidates the entire rule in older browsers."）
- 退路：保住主要行為——不支援時改用 IntersectionObserver 與退路類別，保留章節高亮
- 解鎖：（缺）

經過：在 Firefox 裝好 IntersectionObserver 退路，類別也確實切了，目錄卻始終沒亮。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：:target-current：隨 scroll-target-group 為 Limited availability
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：章節要加 `tabindex="-1"` 讓連結跳轉後鍵盤可從該處繼續；捲動容器不是 `<body>` 時要可聚焦、有名稱與角色；作用中狀態不要只靠顏色
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
