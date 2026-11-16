---
guide: validate-origins
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/validate-origins.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 比對與驗證網頁的來源與站點

%% line-start id="mwg:validate-origins" %%
## 用 `Origin.from()` 加 `isSameOrigin()` 取代字串前綴比對
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：處理跨視窗 `postMessage` 指令、決定是否附帶憑證這類特權操作時，用 `Origin.from()` 把兩邊都轉成 `Origin` 物件（可以直接傳 MessageEvent、`<a>`、URL），再用 `isSameOrigin()` 比對 scheme、host、port；呼叫包在 try/catch，無效網址與 "null" 一律回 false
- 被什麼擋：`startsWith()` 前綴比對會被 `https://app.example.com.attacker.example` 繞過；帶路徑或明寫預設埠的完整網址，又跟字串比對不相等（引用："Checking `url.startsWith('https://app.example.com')` is bypassed by `'https://app.example.com.attacker.example'`."）
- 戰報：部分改善——由瀏覽器的 URL 解析器正規化後再比，前綴偽造與埠號寫法都不再誤判；Firefox 不支援，要退回用 `new URL()` 比 `.origin`，並先排除 "null"（官方宣稱）

經過：前綴比對在測試時永遠過關，因為沒人會拿 `app.example.com.attacker.example` 來測。改成結構化的來源物件，比的是解析後的三元組，而不是字串長得像不像。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：Origin：Limited availability。Supported by: Chrome 145, Edge 145, Safari 26.5。Unsupported in: Firefox
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前每個收 postMessage 的地方都要自己解析網址、處理預設埠 → 現在嵌入式結帳、登入彈窗、跨視窗小工具可以把事件物件直接丟給 `Origin.from()` 比對，一行完成。Firefox 尚未支援
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:validate-origins:2" %%
## 用 `isSameSite()` 判斷跨子網域的轉址與連結
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：驗證登入後的 `?returnTo=` 轉址目標、把連結分成站內站外時，用 `Origin.from()` 轉成來源後呼叫 `isSameSite()`，做含 scheme 的同站比對
- 被什麼擋：把主機名稱用 `.` 切開判斷同站，遇到 `.co.uk`、`.github.io` 這類多段公共後綴就判錯，也忽略 http 與 https 的差異（引用："Splitting hostnames on `.` to check same-site relationships fails on multi-label public suffixes (such as `.co.uk` or shared hosting domains like `.github.io`) and ignores scheme mismatches (`http:` vs. `https:`)."）
- 戰報：部分改善——`isSameSite()` 用瀏覽器內建的公共後綴清單，`tenant-a.github.io` 與 `tenant-b.github.io` 判為不同站，http 降級也被擋下；不支援的瀏覽器裡 `URL` 拿不到公共後綴清單，只能比對自己掌握的網域，或另載公共後綴清單函式庫（官方宣稱）

經過：`a.co.uk` 和 `b.co.uk` 取最後兩段都是 `co.uk`，於是被當成同一個站。正確答案在瀏覽器手上，只是以前沒有開放出來。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：同 mwg:validate-origins，記 Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前要正確判斷同站，得在前端內附一份公共後綴清單 → 現在跨多個子網域的服務（帳單、說明中心、主站）可以安全地放行彼此之間的轉址，又不怕同一公共後綴下的別人冒用。Firefox 不支援
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:validate-origins:3" %%
## 用 `Origin.from(event)` 分辨不同的沙箱 iframe
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：接收沙箱 iframe（`sandbox="allow-scripts"`）的訊息時，用 `Origin.from(event)` 取出底層的不透明來源，在初始化時由預期的 iframe 釘住一次，之後用 `isSameOrigin()` 比對；釘住前用 `new Origin()` 當誰都不符合的哨兵；轉址目標若 `origin.opaque` 為 true 就拒絕
- 被什麼擋：沙箱 iframe 與 `data:` 網址的 `event.origin` 都序列化成字串 "null"，直接用 `===` 比會把兩個不相干的不透明來源當成同一個（引用："Comparing two serialized runtime origins with `originA === originB` falsely equates two unrelated opaque contexts (`"null" === "null"`)."）
- 戰報：部分改善——同一個沙箱 iframe 的訊息彼此判為同源，不同 iframe 判為不同；不支援的瀏覽器裡 `event.origin` 永遠是 "null"，要改核對 `event.source`，或用初始化時轉給 iframe 的專屬 `MessageChannel`（官方宣稱）

經過：把不可信的程式碼關進沙箱 iframe 是好主意，可是每個沙箱寄來的信都署名 "null"。新 API 讓瀏覽器說出「這封和上一封是不是同一個沙箱寄的」。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：同 mwg:validate-origins，記 Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前同一頁嵌多個沙箱 iframe 時，只能靠 `event.source` 或另開 MessageChannel 分辨誰是誰 → 現在外掛系統、使用者程式碼預覽、多個第三方小工具可以各自關在沙箱裡，訊息仍能可靠地對應回送出的那一個。Firefox 不支援
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:validate-origins:4" %%
## `Origin` API 兩邊都要是 `Origin` 物件，呼叫要包 try/catch
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：比對前兩邊都先 `Origin.from()`；取目前環境的來源用 `Origin.from(self)`；測試裡合成的 `MessageEvent` 退回解析 `event.origin`；對執行期輸入的呼叫全部包在 try/catch，失敗回 false
- 被什麼擋：把原始字串傳給 `isSameOrigin()`、把 `Location`／`Document` 傳給 `Origin.from()`，或在單元測試裡用 `new MessageEvent()` 合成事件，都會丟出 `TypeError`（引用："passing a raw string throws a `TypeError`."）
- 戰報：部分改善——照這個寫法，無效網址、"null" 字串與不支援的物件都安全地回 false，而不是丟出未捕捉的錯誤（官方宣稱）

經過：新 API 比字串嚴格，嚴格到傳錯型別就直接丟錯。來源檢查一丟錯，訊息處理器整個中斷，所以每個呼叫都要有退路。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:validate-origins，記 Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
