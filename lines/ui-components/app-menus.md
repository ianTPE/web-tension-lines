---
guide: app-menus
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/app-menus.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 應用程式選單列

%% line-start id="mwg:app-menus" %%
## 用錨點定位把選單黏在觸發鈕上
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：選單列（File/Edit/View）的每個選單用 popover 搭配 CSS anchor positioning 定位在觸發鈕旁
- 被什麼擋：沒有 anchor positioning 時 popover 退回視窗置中，選單脫離觸發鈕，置中的子選單還會蓋住父選單（引用："Never ship that for a menu: it detaches the menu from its trigger, and a centered submenu covers its parent."）
- 戰報：部分改善——選單黏回觸發鈕；錨點定位的核心屬性（`anchor-name`、`position-area`、`anchor()`）已在 Chrome 125、Firefox 147、Safari 26 支援（Baseline Newly，2026-01-13），更舊的瀏覽器仍要靠 `@supports` 守門（官方宣稱；支援狀態經 2026-11-12 驗證修正）

經過：選單列是一個 widget：一個 Tab 停點、左右鍵切換選單、聚焦即預覽。每個選單要黏在觸發鈕下方，原生 popover 的預設位置卻是視窗中央。指南的支援段寫 anchor positioning「僅 Safari 27 支援」，但這是整個功能群組的狀態，不是本指南用到的屬性的狀態，見細節。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：Anchor positioning 核心屬性：Newly（2026-01-13；`position-anchor` 2026-09-14）。指南原寫 "Supported by: Safari 27. Unsupported in: Chrome, Edge, and Firefox."，那是 web-features 整個 `anchor-positioning` 群組（325 個子項）的最低共同支援；Chrome 與 Firefox 只缺 `position-visibility: anchor-valid / anchor-visible` 兩個值（Chrome 157 beta 才加，Firefox 未支援），本指南沒用到。驗證見 `weekly/2026-11-11.md`。Popover：Newly（2025-01-27）；focusgroup：Limited（Chrome/Edge 150）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：已驗證。11 份指南的 anchor positioning 支援段引用整個 web-features 群組狀態，因兩個沒用到的 `position-visibility` 值而顯示「Chrome 不支援」，會誤導讀者（與代理）以為核心功能不可用
- 變更紀錄：2026-11-12 戰報由「僵持」改為「部分改善」，支援狀態由 Limited 改為 Newly（驗證 web-features 3.45.0、@mdn/browser-compat-data）
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
