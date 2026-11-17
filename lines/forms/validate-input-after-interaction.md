---
guide: validate-input-after-interaction
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/validate-input-after-interaction.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 互動後才驗證輸入

%% line-start id="mwg:validate-input-after-interaction" %%
## 用 :user-invalid 等使用者打完再報錯，擋掉邊打邊變紅
- 做法：用 `type="email"`、`pattern`、`required` 宣告規則，錯誤樣式與錯誤文字用 `:user-invalid` 觸發，`:user-valid` 給成功提示
- 對手：使用者一聚焦開始打字就跳錯誤，例如 email 打到「user@gm」時技術上無效，標準 `:invalid` 立刻顯示錯誤狀態（引用："Standard `:invalid` styling results in an error state appearing immediately, frustrating the user."）
- 退路：不需要——`:user-invalid` 已 Widely，不必退路
- 解鎖：以前只有 `:invalid`，一聚焦打字就整欄變紅；現在能用 `:user-invalid` 等使用者改過並離開才報錯

經過：密碼規則五條，打第一個字就整欄變紅，使用者還沒打完就被告知做錯。`:user-invalid` 照「改過並離開」的時機判斷，打字途中保持中性，離開時才給回饋，修好當下錯誤就消失。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:validate-input-after-interaction:2" %%
## 規則清單滿足後用 visibility: hidden 隱藏，不要收掉空間
- 做法：`.field:has(input:user-valid) .rules-list { visibility: hidden; }`，保留清單佔的空間
- 對手：在 blur 時把規則清單收合，送出按鈕會在 mousedown 與 mouseup 之間移位，那次點擊就丟了（引用："collapsing the list on blur would move the submit button between mousedown and mouseup, and the click would be lost."）
- 退路：不需要——`:user-invalid` 已 Widely，清單要不要收合是版面寫法
- 解鎖：（缺）

經過：使用者填好密碼直接去按送出，按下的瞬間欄位 blur、規則清單收起，按鈕往上跳，放開滑鼠時已不在游標下，什麼都沒發生。保留空間只是隱藏，這個點擊就不會落空。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:validate-input-after-interaction:3" %%
## 密碼要有自己的錯誤文字，不能只把規則清單變紅
- 做法：密碼欄位另給一段錯誤訊息（附帶「Error」文字替代的圖示），規則清單變色只當輔助
- 對手：只把規則清單染紅，沒說哪裡錯，讀屏也不會傳達顏色變化（引用："Turning the rules list red doesn't say what is wrong, and screen readers don't convey the color change."）
- 退路：不需要——`:user-invalid` 已 Widely，錯誤文字怎麼寫是內容決策
- 解鎖：（缺）

經過：密碼不合格時規則清單變紅，看得到顏色的人要自己比對是哪條沒過，讀屏使用者則什麼都沒聽到。加一句明確的錯誤文字，狀態不再只靠顏色。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:validate-input-after-interaction:4" %%
## 格式提示與密碼規則放在欄位上方
- 做法：email 的格式提示、密碼的規則清單放在 `<input>` 上方，並用 `aria-describedby` 連結
- 對手：提示放在欄位下方，編輯時自動完成浮層或行動裝置鍵盤會把它蓋住（引用："Place format hints above the input so autocomplete popovers don't cover them during editing"）
- 退路：不需要——純版面擺放，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：使用者正要照規則輸入密碼時，鍵盤升起或瀏覽器的建議浮層跳出，正好蓋住下方的規則清單。移到上方就避開了。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：不適用（版面擺放，指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:validate-input-after-interaction:5" %%
## fallback 選擇器用 :is() 包起來，擋掉一個不認得就整條失效
- 做法：fallback CSS 寫成 `:is(:user-invalid, .user-invalid-fallback)`，不寫成一般的逗號選擇器清單
- 對手：一般選擇器清單裡只要有一個不支援的選擇器，整條規則都會被丟掉（引用："in a plain selector list, one unsupported selector drops the whole rule."）
- 退路：不需要——`:user-invalid` 已 Widely，fallback 怎麼包是 CSS 寫法
- 解鎖：（缺）

經過：想讓新舊瀏覽器共用一條錯誤樣式，寫成 `:user-invalid, .user-invalid-fallback`，結果舊瀏覽器不認得前者，連 fallback class 的樣式也不套用，fallback 等於白寫。包進 `:is()` 就只略過不認得的那一項。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）；指南未附 `:is()` 的支援資料
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 3 條未拆（與既有線同一個對手，指南文字逐字相同）：`aria-invalid` 起始設 `"false"`（同 `mwg:style-parent-with-has:2`）；錯誤訊息只在無效時掛進 `aria-describedby`（同 `mwg:required-field-feedback:3`）；錯誤改由全頁一個 polite live region 播報（同 `mwg:accessible-error-announcement:3`）。另有 2 個糾錯提醒未拆：`pattern` 是整串比對；`type="email"` 的預設驗證很寬鬆。
