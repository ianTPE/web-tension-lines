---
guide: accessible-error-announcement
category: accessibility
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/accessibility/accessible-error-announcement.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 無障礙的表單錯誤播報

%% line-start id="mwg:accessible-error-announcement" %%
## 讓 aria-invalid 跟著 :user-invalid 同步，不在還沒填之前就喊錯
- 做法：視覺用 `:user-invalid`，再用一小段 JS 在 `blur`／`change`／`input`／`invalid` 時檢查它，同步設定 `aria-invalid`；在那之前一律設成 `aria-invalid="false"`
- 對手：只靠 `:invalid`，使用者一 Tab 進空的必填欄位，讀屏就唸「Invalid entry」，錯誤在還沒互動前就播出來（引用："screen readers might announce "Invalid entry" the moment a user tabs into a required field that is currently empty."）
- 退路：不需要——`:user-invalid` 已 Widely（2023-11-02），不必退路
- 解鎖：（缺）

經過：`:user-invalid` 只管畫面，不會自動改 ARIA。指南還點出 Firefox 與 Safari 從頁面載入就把空的必填欄位暴露成 invalid，所以 `aria-invalid` 不能留空，要明確設成 `false`。這段橋接 JS 仍得自己寫，因為沒有「UserInvalidChanged」事件。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：解鎖改為缺

%% line-start id="mwg:accessible-error-announcement:2" %%
## 錯誤訊息只在出錯時才掛進 aria-describedby
- 做法：欄位用 `data-error` 指向錯誤訊息的 id，由 script 只在欄位無效時把它加進 `aria-describedby`
- 對手：在標記裡就把錯誤訊息掛上 `aria-describedby`，被引用的文字即使隱藏也會被唸，使用者還沒互動就聽到錯誤（引用："text that `aria-describedby` references is announced even when it's hidden, so the error would be read out before the user has interacted."）
- 退路：不需要——`aria-describedby` 屬既有 ARIA 屬性，指南未附支援資料
- 解鎖：（缺）

經過：錯誤元素一直在頁面上，只是用 `display: none` 藏起來，直覺上掛著也無妨。但 `aria-describedby` 不看可見性，所以引用關係本身就得跟著狀態開關。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）；aria-describedby 指南未給支援資料
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:accessible-error-announcement:3" %%
## 整頁共用一個 polite live region 播錯誤，不讓每則錯誤自己當 live region
- 做法：頁面放一個 `aria-live="polite"` 的區塊，欄位離開或變更後延遲約 500ms 寫入「標籤：錯誤」；送出失敗時把焦點移到第一個無效欄位
- 對手：把每則錯誤訊息做成 live region，它是「被顯示」而不是「內容改變」，讀屏不一定會播（引用："a live region that is shown, rather than changed, isn't announced reliably."）
- 退路：不需要——live region 屬既有 ARIA 機制，指南未附支援資料
- 解鎖：（缺）

經過：常見做法是在錯誤 `<span>` 上加 `aria-live`，然後切換它的顯示，結果時播時不播。指南改成單一播報器寫入文字；欄位修好時還要清空播報器，免得之後瀏覽頁面時又讀到舊錯誤。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）；live region 指南未給支援資料
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
