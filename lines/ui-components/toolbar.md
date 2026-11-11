---
guide: toolbar
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/toolbar.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 工具列

%% line-start id="mwg:toolbar" %%
## 用 aria-disabled 停用，讓控制項仍可聚焦
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：工具列中暫時不能用的按鈕設 `aria-disabled="true"` 並忽略點擊
- 被什麼擋：用 `disabled` 停用後按鈕無法聚焦，方向鍵移動時直接跳過，使用者不知道它存在（引用："Disable with `aria-disabled="true"` rather than `disabled` so the control stays focusable and reachable by arrow keys."）
- 戰報：勝——按鈕保持可聚焦、可被讀出狀態（官方宣稱）

經過：和 copy-button 是同一組對手：停用或隱藏的方式把鍵盤使用者擋在外面。在工具列這種一個 Tab 停點、方向鍵逐一移動的元件裡，被跳過的按鈕等於不存在。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：—
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:toolbar:2" %%
## 用 focusgroup 讓工具列只有一個 Tab 停點
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `role="toolbar"` 容器上加 `focusgroup="toolbar wrap"`，由瀏覽器處理方向鍵與 roving tab stop
- 被什麼擋：（缺）指南規定「同時只能有一個項目在 Tab 順序中」，但沒有描述每個按鈕都是 Tab 停點時具體造成什麼（引用："MANDATORY: Only one item is in the tab order at a time."）
- 戰報：僵持——`focusgroup` 僅 Chrome/Edge 150 支援（官方宣稱）

經過：與 tabs 的 focusgroup 線同形：新屬性取代手寫焦點管理，但對手只寫成規則。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：focusgroup：Limited（Chrome/Edge 150）；Anchor positioning：Limited（資料疑誤，見 app-menus）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
