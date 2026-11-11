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
- 戰報：僵持——指南列出的支援資料只有 Safari 27，Chrome/Edge/Firefox 標示不支援，實務上要靠 `@supports` 守門與替代定位（官方宣稱）

經過：選單列是一個 widget：一個 Tab 停點、左右鍵切換選單、聚焦即預覽。每個選單要黏在觸發鈕下方，原生 popover 的預設位置卻是視窗中央。注意：指南的支援資料寫 anchor positioning「僅 Safari 27 支援」，與一般認知不符，見細節。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：Anchor positioning：Limited（指南寫：Supported by Safari 27；Unsupported in Chrome, Edge, Firefox）；Popover：Newly（2025-01-27）；focusgroup：Limited（Chrome/Edge 150）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：支援資料疑誤：多份指南（app-menus、toolbar、navbar、persistent-toast-notifications、persistent-app-tours）都寫 anchor positioning 僅 Safari 27 支援、Chrome 不支援，需確認是否為資料來源取錯子功能
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
