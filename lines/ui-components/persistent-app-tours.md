---
guide: persistent-app-tours
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/persistent-app-tours.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 建立持續顯示的產品導覽

%% line-start id="mwg:persistent-app-tours" %%
## 用 `popover="manual"` 加錨點定位做導覽提示，擋掉使用者一點頁面就關掉
- 做法：導覽步驟用 `<dialog popover="manual" aria-labelledby>`，以 `anchor-name`／`position-anchor`／`position-area` 綁在要介紹的功能旁邊；內放 `popovertargetaction="hide"` 的「知道了」按鈕
- 對手：auto popover 只要使用者點頁面其他地方就會關閉，導覽在使用者試用功能時被意外收掉（引用："Unlike auto popovers, manual popovers do not close when the user clicks elsewhere on the page."）
- 退路：保住主要行為——不支援時分別載入 popover 與錨點定位 polyfill，維持持續貼附提示
- 解鎖：manual popover 結合錨點定位，可讓導覽提示持續貼在功能旁

經過：新功能的提示框一出現，使用者照著去點那個功能，提示就自己消失了。改成 manual 之後，它會跟著功能待著，等使用者說「知道了」。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：Popover：Baseline Newly available（2025-01-27 起）；Anchor positioning：記 Newly（核心屬性 2026-01-13 起 Baseline）。指南寫 "Supported by: Safari 27 … Unsupported in: Chrome, Edge, and Firefox"，為群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線未用 `position-visibility`
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前導覽提示要 JS 算位置、還會被點擊收掉 → 現在「新功能小提示」可以宣告式貼在按鈕旁、讓使用者邊看邊操作，多個提示彼此獨立，各自在使用者走到那一區時才看
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:persistent-app-tours:2" %%
## 打開導覽時把焦點移進去、關閉時送回對應控制項，但不要在頁面載入時搶焦點
- 做法：`showPopover()` 後對提示內的按鈕呼叫 `focus()`；關閉後把焦點移到被介紹的控制項；提示在 DOM 中放在該控制項正前方
- 對手：非模態提示開了焦點卻沒進去，鍵盤與讀屏使用者察覺不到；反過來在載入時搶焦點，又會把帶著目的而來的使用者拉離原本要做的事（引用："Focus must not be moved to these popovers on page load. This is to both prevent confusion from hijacking focus."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：鍵盤使用者按 Tab 走過整頁，完全不知道右側跳出了新功能說明；可是一進頁面就被拉進導覽，又打斷了原本要做的事。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：指南未給此做法的支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 註：指南範例在 `showPopover()` 後立刻 `focus()` 並把 `main` 設 `inert`，與「載入時不可移動焦點」的說明彼此拉扯，兩者原文並列
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:persistent-app-tours:3" %%
## 導覽內容要能獨立讀懂，不要寫「新功能，點這裡」
- 做法：每個提示以標題開頭，文字說清楚功能是什麼、能做什麼，例如「新的聊天功能：開始聊天，與成員一起審閱項目」
- 對手：「點這裡」依賴視覺上指向的東西，看不到畫面的人拿不到，若外面被設成 `inert` 更是完全碰不到（引用："relies heavily on visual information that people may not have, or may not be able to access (particularly if the content outside the popover is `inert`)"）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：讀屏唸出「新功能。點這裡」，使用者不知道這裡是哪裡；外面又被設成 inert，想去找也找不到。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：內容撰寫原則，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:persistent-app-tours:4" %%
## 非模態導覽提示不要蓋住正在取得焦點的控制項
- 做法：鍵盤焦點移到被提示擋住的元素時，調整提示的位置，或在提示已不相關時關掉它
- 對手：非模態 popover 可能蓋住取得焦點的控制項，違反 WCAG 2.4.11（引用："Use of non-modal popovers may result in controls being obscured when they receive focus"）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：使用者 Tab 到下一個按鈕，焦點框卻落在導覽提示底下，看不到自己在哪。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：無特定功能，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：提示內容要能放大到 200%、調整文字間距、320×256 視窗下仍可見；popover polyfill 的 IDL 屬性與 `:popover-open` 合併寫法（同 `mwg:declarative-dialog-popover-control:4`）；錨點定位的 polyfill 與 `@supports` 包法（同 `mwg:viewport-aware-dropdowns:2`、`:3`）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
