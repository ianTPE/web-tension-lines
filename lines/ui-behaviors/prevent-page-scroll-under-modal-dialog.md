---
guide: prevent-page-scroll-under-modal-dialog
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/prevent-page-scroll-under-modal-dialog.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 防止模態對話框底下的頁面捲動

%% line-start id="mwg:prevent-page-scroll-under-modal-dialog" %%
## 用 `overscroll-behavior: contain` 鎖住模態框後面的頁面，不再改 `<body>` 的 overflow
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `dialog:modal` 設 `overscroll-behavior: contain`；在 `dialog::backdrop` 設 `overflow: hidden` 讓它變成不可捲動的捲動容器，再設 `overscroll-behavior: contain`
- 被什麼擋：`showModal()` 只擋點擊和焦點，不擋捲動：在 backdrop 上滑或在對話框裡滑到底，後面的頁面照樣捲；舊解法在 `<html>`／`<body>` 設 `overflow: hidden` 或 `position: fixed`，又讓捲軸消失、版面橫移、捲動位置跳走（引用："Mutating root overflow removes the page scrollbar (causing horizontal layout shift), can reset or jump the page scroll position, and can break `position: sticky` elements"）
- 戰報：部分改善——支援的瀏覽器在 backdrop 上與對話框內都完全擋住背景捲動；Safari 尚未對「不可捲動的捲動容器」套用 overscroll-behavior，只有對話框內容溢出時才擋得住，但 `showModal()` 仍讓背景 inert（官方宣稱）

經過：模態框開著，使用者在暗掉的背景上滑一下，底下的文章就默默捲走了；用 body 鎖捲動的老招又讓整頁往旁邊跳一下、sticky 標頭壞掉。現在兩條 CSS 宣告就把捲動關在對話框裡，Safari 是剩下的缺口。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：overscroll-behavior（作用於不可捲動的捲動容器）：Limited availability，Supported by: Chrome 144, Edge 144, Firefox 150；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前鎖背景捲動得動根元素、付出版面跳動 → 現在燈箱、確認框、全螢幕設定面板可以純 CSS 鎖住背景，關掉後頁面停在原處、sticky 照常。Safari 只在對話框內容溢出時有效
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:prevent-page-scroll-under-modal-dialog:2" %%
## 不要用 `@supports` 偵測「不可捲動容器」的 overscroll 支援
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把對話框的捲動圍堵當成漸進增強，不用 `@supports (overscroll-behavior: contain)` 或 `CSS.supports()` 分支
- 被什麼擋：所有現代瀏覽器都認得這個屬性語法、偵測一律回傳 true，即使它們只在內容溢出時才執行（引用："All modern browsers support the `overscroll-behavior: contain` property syntax and return `true`, even if they only enforce it when content overflows."）
- 戰報：部分改善——不分支、直接寫，支援的瀏覽器完整圍堵，其他瀏覽器至少在內容溢出時圍堵（官方宣稱）

經過：寫了偵測想替 Safari 補退路，偵測卻在 Safari 也成立，退路永遠不會跑。這個行為無法偵測，只能直接寫、接受差異。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：overscroll-behavior（不可捲動容器）：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：`overflow: clip` 或 `visible` 不建立捲動容器，overscroll-behavior 不會生效（已併入第一條的動作）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
