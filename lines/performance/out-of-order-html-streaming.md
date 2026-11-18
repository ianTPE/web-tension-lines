---
guide: out-of-order-html-streaming
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/out-of-order-html-streaming.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 亂序 HTML 串流

%% line-start id="mwg:out-of-order-html-streaming" %%
## 用 `<?start>`／`<?marker>` 與 `<template for>` 先送骨架、晚到的內容在同一條串流裡補位
- 做法：在文件前段放處理指令 `<?marker name>` 或 `<?start name>…<?end>`（中間放載入中的替代內容），伺服器之後在同一條回應串流裡送出 `<template for="name">`，瀏覽器自動替換；先串流首屏關鍵內容，留言、廣告、相關內容等昂貴區塊放佔位
- 對手：指南只說這是傳統「由上往下」線性處理 HTML 的替代方案，沒說線性處理在哪個時刻出問題（引用："an alternative to the traditional "top-to-bottom" linear processing of HTML"）
- 退路：保住主要行為——Firefox 與 Safari 靠 `template-for-polyfill` 仍能補位替換，只失去免腳本原生支援
- 解鎖：用處理指令與 `<template for>` 在同條串流先出骨架、後補慢區塊，不必綁死由上往下順序

經過：以前一個慢的區塊卡在文件中間，它後面的內容全都得等。改成先放佔位、內容晚點在串流尾端補上，順序不再綁死在文件順序上；只是原生支援只有 Chromium。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：`<template for>`：Limited availability。Supported by: Chrome 150, Edge 150。Unsupported in: Firefox and Safari。HTML processing instructions：同上（不支援的瀏覽器把 `<?marker>` 等當註解解析，polyfill 仍認得）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：純伺服器渲染的頁面（不用前端框架）也能做到「殼先出、慢的區塊後補」：例如部落格文章立刻顯示，留言與相關文章算好再串流進來
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:out-of-order-html-streaming:2" %%
## 用 `streamHTML()` 把 fetch 回應直接串流進 DOM，不等整包 JSON
- 做法：用新的 HTML setter 家族（`setHTML()`、`streamHTML()`、`streamAppendHTML()` 等 24 個方法，含 Safe／Unsafe 版本），把 `fetch` 回應 `pipeTo(el.streamHTML())`，瀏覽器邊收邊渲染
- 對手：指南只說可取代「等整包 JSON 回來再手動建 DOM」，沒說那樣做在哪個時刻出問題（引用："Stream large UI transitions in SPAs using `streamHTML()` instead of waiting for a full JSON payload and manual DOM construction."）
- 退路：保住主要行為——退回 html-setters polyfill，失去原生串流 setter
- 解鎖：用 `streamHTML()` 直接把 fetch 串流接進 DOM 邊收邊畫，不必等整包載完或手切分段

經過：SPA 換頁時得等 JSON 全部到齊、再自己組 DOM。串流 setter 讓 HTML 一邊到一邊畫，但現在還只是 polyfill 撐起來的 API 形狀。
%% line-end %%

### 細節（不索引）
- 對手組：內容要等JS才成形
- 支援狀態：HTML setter methods：Limited（Supported by: Chrome 157, Edge 157. Unsupported in: Firefox and Safari.）；HTML streaming setters（`streamHTML()` 等，本線關鍵功能）："not natively supported by any major browser yet."，故整條仍記無瀏覽器支援
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：伺服器回傳 HTML 片段的「孤島式」頁面，點連結後新內容一段一段流進主區塊，不必寫 JSON API 加前端模板。目前串流 setter 沒有瀏覽器原生支援
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」；2026-11-18（v1.0.1）上游把非串流的 HTML setter methods 改為 Limited（Chrome／Edge 157）；串流 setter 仍無支援，支援狀態與戰報不變

%% line-start id="mwg:out-of-order-html-streaming:3" %%
## live region 只包進度文字，不包整塊串流內容，也不用 `role="alert"`
- 做法：只在「載入中…」這類進度文字的容器上加 live region；不要把整塊內容包進 live region；進度訊息不用 `role="alert"`
- 對手：整塊內容包進 live region，串流完成時讀屏會把補上的全部內容唸一遍；`role="alert"` 讓 NVDA 先唸「Alert」（引用："Do not wrap the entire content in a live region, as this will cause screen readers to announce the full "patched" content when streaming is complete, which can overwhelm screen reader users."）
- 退路：不需要——`aria-live` 機制已 Widely，不必另設退路
- 解鎖：（缺）

經過：好意想讓讀屏使用者知道內容到了，結果整塊內容被一次唸完。把 live region 縮到只剩進度文字，通知就剛好夠。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：aria-live：指南未附支援資料，依既有線（mwg:language-model:3）記 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:out-of-order-html-streaming:4" %%
## 進度通知不要放進 `aria-busy="true"` 的面板裡
- 做法：在要更新的容器上設 `aria-busy="true"`、載完改回 `false`；live region 通知放在這些面板之外
- 對手：通知放進 `aria-busy="true"` 的面板裡，讀屏要等全部內容載完才唸（引用："Do not nest the live region-based notification inside panels with `aria-busy="true"`, as this will prevent screen readers announcing the live region until after all of the content has been loaded."）
- 退路：不需要——`aria-busy` 與 `aria-live` 均已 Widely，不必另設退路
- 解鎖：（缺）

經過：儀表板有好幾個面板慢慢串流進來，進度通知卻被包在忙碌中的面板裡，等到能唸時已經沒有意義了。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：aria-busy／aria-live：指南未附支援資料，依既有線記 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:out-of-order-html-streaming:5" %%
## 佔位被替換時，焦點不能跟著消失
- 做法：替換含有目前焦點元素的佔位時保住焦點；載入期間與載入完成時焦點都留在原處，不要移到新內容（SPA 換頁例外：串流完成後移到新內容開頭）
- 對手：佔位裡若有目前焦點的元素，被替換時焦點會遺失（引用："make sure that focus is not lost if a placeholder containing the active element is replaced."）
- 退路：不需要——一般 DOM 焦點操作已 Widely，不必另設退路
- 解鎖：（缺）

經過：鍵盤使用者正停在佔位裡的某個連結上，串流內容一到，整塊被換掉，焦點掉回頁首。替換時保住焦點，或讓焦點留在不會被換掉的地方。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：焦點管理只用一般 DOM 焦點操作，不涉及新功能；指南未附支援資料，記 Widely（與本指南 :3、:4 同一處理）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:out-of-order-html-streaming:6" %%
## 佔位要先留好尺寸，內容補上時才不會推擠版面
- 做法：佔位給穩定尺寸；最終尺寸未知時用骨架畫面或 CSS `aspect-ratio` 預留空間
- 對手：佔位沒有尺寸，內容補上時版面突然位移（引用："Always provide stable dimensions for placeholders. If the final content size is unknown, use skeleton screens or CSS `aspect-ratio` to reserve space and prevent jarring shifts."）
- 退路：不需要——`aspect-ratio` 等空間預留已 Widely，不必另設退路
- 解鎖：（缺）

經過：亂序串流讓內容晚到，晚到的東西若沒先占好位置，就會在使用者閱讀時把整頁往下推。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：aspect-ratio：指南未附支援資料，依既有線（mwg:css-layout:2）記 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆（不要過度切碎串流、不要假設 `<template for>` 內腳本的執行順序、Trusted Types 環境下的 `*Unsafe` 方法）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
