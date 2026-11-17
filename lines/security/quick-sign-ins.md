---
guide: quick-sign-ins
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/quick-sign-ins.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用即時 UI 模式快速登入

%% line-start id="mwg:quick-sign-ins" %%
## 用 `uiMode: 'immediate'` 在原地登入，不把使用者送去登入頁
- 做法：在「登入」連結、「前往結帳」、收藏／按讚、文章付費牆這類點擊處理器裡，呼叫 `navigator.credentials.get({ password: true, publicKey, uiMode: 'immediate' })`（不帶 `signal`、不帶 `allowCredentials`）；依 `cred.type` 分流到通行金鑰或密碼驗證；拿到 `NotAllowedError` 時退回一般登入流程並保留回到原動作的路徑
- 對手：使用者點了「登入」、開始結帳、收藏或碰到付費牆時被導去專門的登入頁，失去當下情境、流失率上升（引用："Navigating an unauthenticated user to a dedicated sign-in page when they click a "Sign in" link, start checkout, save an item to favorites, or reach an article paywall causes context loss and increases user drop-off."）
- 退路：失去主要好處——Firefox、Safari 不支援即時模式，退回原本的登入頁流程，情境流失與流失率照舊
- 解鎖：以前點收藏或開始結帳就跳去登入頁，動作被打斷；現在能在原地呼叫帳號選擇器，一次點擊就完成登入與動作

經過：讀者按下收藏，被帶去登入頁，登完回來已經忘了要收藏什麼。即時模式讓有憑證的人原地登入並完成動作，沒有憑證的人瞬間退回原本的流程，不會卡在 QR code 對話框。
%% line-end %%

### 細節（不索引）
- 對手組：登入打斷使用者
- 支援狀態：Password credentials：Limited availability。Supported by: Chrome 60, Edge 79。Unsupported in: Firefox and Safari。immediate 模式本身指南只給執行期偵測（`capabilities.immediateGet`），沒附支援資料；getClientCapabilities()：Newly available
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：內容網站的「收藏」「留言」「繼續閱讀」按鈕可以在原地完成登入加動作，回訪讀者不必離開文章；沒有憑證的人仍看到原本的登入表單。支援範圍以執行期偵測為準
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:quick-sign-ins:2" %%
## 專門的登入頁不要用即時模式，否則按鈕按了沒反應
- 做法：最終的登入頁改用條件式 UI（`mediation: 'conditional'` 配 `autocomplete="username webauthn"`）加一般的模態 `get()` 按鈕；即時模式只放在離開目前頁面「之前」的那一刻
- 對手：會到專門登入頁的人多半裝置上沒有本機憑證、或要用手機掃 QR code 或硬體金鑰，而即時模式關掉這些選項、沒有本機憑證就立刻丟 `NotAllowedError`（引用："using it on a dedicated sign-in page traps the user in a dead end where clicking the button does nothing."）
- 退路：保住主要行為——不支援即時模式的瀏覽器本來就走條件式 UI 與一般模態按鈕，專門登入頁不受影響
- 解鎖：（缺）

經過：把最順的按鈕放到登入頁，結果正好碰上最需要 QR code 的那群人，按下去什麼都沒發生。即時模式是攔截用的，不是終點。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:quick-sign-ins，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:quick-sign-ins:3" %%
## 一定要先查 `capabilities.immediateGet`，不能看瀏覽器版本猜
- 做法：呼叫即時模式前用 `PublicKeyCredential.getClientCapabilities()` 確認 `immediateGet`；不支援時直接當成 `NotAllowedError` 走原本的登入流程
- 對手：不認得 `uiMode: 'immediate'` 的瀏覽器會忽略這個鍵，改跳出擋住畫面的通行金鑰與 QR code 對話框（引用："browsers that do not recognize `uiMode: 'immediate'` ignore the unknown dictionary key and open a blocking modal passkey and QR code dialog."）
- 退路：保住主要行為——不支援時把能力視為 false，直接走原本的登入流程，不會跳出 QR code 對話框
- 解鎖：（缺）

經過：本來想「有就原地登入、沒有就算了」，在不支援的瀏覽器上卻變成「每個人都被一個 QR code 對話框打斷」。先問能力，再決定要不要呼叫。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：同 mwg:quick-sign-ins，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：解鎖改為缺

%% line-start id="mwg:quick-sign-ins:4" %%
## 重新驗證不要用即時模式，否則可能選到另一個帳號
- 做法：改密碼、改地址、編輯付款方式、新增通行金鑰之前的重新驗證，照 `passkey-reauthentication` 用非空的 `allowCredentials`
- 對手：即時模式拒絕非空的 `allowCredentials`，省略它又會讓使用者在不知情中選到目前登入者以外的帳號（引用："omitting `allowCredentials` would let the user inadvertently select a different account than the one currently signed in."）
- 退路：保住主要行為——這是選項內容的規則，沒有即時模式時本來就用非空的 `allowCredentials` 走一般流程
- 解鎖：（缺）

經過：即時模式為了隱私不准指定憑證，正好和重新驗證「只能是這個人」的需求相反。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：同 mwg:quick-sign-ins，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:quick-sign-ins:5" %%
## 原地登入後藏起登入按鈕時，把焦點還給原本的動作按鈕
- 做法：原地登入完成、或退回表單送出後隱藏登入觸發點時，把焦點移回原本的動作控制項（或頁首仍存在的已登入控制項），並在 `role="status"` 播報已登入；顯示退回用的內嵌表單時，焦點移到第一個欄位
- 對手：登入觸發點或內嵌表單被隱藏，鍵盤焦點掉回 `document.body`（引用："restore focus to the originating action control (…) so keyboard focus does not drop to `document.body`"）
- 退路：保住主要行為——焦點處理是頁面自己的腳本，不受瀏覽器支援度影響
- 解鎖：（缺）

經過：按下收藏、原地登入成功，「登入」按鈕消失，焦點也跟著不見，鍵盤使用者得從頁首重新 Tab。把焦點放回收藏按鈕，動作就是連續的。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：同 mwg:quick-sign-ins，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆（必須在使用者手勢內呼叫、不帶 `signal`、404 時呼叫 `signalUnknownCredential()` 同 mwg:passkey-authentication:3）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
