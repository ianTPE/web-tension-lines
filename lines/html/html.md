---
guide: html
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/html.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# HTML

%% line-start id="mwg:html" %%
## 用 <dialog> 的 showModal() 與 closedby="any" 做模態框，不自己寫焦點陷阱與關閉
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：模態覆蓋層用 `<dialog>` 加 `.showModal()`，`closedby="any"` 開啟點背景關閉，`<form method="dialog">` 關閉並回傳 `returnValue`，`::backdrop` 畫背景；非模態的選單與提示用 `popover`
- 被什麼擋：缺——指南只說 `<dialog>` 會自動困住焦點、暗化背景、支援 Esc，`closedby="any"` 不必自訂 JS，沒說手寫版在哪個時刻出錯；只提醒需要焦點陷阱時別用 `show()`
- 戰報：勝——焦點陷阱、Esc、點背景關閉、回傳值都由瀏覽器處理（官方宣稱）

經過：模態框是最常被手寫的元件之一：攔 Tab、攔 Esc、算點擊是否在外面。`<dialog>` 加 `showModal()` 把這些都收進平台，`closedby` 連點背景關閉也宣告式了。仍要提供看得見的關閉按鈕，讓語音控制的使用者知道怎麼離開。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:2" %%
## 用 inert 把整塊隱藏區域移出 Tab 順序與無障礙樹
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：畫面外的選單、自訂抽屜打開時的背景頁面加全域 `inert` 屬性，再用 CSS（例如 `opacity: 0.5`）表示不可操作
- 被什麼擋：缺——指南只說 `inert` 會把這些區域移出 Tab 流程與無障礙樹，沒說留著不處理時具體發生什麼
- 戰報：勝——加上 `inert` 的區域不能聚焦、不被讀屏讀到（官方宣稱）

經過：抽屜打開後，背後的導覽連結仍在 Tab 順序裡，鍵盤使用者一路按會跑到看不見、也不該操作的地方。`inert` 一個屬性把整塊關掉，不必逐一改 tabindex。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:3" %%
## 不要對可聚焦的元素或其祖先加 aria-hidden 或 role="presentation"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`aria-hidden="true"`、`role="none"` 只用在不可聚焦的元素上；背景影片可以，因為省略 `controls` 後它不可聚焦，互動式 `<iframe>` 不行
- 被什麼擋：把元素從輔助技術的樹裡藏起來，卻還能用鍵盤依序走到它（引用："Hiding elements from the assistive technology tree while leaving them accessible to sequential keyboard navigation violates core accessibility heuristics."）
- 戰報：勝——只隱藏不可聚焦的內容，鍵盤能到的地方讀屏也讀得到（官方宣稱）

經過：為了讓讀屏略過一塊裝飾區，把它整個 `aria-hidden`，裡面卻有一個嵌入的互動 iframe。鍵盤使用者 Tab 進去，讀屏一片沉默，不知道自己在哪。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:4" %%
## 不要隨手用 focus({ preventScroll: true })
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：移動焦點時不加 `preventScroll`，除非做過可用性驗證；被聚焦的元素要確保不被其他東西擋住
- 被什麼擋：`preventScroll` 可能讓被聚焦的元素停在畫面外（引用："it can hide the focused element off-screen."）
- 戰報：勝——讓瀏覽器把焦點捲進視野，使用者看得到自己在哪（官方宣稱）

經過：為了避免頁面跳動加上 `preventScroll`，結果焦點移到畫面下方的錯誤欄位，畫面卻沒動，鍵盤使用者打字打進看不見的地方。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:5" %%
## 可捲動的程式碼區塊加 tabindex="0" 與 role="region"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<pre><code>` 會捲動時，`<pre>` 加 `tabindex="0"`、`role="region"`，並以 `aria-labelledby` 或 `aria-label` 命名
- 被什麼擋：可捲動的程式碼區塊不在 Tab 順序裡時，鍵盤使用者到不了它，也就無法捲動看到被截掉的內容（引用："adding `tabindex="0"` to the `<pre>` element if it becomes scrollable, allowing keyboard users to reach the content."）
- 戰報：勝——區塊可聚焦後能用方向鍵捲動，讀屏也會唸出區域名稱（官方宣稱）

經過：長的設定檔範例橫向溢出，滑鼠使用者拖捲軸就好，鍵盤使用者 Tab 不進去，右半邊永遠看不到。加上 tabindex 與區域名稱就能進去捲。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:6" %%
## 不要用 title 屬性做提示
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：提示改用可由鍵盤觸發、讀屏能一致播報的提示模式，不用 `title`
- 被什麼擋：`title` 產生的提示無法用鍵盤取得（引用："DON'T use the `title` attribute to create tooltip effects, as these cannot be accessed using a keyboard."）
- 戰報：勝——可由鍵盤觸發的提示，鍵盤與讀屏使用者都拿得到內容（官方宣稱）

經過：圖示按鈕的說明只放在 `title`，滑鼠停留才看得到，鍵盤聚焦時什麼都不出現。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:7" %%
## 首屏主圖不要 loading="lazy"，改給 fetchpriority="high"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：LCP 元素（主視覺圖）加 `fetchpriority="high"`，CSS 背景主圖用 `<link rel="preload" as="image" fetchpriority="high">`；`loading="lazy"` 只給畫面外的圖片與 iframe
- 被什麼擋：對首屏或主視覺圖片加 `loading="lazy"` 會延後 LCP（引用："DON'T apply `loading="lazy"` to above-the-fold or hero images. This delays LCP."）
- 戰報：勝——主圖提早、優先下載，畫面外的資源才延後（官方宣稱）

經過：為了省頻寬把所有圖片都加上 lazy，結果最重要的那張主圖也要等版面算完才開始下載，最大內容繪製因此變慢。優先度是零和的，`fetchpriority="high"` 也不能到處加，非關鍵的追蹤或後面的輪播圖反而該設 `low`。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:8" %%
## img 與 video 都寫 width 與 height
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：所有 `<img>`、`<video>` 標上 `width` 與 `height` 屬性，`<picture>` 的 `<source>` 也可各自標尺寸
- 被什麼擋：沒有尺寸時載入後才撐開，造成版面位移（引用："DO specify `width` and `height` on all `<img>` tags to preserve aspect ratio and prevent Layout Shifts (CLS)."）
- 戰報：勝——瀏覽器先依比例保留空間，媒體載入後版面不跳（官方宣稱）

經過：文章讀到一半，上方的圖片載完把內容往下推，讀的那行跑掉。寫上寬高後瀏覽器先留好位置。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:html:9" %%
## 登入、地址、付款欄位不要用 autocomplete="off"，改給具體 token
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：憑證、地址、付款、聯絡欄位寫 `autocomplete="email"`、`"street-address"`、`"cc-number"` 等具體值，並和 `type`、`inputmode` 對齊
- 被什麼擋：在這些欄位寫 `autocomplete="off"`，瀏覽器與密碼管理器本來就會刻意忽略它（引用："Browsers and password managers ignore it there by design."）
- 戰報：勝——具體 token 讓自動填入與密碼管理器提供正確的值與動作（官方宣稱）

經過：想關掉自動填入卻寫了 `off`，瀏覽器照樣跳出建議，只是不知道欄位是什麼，填錯的機率反而更高。給它明確的 token 才是能控制的方式。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 4 條未拆（與既有線同一個對手）：表單裡的非送出按鈕寫 `type="button"`（同 `mwg:forms`）；`<summary>` 裡放標題改用標題包按鈕的寫法（同 `mwg:accessibility:2`）；每頁一個 `<h1>`（同 `mwg:accessibility`）；不要用 CSS `order`／`row-reverse` 改焦點順序（同 `mwg:drag-and-drop`）。另有約 20 個糾錯提醒未拆（doctype、`lang`、viewport、地標、`<search>`、正數 tabindex、`<figure>`／`<blockquote>`／`<cite>` 用法、字幕、自動播放音訊、不只靠顏色等），指南沒指出可觀察的後果。
