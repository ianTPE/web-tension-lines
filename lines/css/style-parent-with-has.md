---
guide: style-parent-with-has
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/style-parent-with-has.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 欄位無效時用 :has() 標示整個群組

%% line-start id="mwg:style-parent-with-has" %%
## 用 :has(:user-invalid) 標示含錯誤欄位的整個區塊
- 做法：以 `.card-section:has(:user-invalid)` 改變外層卡片的邊框、背景與標題列的警示圖示，選擇器範圍限定在欄位群組，不掛在 `body`
- 對手：（缺）只說過去要靠 JavaScript 在父元素上切換 class，沒說手寫切換在哪個時刻出錯（引用："Historically, this required JavaScript to toggle classes on parent elements."）
- 退路：不需要——`:has()` 與 `:user-invalid` 已 Widely，不必退路
- 解鎖：欄位群組可用純 CSS 依內部欄位的無效狀態改變外觀

經過：錯誤要標在欄位以外的地方——整個 fieldset 的邊框、卡片標題的圖示——以往得由 JS 監聽再往上加 class。`:has()` 讓祖先直接看子孫的狀態。指南提醒外層標示只是加強，不說明哪一欄錯、錯在哪，每一欄仍要有自己的錯誤文字。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）；`:has()` 本指南未給支援資料（content-based-styling 指南記為 Widely 2023-12-19）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:style-parent-with-has:2" %%
## aria-invalid 先設 "false"，再跟著 :user-invalid 同步
- 做法：所有欄位一開始設 `aria-invalid="false"`，在 blur、change、invalid 事件時依 `:user-invalid` 是否成立改成 `"true"` 或改回
- 對手：`:user-invalid` 不會自動同步 ARIA；不設值時 Firefox 和 Safari 從頁面載入就把空的必填欄位報成無效，Chromium 則在互動後也不報，除非設了 `aria-invalid="true"`（引用："Firefox and Safari expose an empty `required` field as invalid from page load, and Chromium doesn't expose an empty `required` field as invalid after interaction unless `aria-invalid="true"` is set."）
- 退路：不需要——相關原生狀態與 ARIA 已 Widely，不必退路
- 解鎖：（缺）

經過：畫面上的紅框要等使用者離開欄位才出現，螢幕閱讀器卻可能一進頁面就唸「無效」，或反過來錯了也不唸。明確給 `"false"` 起始值，再由腳本跟著 `:user-invalid` 切換，兩邊才對得上。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:style-parent-with-has:3" %%
## 錯誤訊息只在欄位無效時才掛進 aria-describedby
- 做法：欄位用 `data-error` 指向錯誤訊息的 `id`，由腳本只在欄位無效時把該 `id` 加進 `aria-describedby`，修好後移除；標記裡不預先引用
- 對手：錯誤訊息元素一直在頁面上，被 `aria-describedby` 引用的文字即使隱藏也會被唸出（引用："text that `aria-describedby` references is announced even when it's hidden."）
- 退路：不需要——相關原生狀態與 ARIA 已 Widely，不必退路
- 解鎖：（缺）

經過：使用者第一次 Tab 進欄位，還沒輸入任何東西，就聽到「此欄必填」的錯誤。原因是標記裡早就把隱藏的錯誤訊息掛在描述上。改成動態掛載後，錯誤只在真的出現時才被唸。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:style-parent-with-has:4" %%
## 錯誤用全頁一個 polite live region 延遲播報
- 做法：欄位離開或改變時，把錯誤文字送進全頁共用的 polite live region，稍等下一個欄位播報完再更新；失敗送出後聚焦第一個無效欄位
- 對手：每則錯誤各自當 live region，只是被顯示而不是文字內容改變時，讀屏不一定會播；同時播報又會蓋過下一個欄位（引用："a live region that is shown, rather than changed, isn't announced reliably."）
- 退路：不需要——相關原生狀態與 ARIA 已 Widely，不必退路
- 解鎖：（缺）

經過：畫面上的紅字出現了，讀屏卻沒有反應，因為它只對「內容更新」可靠。與 `mwg:accessible-error-announcement:3` 是同一個對手，這份指南提供相同的同步腳本。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
