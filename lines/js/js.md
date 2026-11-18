---
guide: js
category: js
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/js/js.md
first_seen: 2026-11-18（v1.0.1）
license: CC-BY-4.0（上游指南）
---

# JavaScript（內建原語取代手寫替代品）

%% line-start id="mwg:js" %%
## 用 structuredClone() 深拷貝，擋掉 JSON 來回把資料型別洗掉
- 做法：在記憶體裡複製巢狀狀態時用 `structuredClone(value)`，不用 `JSON.parse(JSON.stringify(value))` 或 `_.cloneDeep`；要轉移 `ArrayBuffer` 擁有權時傳 `{ transfer: [...] }`
- 對手：JSON 來回會把 `Date` 變成字串、刪掉值為 `undefined` 的鍵、把 `NaN`／`Infinity` 和陣列空洞變成 `null`（引用："converting `NaN`, `Infinity`, `-Infinity`, and sparse array holes to `null` (and `-0` to `+0`)"）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：不靠函式庫就能深拷貝帶循環參照、`Map`、`Set`、`Date`、TypedArray 的物件

經過：狀態快照用 JSON 來回複製，`createdAt` 回來時已經不是 `Date`，選填欄位的 `undefined` 鍵整個消失。`structuredClone()` 保住這些值，也保住循環參照、`Map`、`Set`，但它不保留自訂類別原型、會對函式與 DOM 節點丟 `DataCloneError`；呼叫端若本來就依賴 JSON 正規化（`toJSON()`、replacer），就不該換。
%% line-end %%

### 細節（不索引）
- 對手組：手寫替代品悄悄弄壞資料
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出

%% line-start id="mwg:js:2" %%
## 用 toSorted()、with()、findLastIndex() 取代先複製再改，擋掉反轉後換算索引出錯
- 做法：`toSorted()`、`toReversed()`、`toSpliced()`、`with(index, value)` 做不改原陣列的轉換；`findLast()`／`findLastIndex()` 做反向搜尋，不再先 `[...arr].reverse()`
- 對手：手寫「反轉副本後 `findIndex()` 再換算回原索引」，沒找到時 `arr.length - 1 - (-1)` 算出 `arr.length`，變成越界索引，而不是 -1（引用："`arr.length - 1 - (-1) === arr.length` evaluates to an out-of-bounds index on a miss whereas `findLastIndex()` returns `-1`."）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：（缺）

經過：找「最後一筆已完成的任務」時，先反轉副本再換算索引，找不到的那一次會拿到一個不存在的位置，後面的更新就寫錯地方。`findLastIndex()` 直接回 -1。指南也提醒：`Set`、`NodeList`、字串沒有這些方法，仍要先轉成陣列；TypedArray 的 `toSorted()` 是數值排序，和一般陣列的字串排序不同。
%% line-end %%

### 細節（不索引）
- 對手組：手寫替代品悄悄弄壞資料
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出

%% line-start id="mwg:js:3" %%
## 用 Object.groupBy()／Map.groupBy() 分組，擋掉 reduce 累加器撞上原型鍵
- 做法：字串鍵分組用 `Object.groupBy(items, fn)`，讀桶子用 `groups[key] ?? []` 或 `Object.hasOwn()`；鍵是物件或要保留數字、布林型別時用 `Map.groupBy()`
- 對手：用 `{}` 當 `reduce()` 累加器分組時，`'constructor'`、`'toString'` 這類鍵會撞上 `Object.prototype` 既有的屬性（引用："keys like `'constructor'` or `'toString'` never collide with `Object.prototype`"）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：（缺）

經過：依使用者輸入的標籤分組，某天有人的標籤叫 `constructor`，普通物件上這個鍵早就有原型繼承來的值，分組結果就和預期不同。`Object.groupBy()` 回傳 null 原型物件，沒有這個問題，但也因此不能呼叫 `groups.hasOwnProperty()`。要邊分組邊轉換或算總和時，仍該留著 `reduce()`。
%% line-end %%

### 細節（不索引）
- 對手組：手寫替代品悄悄弄壞資料
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出

%% line-start id="mwg:js:4" %%
## 用 Promise.withResolvers() 在 executor 外結算，但搬出來的同步程式要自己接錯
- 做法：`resolve`／`reject` 要交給事件監聽、worker 訊息或取消權杖時，用 `const { promise, resolve, reject } = Promise.withResolvers()`；操作本身能寫在 executor 裡時，仍用 `new Promise()`
- 對手：把原本在 executor 裡的同步設定搬出來後，那段程式丟的錯不再自動變成 rejection，而是變成未捕捉的同步例外（引用："synchronous throws inside an executor automatically reject the promise, whereas throws after `Promise.withResolvers()` become uncaught synchronous exceptions."）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：（缺）

經過：把 `let resolve, reject` 外掛變數改寫成 `withResolvers()` 看起來只是整理程式碼，但原本 executor 會替你接住同步錯誤，搬出來之後呼叫端的 `.catch()` 就等不到它。搬動時要包 `try / catch` 並呼叫 `reject(err)`。
%% line-end %%

### 細節（不索引）
- 對手組：新屬性的隱藏前提
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出；2026-11-18 對手組由「新功能的副作用」改為「新屬性的隱藏前提」

%% line-start id="mwg:js:5" %%
## 用 AbortSignal.timeout() 與 any() 設期限，並分辨 TimeoutError 與 AbortError
- 做法：`fetch()` 等可中止的 API 直接傳 `{ signal: AbortSignal.timeout(ms) }`；使用者取消與期限用 `AbortSignal.any([controller.signal, AbortSignal.timeout(ms)])` 合併；`catch` 同時檢查 `'TimeoutError'` 與 `'AbortError'`
- 對手：以為逾時會以 `AbortError` 中止，`catch` 只比對這個名稱，結果逾時被當成別的錯誤處理（引用："DO NOT assume `AbortSignal.timeout(ms)` aborts with `error.name === 'AbortError'`."）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：一個 signal 就能同時表達「使用者按取消」與「超過期限」，先到者中止並帶出原因

經過：手寫 `AbortController` 加 `setTimeout` 改成 `AbortSignal.timeout()` 之後，逾時的 `error.name` 是 `TimeoutError`，原本只認 `AbortError` 的分支就漏接。會隨活動重設的閒置計時器，或要在到期前自訂中止原因的，仍該保留手寫版。
%% line-end %%

### 細節（不索引）
- 對手組：比對錯型別
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出

%% line-start id="mwg:js:6" %%
## 用 URLSearchParams 解析查詢字串，擋掉 split('=') 切掉值裡的等號
- 做法：查詢字串用 `new URLSearchParams(search)` 讀寫，完整網址用 `new URL(url, base).searchParams`；`location.hash` 要先 `slice(1)` 再解析
- 對手：手寫 `.split('=')[1]` 會把值裡的 `=` 切掉，例如 Base64 結尾的補位（引用："such as Base64 padding `?token=aGVsbG8=`, which `.split('=')[1]` truncates"）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：（缺）

經過：從網址拿 token 時用 split 切，結尾的 `==` 不見了，驗證就失敗。`URLSearchParams` 保住值裡的等號，也不會把鍵寫進 `Object.prototype`。但它照表單編碼規則把 `+` 解成空白、重複鍵 `get()` 拿第一個而 `Object.fromEntries()` 留最後一個，也不能拿來解析以分號分隔的 cookie。
%% line-end %%

### 細節（不索引）
- 對手組：手寫替代品悄悄弄壞資料
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出

%% line-start id="mwg:js:7" %%
## 用 TextDecoder／TextEncoder 轉換 UTF-8，擋掉 fromCharCode 的亂碼與堆疊溢位
- 做法：位元組轉文字用 `new TextDecoder().decode(bytes)`，文字轉位元組用 `new TextEncoder().encode(str)`；分塊串流重用同一個 decoder 並傳 `{ stream: true }`，最後再呼叫一次 `decode()` 收尾
- 對手：`String.fromCharCode(...bytes)` 把位元組當 UTF-16 碼元，多位元組 UTF-8 變成亂碼，資料超過約 65 KB 還會撐爆呼叫堆疊（引用："corrupting multi-byte UTF-8 into Latin-1 mojibake and overflowing the call stack at ~65 KB+"）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：分塊讀進來的 UTF-8 串流，切在多位元組字元中間也能正確接回

經過：讀 WebSocket 或檔案分塊時，中文或 emoji 剛好被切在兩塊之間，逐塊用 `fromCharCode` 解碼就出現亂碼，檔案一大還撐爆呼叫堆疊。`TextDecoder` 的 stream 模式會把殘缺的位元組留到下一塊。例外：要餵給 `btoa()` 的原始二進位字串仍要用分段的 `fromCharCode`，否則丟 `InvalidCharacterError`。
%% line-end %%

### 細節（不索引）
- 對手組：手寫替代品悄悄弄壞資料
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出

%% line-start id="mwg:js:8" %%
## 用 replaceChildren() 清空或整批替換子節點，擋掉刪除迴圈漏掉一半
- 做法：`container.replaceChildren()` 不帶參數清空，帶節點或字串時一次清空並插入；`<template>` 要改 `template.content.replaceChildren()`
- 對手：對即時的 `children`／`childNodes` 正向跑刪除迴圈會每隔一個漏刪；`innerHTML = ''` 則要動用 HTML 解析器，在 Trusted Types 下失敗（引用："forward `for` loops over live `children`/`childNodes` skip every other node"）
- 退路：不需要——指南未附支援資料，記不適用，不必退路
- 解鎖：（缺）

經過：重繪通知清單時用 for 迴圈刪舊節點，刪掉第 0 個後第 1 個補位成第 0 個，結果只刪了一半。`replaceChildren()` 一次完成，`MutationObserver` 只收到一筆紀錄。它會連文字與註解節點一起移除，也不解析 HTML 字串；要插入不可信的 HTML 另見 sanitize-untrusted-html。
%% line-end %%

### 細節（不索引）
- 對手組：手寫替代品悄悄弄壞資料
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-18（v1.0.1）首次拆出

另有 2 個糾錯提醒未拆：包裝再丟出錯誤時用 `new Error(message, { cause: err })` 取代字串串接（指南沒說串接在哪個時刻出問題）；事件用 `new Event()`／`new CustomEvent()` 建構並明寫 `bubbles`、`cancelable`、`composed`，不用 `document.createEvent()` 與 `init*Event()`。
