---
guide: custom-button-actions
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/custom-button-actions.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 自訂按鈕動作

%% line-start id="mwg:custom-button-actions" %%
## 用 `command="--自訂指令"` 宣告按鈕要對誰做什麼
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：按鈕寫 `commandfor="目標id"` 與 `command="--spin"` 這類 `--` 開頭的自訂指令，目標元素上監聽 `command` 事件，依 `event.command` 從指令表找動作，用 `event.source` 回寫按鈕的 `aria-pressed`／`aria-expanded`
- 被什麼擋：指南只說能減少手動事件監聽、讓介面和實作脫鉤，沒說手接監聽在哪個時刻出問題（引用："This approach reduces the need for manual event listeners and decouples the UI from implementation details."）
- 戰報：部分改善——按鈕與目標的關係寫在 HTML，一個監聽器處理所有指令；Invoker commands 為 Newly，舊瀏覽器靠 polyfill 派發同樣的事件，但 polyfill 不管 ARIA 狀態（官方宣稱）

經過：每顆按鈕各自 `addEventListener` 再找目標，改一個 id 就要改 JS。現在按鈕只宣告「對誰、做什麼」，行為集中在目標上的一張指令表。
%% line-end %%

### 細節（不索引）
- 對手組：每顆按鈕手接JS
- 支援狀態：Invoker commands：Newly（2025-12-12），Supported by: Chrome 135, Edge 135, Firefox 144, Safari 26.2
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前一組控制鈕要逐顆接 JS → 現在播放器、畫布編輯器、看板卡片的動作鈕可以在 HTML 裡寫 `--play`、`--zoom-in`、`--archive`，伺服器渲染的頁面也能直接帶出可用的按鈕
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:custom-button-actions:2" %%
## `command` 事件不冒泡，監聽器要掛在目標上
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`command` 監聽器直接掛在目標元素上；目標不固定時在祖先用 `{ capture: true }`；目標可能在 shadow root 裡時用 `event.composedPath()[0]`
- 被什麼擋：`command` 事件不冒泡，照一般事件委派掛在祖先上的監聽器收不到（引用："The `command` event does not bubble."）
- 戰報：部分改善——掛在目標或用捕獲階段，指令才收得到（官方宣稱）

經過：習慣在 document 上做事件委派的人，第一次寫 `command` 會發現什麼都沒發生。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Invoker commands：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：自訂指令沒有內建語意，要自己設 `aria-pressed`／`aria-expanded`；開啟 menu/listbox/dialog 等角色時加 `aria-haspopup`；按下後要停用時用 `aria-disabled` 而非 `disabled`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
