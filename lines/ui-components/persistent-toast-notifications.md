---
guide: persistent-toast-notifications
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/persistent-toast-notifications.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 建立 Toast 通知

%% line-start id="mwg:persistent-toast-notifications" %%
## 用 `popover="manual"` 做 toast，擋掉使用者一操作頁面就把通知關掉
- 做法：每則 toast 是 `popover="manual"`，加進同一個 `role="region" aria-label="Notifications"` 容器；內有 `popovertargetaction="hide"` 的關閉鈕，可用 Tab 到達但出現時不搶焦點
- 對手：toast 不該像選單那樣在使用者操作頁面其他地方時關閉；auto popover 的點外面關閉會把它收掉，也不能多則並存（引用："Unlike menus, they should not close when a user interacts with other parts of the page."）
- 退路：保住主要行為——不支援 popover 時載入 polyfill，保留手動關閉與多則並存
- 解鎖：manual popover 可讓多則通知並存，操作頁面時不會被關掉

經過：表單送出成功的提示剛跳出，使用者順手點了下一個欄位，提示就不見了。換成 manual 之後，它待在固定的通知區，等使用者自己關。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：Popover：Baseline Newly available（2025-01-27 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前 toast 要自己管 z-index 與堆疊、還怕被點擊收掉 → 現在上傳完成、收到新訊息、背景同步結果可以在頂層並存，固定出現在同一個具名區域，讀屏使用者也找得到
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:persistent-toast-notifications:2" %%
## 用 `ariaNotify()` 播報 toast，擋掉讀屏使用者根本不知道有通知
- 做法：toast 顯示時呼叫 `ariaNotify()`，只唸 toast 的可見文字、不唸控制項名稱；若有關閉以外的動作，結尾加「Actions available」；不支援時改用載入時就存在的 `aria-live` 容器，前面放一段說明文字
- 對手：看不到畫面的讀屏使用者不會知道 toast 出現了（引用："This ensures that people using screen readers, who cannot see the screen, are aware of the presence of toast messages"）
- 退路：保住主要行為——不支援時改用頁面載入即存在的 aria-live 容器播報
- 解鎖：`ariaNotify()` 可直接播報通知文字，不必預留 live region

經過：畫面角落閃過「已儲存」，讀屏使用者什麼也沒聽到，以為存檔失敗又按了一次。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：ariaNotify()：Baseline Newly available（2026-09-14 起），Supported by: Chrome 141, Edge 141, Firefox 150, Safari 27
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前播報要預先埋好 live region、還得算好插入時機 → 現在任何短暫狀態（「已複製」「已加入購物車」「連線恢復」）都能一行程式直接唸，不必在 DOM 裡留一個隱藏容器
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:persistent-toast-notifications:3" %%
## Toast 預設不自動消失；會自動消失的，焦點在裡面時要暫停
- 做法：優先做成要手動關閉的 toast；若採逾時消失，先檢查焦點是否在 toast 的控制項上，在的話等焦點離開再關；toast 裡的資訊要在別處也查得到
- 對手：會自動消失的 toast 讓資訊跟著消失，使用者還在讀或正要按裡面的按鈕時就不見了（引用："If the user is focused on a control inside the toast, pause dismissal until focus has left the toast."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：使用者 Tab 到 toast 裡的「復原」按鈕，正要按下，toast 剛好逾時關閉，焦點掉進空白。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：無特定功能，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:persistent-toast-notifications:4" %%
## 有焦點轉移或模態對話框開著時不要跳 toast
- 做法：同時要轉移焦點的情境不發 toast；模態對話框開著時先壓住通知，等對話框關閉再顯示；也不要把 toast 放進模態對話框裡
- 對手：焦點轉移會蓋掉 toast 的播報，使用者漏掉訊息；模態開著時背景的 toast 也很可能被錯過（引用："The focus redirection may cancel out the toast announcements, resulting in people missing information."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：按下儲存後焦點跳回清單，同時跳出「已儲存」toast，讀屏只唸了清單項目，通知被吃掉了。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：無特定功能，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:persistent-toast-notifications:5" %%
## `transition-behavior: allow-discrete` 寫成獨立宣告，不寫進 `transition` 簡寫
- 做法：`transition` 之後另起一行 `transition-behavior: allow-discrete`，讓 toast 進出頂層有動畫；另提供 `prefers-reduced-motion` 的無動畫版本
- 對手：寫進簡寫時，舊瀏覽器會忽略整條 `transition` 宣告（引用："to animate entry and exit from the Top Layer without older browsers ignoring the `transition` declaration."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：加了 allow-discrete 之後，舊版瀏覽器上 toast 的淡入淡出全部消失。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：transition-behavior：指南本篇未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 6 個糾錯提醒未拆：頂層忽略父層 z-index，要用共同容器或 `sibling-index()`（不支援時用 `popover + popover` 加間距）排堆疊；關閉有焦點的 toast 時焦點移到下一則或原處；toast 的動作要在介面其他地方也能做；內容要能放大到 200%、調整間距、在 320×256 下仍可見；popover polyfill 寫法（同 `mwg:declarative-dialog-popover-control:4`）；錨點定位 fallback（同 `mwg:viewport-aware-dropdowns:2`、`:3`）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
