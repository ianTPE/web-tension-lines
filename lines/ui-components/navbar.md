---
guide: navbar
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/navbar.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 響應式網站導覽列

%% line-start id="mwg:navbar" %%
## 不寫死斷點，量測放不放得下才收合
- 做法：用同一棵 `<nav>` 樹；script 比較 `scrollWidth` 與 `clientWidth`，放不下時才收進原生 popover
- 對手：寫死的斷點：加一個連結、換一種語言、放大文字，導覽列就在錯的寬度擠爆或過早收合（引用："There is no hard-coded breakpoint. Script collapses the navigation only when the inline row (brand, actions and every link) does not fit, so adding a link, a translation or larger text moves the point automatically."）
- 退路：保住主要行為——不支援 popover 時載入 polyfill，保留收合導覽與開合行為
- 解鎖：量測實際寬度即可在放不下時收合成 popover，不必寫死斷點

經過：傳統導覽列用 media query 在固定寬度切換漢堡選單，翻譯成較長的語言後連結在斷點前就擠出畫面。指南改成量測實際能否放下，沒有 script 時預設收合版，確保永遠可用。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Popover：Newly（2025-01-27）；@starting-style：Newly（2024-08-06）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：導覽列放不下時自動收進原生 popover，鍵盤、Esc、點外面關閉都是瀏覽器內建；連結數或語言變了也不用重調斷點
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navbar:2" %%
## 子選單用 button + aria-expanded，不用 details/summary
- 做法：巢狀導覽的觸發用 `<button aria-expanded aria-controls>`，緊接子選單清單
- 對手：用 `<details>`/`<summary>` 做子選單，`summary` 該對應 button 角色卻沒有被一致實作（引用："DO NOT use `<details>` and `<summary>`: `<summary>` should map to a `button` role, but has not been consistently implemented"）
- 退路：不需要——原生 button 與 ARIA 已 Widely，不必退路
- 解鎖：（缺）

經過：和 accordion 指南是同一個對手：summary 的角色在不同螢幕閱讀器表現不一。`<details>` 不寫 JS 就能開合，很誘人，但在導覽情境裡角色不穩定的代價更高。
%% line-end %%

### 細節（不索引）
- 對手組：原生元素角色實作不一致
- 支援狀態：—
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
