---
guide: responsive-table
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/responsive-table.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 響應式表格

%% line-start id="mwg:responsive-table" %%
## 用 sticky 表頭加容器查詢的堆疊版面，讓大表格在窄處仍可讀
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用語意 `<table>`；`thead` 與列標題 `tbody th` 設 `position: sticky`（明確 z-index、有底色）；包裝層 `container-type: inline-size`，`@container (width < 600px)` 時改成卡片式堆疊，隱藏 `thead`，用 `::before` 與 CSS 變數把欄名注入每一格；長文字維持單行並用截斷技巧
- 被什麼擋：大型資料表在小螢幕上欄位溢出，或被壓縮到無法辨讀（引用："Large data tables often become unreadable on small screens as columns overflow or shrink beyond legibility."）
- 戰報：勝——不論往哪個方向捲都看得到表頭；表格依自己的寬度（放進側欄或窄小工具時）而不是視窗寬度切換成堆疊版面（官方宣稱）

經過：表格一放進手機或側欄，要嘛十欄擠成一團，要嘛往右捲到第七欄時已經不知道這是誰的資料。表頭黏住、窄時改成卡片，資料和標籤的關係就不會斷。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：position: sticky、container queries：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:responsive-table:2" %%
## 可捲動的表格包裝層要能用鍵盤聚焦
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：包裝層加 `tabindex="0"`、`role="region"`，並用 `aria-labelledby` 指向表格的 `<caption>`（或用 `aria-label`）
- 被什麼擋：表格包裝層可以捲動但取不到焦點，只用鍵盤的人無法穩定地捲動表格（引用："Add a `tabindex="0"` attribute to the container, to ensure that people using only a keyboard can consistently scroll the table."）
- 戰報：勝——鍵盤使用者能聚焦表格區域並捲動，輔助技術也知道這塊是什麼（官方宣稱）

經過：表格裡全是文字、沒有連結，Tab 鍵就直接跳過它；超出右邊的欄位，鍵盤使用者永遠看不到。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：tabindex、role：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:responsive-table:3" %%
## 注入的欄名只對非文字內容提供替代文字
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：堆疊版面用 `content: var(--label-2) ": "` 注入欄名；只有非文字內容才在 `/` 後提供可及名稱
- 被什麼擋：對文字內容也提供替代文字，讀屏會把文字和可及名稱都唸一次（引用："Only provide alternative text for non-text content, otherwise this may result in both the text content and accessible name being announced by screen readers."）
- 戰報：勝——欄名只被唸一次（官方宣稱）

經過：每格前面多了「Role:」，若又替它寫一份替代文字，讀屏使用者每格都聽兩遍。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：content 替代文字：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
