---
guide: navigation-drawer
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/navigation-drawer.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 導覽抽屜

%% line-start id="mwg:navigation-drawer" %%
## 抽屜用捲動吸附開關、背景暗度綁在捲動時間軸上
- 做法：模態 `<dialog>` 裡放一個水平捲動容器（抽屜寬度一欄＋整個視窗寬的空白欄），`scroll-snap-type: x mandatory` 讓它只停在開或關；用 `scroll-timeline` 加 `timeline-scope` 把 `--drawer-backdrop`（以 `@property` 註冊為 number）綁到捲動位置，`::backdrop` 的不透明度跟著變；IntersectionObserver 觀察抽屜，完全離開時才 `close()`
- 對手：用 JS 驅動 `transform` 動畫時，抽屜位置由補間決定、不是手指（引用："the scroll mechanism gives the user direct control of the panel's position (their finger drives it, not a tween)"）
- 退路：保住主要行為——不支援捲動時間軸時用 scroll 監聽更新暗度，保留同步淡化
- 解鎖：原生捲動吸附可控制抽屜開合，背景暗度也能跟著拖動位置變化

經過：手機上拉出側欄選單，舊做法放手後播一段固定動畫，拖到一半反悔也拉不回來。改成捲動之後，抽屜就是手指底下的東西，背景的暗度也跟著位置走。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Scroll snap：Widely；Scroll-driven animations：Baseline Newly available（2026-10-27 起）；Registered custom properties：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「跟手」的抽屜與底部面板要手勢函式庫 → 現在側欄導覽、底部動作面板、可拉出的篩選面板都能用原生捲動做，拖動中背景同步變暗，放手自然停在開或關
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:2" %%
## 滿版抽屜不要用 `closedby="any"`，自己判斷點在抽屜外
- 做法：在 dialog 上聽 `click`，目標不在抽屜內就呼叫捲回關閉的 `closeDrawer()`
- 對手：dialog 佔滿整個視窗，點擊落在 dialog 上而不是 `::backdrop`，而且會在沒有滑出動畫的情況下直接關閉（引用："the dialog fills the viewport, so taps land on the dialog rather than its ::backdrop, and it would close without the slide-out animation."）
- 退路：沒說——指南未交代不支援 `closedby` 時怎麼辦
- 解鎖：（缺）

經過：加了 `closedby="any"`，點暗處抽屜瞬間消失，沒有滑出去。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：<dialog closedby>：指南本篇未給支援資料；其他指南記為 Limited
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:3" %%
## 關閉時先捲回去，等觀察器看到抽屜完全離開才 `close()`
- 做法：`closeDrawer()` 只捲到空白欄；IntersectionObserver 在可見比例低於門檻時才呼叫 `drawer.close()`；Esc 的 `cancel` 也 `preventDefault()` 後改走滑出
- 對手：直接呼叫 `close()` 會在動畫途中把元素移出頂層，看不到關閉動畫（引用："doing so would remove the element from the top layer mid-animation and the close animation would not be visible."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：按了關閉鈕，抽屜沒滑出去，直接不見。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Intersection observer：Baseline Widely available（2019-03-25 起）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:4" %%
## 捲動驅動的背景動畫整塊包在 `@supports (animation-timeline: scroll())`
- 做法：`@keyframes`、`@property`、`animation-timeline` 都放進 `@supports` 區塊
- 對手：不支援的瀏覽器仍會解析 keyframes 並套用 `0%` 的值，背景永遠全暗（引用："would apply the animation's `0%` value (--drawer-backdrop: 1) at all times, leaving the backdrop permanently opaque."）
- 退路：保住主要行為——不支援時以 `@supports` 停用 CSS 動畫，改用 scroll 監聽更新暗度
- 解鎖：（缺）

經過：在舊瀏覽器開過一次抽屜，關掉後背景還是一片暗。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Scroll-driven animations：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:5" %%
## 背景暗度的自訂屬性一定要用 `@property` 註冊成數字
- 做法：`@property --drawer-backdrop { syntax: '<number>'; inherits: true; initial-value: 0; }`
- 對手：沒有註冊時瀏覽器把它當字串、無法內插，背景從 0 直接跳到 1（引用："the backdrop would jump from 0 to 1 with no fade."）
- 退路：保住主要行為——不支援 `@property` 時由 scroll 監聽逐幀寫入數值，保留暗度變化
- 解鎖：註冊為數字的自訂屬性可在捲動動畫中平滑內插

經過：拖抽屜時背景不是漸暗，而是在某一點突然變黑。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Registered custom properties：Baseline Newly available（2024-07-09 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:6" %%
## 抽屜高度用 `svh`，不用 `vh` 或 `dvh`
- 做法：抽屜內容設 `height: 100svh`
- 對手：iOS Safari 的網址列在滑動途中縮放，`vh`／`dvh` 讓抽屜高度跟著跳（引用："so the sheet height does not jump when the iOS Safari address bar resizes mid-swipe."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：在 iPhone 上拉抽屜，抽屜高度一抖一抖。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：svh：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:7" %%
## 會兼當側欄的抽屜用 `popover="manual"`，不用 `auto` 或 `hint`
- 做法：一般元素加 `role="dialog"` 與 `popover="manual"`，並自己做 inert、`aria-modal`、焦點還原與 Esc
- 對手：`auto`、`hint` 內建的點外面關閉會在滑動途中觸發（引用："their built-in light-dismiss would also fire mid-swipe."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：手指拖著抽屜往回推，還沒放手抽屜就自己關了。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：showPopover()：Baseline Widely available（2024-04-16 起）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:8" %%
## 寬螢幕會變成常駐側欄的抽屜不要用 `<dialog>`
- 做法：要兼當側欄時改用一般元素加 `role="dialog"`，在側欄狀態時用 `matchMedia()` 拿掉 role
- 對手：`<dialog>` 永遠被當成對話框暴露，但側欄不是對話框（引用："A `<dialog>` element does not work here, since it is always exposed as a dialog, but a sidebar is not one."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：桌機上的固定側欄，讀屏每次都唸「對話框」。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:navigation-drawer:9" %%
## 用 `scroll-initial-target` 讓抽屜一進頂層就停在關閉位置，再滑進來
- 做法：空白欄的 `::after` 設 `scroll-initial-target: nearest`，`showModal()` 後再 `scrollTo({ left: 0 })` 滑進來；不支援時先即時捲到關閉位置、等兩個 `requestAnimationFrame` 再捲回
- 對手：沒有初始位置時，抽屜一出現就在開啟位置，沒有滑入動畫；退路只等一個 rAF 時，第二次 `scrollTo` 會把第一次取消（引用："Without this, the drawer would appear instantly in the open position with no slide-in animation."）
- 退路：保住主要行為——不支援時先即時捲到關閉位置，等兩幀再滑入
- 解鎖：`scroll-initial-target` 可讓抽屜進入頂層時已停在畫面外

經過：點選單鈕，抽屜不是滑出來而是直接出現在那裡。初始捲動位置讓它先待在畫面外，才有東西可以滑。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：scroll-initial-target：Limited availability，Supported by: Chrome 133, Edge 133；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前捲動式抽屜的初始位置要腳本先捲一次再等兩幀 → 現在底部面板、側欄、可拉出的評論區都能在進場前就停在畫面外，開啟只要一次捲動。目前僅 Chromium
- 另有 1 個糾錯提醒未拆：連續按 Esc 時 `cancel` 可能變成不可取消，對話框會瞬間關閉
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
