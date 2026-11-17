---
guide: spatial-navigation
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/spatial-navigation.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 空間導覽（方向鍵移動焦點）

%% line-start id="mwg:spatial-navigation" %%
## 方向上沒有候選項目時不要 `preventDefault()`，讓瀏覽器照常捲動
- 做法：只在複合元件裡攔方向鍵；找到候選項目才 `preventDefault()`、移動 roving tabindex 並 `scrollIntoView({ block: 'nearest', inline: 'nearest' })`；找不到就直接 return；有修飾鍵、事件已被處理、或目標本身會用方向鍵（可編輯欄位、滑桿）時都不攔
- 對手：無條件攔截方向鍵，會讓瀏覽器原生的捲動失效、破壞可及性（引用："Overriding arrow keys unconditionally breaks accessibility (WCAG 1.4.10)."）
- 退路：不需要——方向鍵與 scrollIntoView 屬基礎事件處理，依是否找到候選再阻斷預設行為即可全面相容
- 解鎖：（缺）

經過：媒體列做了方向鍵導覽，焦點在最後一列時按下鍵，整頁卻捲不下去了。
%% line-end %%

### 細節（不索引）
- 對手組：平台慣用操作沒有作用
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:spatial-navigation:2" %%
## 依每次按鍵當下的實際幾何選下一個焦點，不靠索引或 DOM 順序
- 做法：按鍵時讀目前元素與候選元素的 `getBoundingClientRect()`（不快取），以邊緣判斷方向、優先選垂直軸有重疊的，否則以 `gap + w * 垂直偏移` 計分；候選只取通過 `checkVisibility()` 的元素
- 對手：不對稱、會換行或格狀的版面裡，用索引對應會選錯；隱藏元素的矩形可能是 `(0, 0)` 的零尺寸，變成意外的上、左目標（引用："In asymmetrical, wrapped, or grid layouts, index-based mapping fails. … Hidden elements can have a zero-sized rect at `(0, 0)` and must not become accidental `up` or `left` targets."）
- 退路：不需要——getBoundingClientRect() 與 checkVisibility() 屬標準查詢，按鍵時即時重算幾何即可相容
- 解鎖：（缺）

經過：寬卡片和窄卡片混排，按右鍵焦點跳到下一行開頭；某個藏起來的按鈕還讓按上鍵飛到左上角。
%% line-end %%

### 細節（不索引）
- 對手組：視覺順序與DOM順序脫鉤
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:spatial-navigation:3" %%
## roving tabindex 要搭配複合元件角色，光有 tabindex 讀屏不認
- 做法：依用途給容器與項目 `grid`／`gridcell`、`tablist`、`listbox`／`option`、`tree`、`treegrid` 或 `combobox` 等角色
- 對手：只有 tabindex、沒有對應角色時，roving tabindex 在讀屏上不成立（引用："Roving tabindex only works with screen readers when the container and items have appropriate composite-widget roles and states (e.g. grid/gridcell, listbox/option); tabindex alone isn't enough."）
- 退路：不需要——ARIA 複合元件角色與 roving tabindex 屬既有規範，正確配對後各輔助技術皆可識別
- 解鎖：（缺）

經過：鍵盤使用者用得很順，讀屏使用者卻只聽到一堆不相關的按鈕，不知道可以用方向鍵。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:spatial-navigation:4" %%
## 判斷按鍵來源用 `composedPath()[0]`，不要只看 `e.target`
- 做法：以 `e.composedPath()[0]` 取最內層目標，再用 `:read-write, select, input[type="range"], [role="slider"]` 判斷它是否自己要用方向鍵
- 對手：`e.target` 可能被重定向成 shadow host，看不出真正收到按鍵的是裡面的輸入框（引用："Use `e.composedPath()[0]` rather than only `e.target`, because `e.target` can be retargeted to a shadow host."）
- 退路：不需要——composedPath() 與標準表單控制項選擇器皆屬既有規範，各瀏覽器都能判別真實按鍵目標
- 解鎖：（缺）

經過：在某個自訂元件的文字框裡按左鍵想移游標，焦點卻跳到旁邊的卡片。
%% line-end %%

### 細節（不索引）
- 對手組：封裝邊界切斷關聯
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：不要加 h/j/k/l、W/A/S/D 這類單字元快捷鍵
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
