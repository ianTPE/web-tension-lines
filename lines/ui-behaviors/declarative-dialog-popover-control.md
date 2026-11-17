---
guide: declarative-dialog-popover-control
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/declarative-dialog-popover-control.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 宣告式控制對話框與彈出層

%% line-start id="mwg:declarative-dialog-popover-control" %%
## 用 `command="show-modal"`、`toggle-popover` 從 HTML 開關對話框
- 做法：`<button commandfor="id" command="show-modal">` 開模態 `<dialog>`、`command="close"` 關閉；popover 用 `toggle-popover`，或分開用 `show-popover`／`hide-popover`
- 對手：指南只說可以移除脆弱的樣板程式、HTML 一解析完就能互動，沒說手寫監聽器在哪個時刻出問題（引用："removes brittle boilerplate code, ensures interactions are functional immediately upon HTML parsing"）
- 退路：保住主要行為——舊瀏覽器條件載入 invokers 與 popover polyfill，開關對話框與彈出層照常可用
- 解鎖：不寫客製 JS 監聽，HTML 解析完按鈕就能宣告式開關對話框與彈出層並內建焦點與無障礙綁定

經過：開一個確認框以前至少要一段 `showModal()` 的 JS。現在按鈕直接指向對話框，頁面還沒跑任何腳本就能開關。
%% line-end %%

### 細節（不索引）
- 對手組：每顆按鈕手接JS
- 支援狀態：Invoker commands：Newly（2025-12-12）；Popover：Newly（2025-01-27）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前模態對話框一定要寫 JS 開 → 現在純 HTML 的靜態頁（說明文件、表單確認、圖片燈箱）也能有原生焦點管理的對話框，腳本壞了照樣能開
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:declarative-dialog-popover-control:2" %%
## 同一顆按鈕別同時寫 `popovertarget` 和 `commandfor`
- 做法：控制同一個 popover 時只用 `popovertarget` 或 `commandfor` 其中一種
- 對手：兩個都寫會切換兩次，功能壞掉（引用："This will double-toggle it, breaking functionality."）
- 退路：保住主要行為——對同一個彈出層只擇一屬性並搭配 polyfill 退路，開關切換就能穩定不打架
- 解鎖：（缺）

經過：兩套宣告式開關都做得到同一件事，疊在一起就是開了又關。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Invoker commands：Newly；Popover：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:declarative-dialog-popover-control:3" %%
## 從 popover 裡面關掉它時，把焦點還給觸發鈕
- 做法：用 popover 內的 `hide-popover` 按鈕關閉時，另寫腳本把焦點送回開啟它的按鈕
- 對手：關閉按鈕跟著被隱藏，焦點遺失（引用："will result in a loss of focus as the button will be hidden and won't retain focus"）
- 退路：保住主要行為——搭配 polyfill 與歸還焦點腳本，不論原生效力或補丁環境都能保住鍵盤導覽
- 解鎖：（缺）

經過：按下「關閉」的那一刻，那顆按鈕自己也不見了，鍵盤使用者被丟回頁首。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Invoker commands：Newly；Popover：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:declarative-dialog-popover-control:4" %%
## popover polyfill 下別用 `popover` 屬性設值，`:popover-open` 要包 `:is()`
- 做法：polyfill 載入前用 `setAttribute()`／`removeAttribute()` 設 popover；樣式寫成 `[popover]:is(:popover-open, .\:popover-open)`；polyfill 只在 `HTMLElement.prototype` 沒有 `popover` 時才載入
- 對手：polyfill 載好前用 IDL 屬性設值，元素不會被 polyfill 接手，還會永遠遮住 polyfill 加的存取子；單寫 `:popover-open` 時，不認得它的瀏覽器丟掉整條規則（引用："otherwise browsers that lack `:popover-open` discard the entire rule"）
- 退路：保住主要行為——透過條件載入 polyfill、屬性操作與 `:is()` 雙選擇器，舊瀏覽器也能正常開關並套用樣式
- 解鎖：（缺）

經過：polyfill 補不出真的偽類，也來不及攔截太早的屬性設定；照原生的寫法寫，舊瀏覽器裡 popover 就是開不起來或沒樣式。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Popover：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
