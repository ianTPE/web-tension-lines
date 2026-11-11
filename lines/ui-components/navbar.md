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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用同一棵 `<nav>` 樹；script 比較 `scrollWidth` 與 `clientWidth`，放不下時才收進原生 popover
- 被什麼擋：寫死的斷點：加一個連結、換一種語言、放大文字，導覽列就在錯的寬度擠爆或過早收合（引用："There is no hard-coded breakpoint. Script collapses the navigation only when the inline row (brand, actions and every link) does not fit, so adding a link, a translation or larger text moves the point automatically."）
- 戰報：部分改善——收合點跟著實際內容移動；但判斷仍要 JS 量測，popover 為 Newly，舊瀏覽器要 polyfill（官方宣稱）

經過：傳統導覽列用 media query 在固定寬度切換漢堡選單，翻譯成較長的語言後連結在斷點前就擠出畫面。指南改成量測實際能否放下，沒有 script 時預設收合版，確保永遠可用。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Popover：Newly（2025-01-27）；@starting-style：Newly（2024-08-06）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:navbar:2" %%
## 子選單用 button + aria-expanded，不用 details/summary
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：巢狀導覽的觸發用 `<button aria-expanded aria-controls>`，緊接子選單清單
- 被什麼擋：用 `<details>`/`<summary>` 做子選單，`summary` 該對應 button 角色卻沒有被一致實作（引用："DO NOT use `<details>` and `<summary>`: `<summary>` should map to a `button` role, but has not been consistently implemented"）
- 戰報：勝——button 的角色在各輔助技術中一致（官方宣稱）

經過：和 accordion 指南是同一個對手：summary 的角色在不同螢幕閱讀器表現不一。`<details>` 不寫 JS 就能開合，很誘人，但在導覽情境裡角色不穩定的代價更高。
%% line-end %%

### 細節（不索引）
- 對手組：原生元素角色實作不一致
- 支援狀態：—
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
