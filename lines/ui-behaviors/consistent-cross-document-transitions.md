---
guide: consistent-cross-document-transitions
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/consistent-cross-document-transitions.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 一致的跨文件轉場

%% line-start id="mwg:consistent-cross-document-transitions" %%
## 用 `blocking="render"` 與 `<link rel="expect">` 等新頁面就緒再轉場
- 做法：兩頁都寫 `@view-transition { navigation: auto; }`；新頁面 `<head>` 裡影響版面的腳本加 `blocking="render"`，再用 `<link rel="expect" href="#main-content" blocking="render">` 擋住繪製直到首屏元素被解析，可配 `media` 依視窗寬度選要等的元素
- 對手：新頁面的關鍵資源還沒好就開始轉場，動畫跑向不完整或沒樣式的畫面：元素變形到錯的位置、內容在動畫中重排、轉場結束後備用字型才換成網頁字型；形變目標還沒被解析時，形變退化成分開的淡出淡入（引用："elements morphing to wrong positions, content reflowing mid-animation, or fallback fonts flashing to web fonts after the transition completes"）
- 退路：保住主要行為——不支援的瀏覽器忽略規則並維持一般同源換頁，支援轉場者皆已原生支援阻擋繪製
- 解鎖：不用改成 SPA，多頁網站也能在首屏資源與 DOM 就緒後才平滑轉場，避免元素錯位與重排

經過：跨文件轉場會先拍舊頁、換頁、再動到新頁，問題出在「新頁」那張拍得太早。把首屏需要的腳本和元素宣告成擋繪製條件，拍到的就是完成的樣子。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Cross-document view transitions：Limited availability，Supported by: Chrome 126, Edge 126, Safari 18.2；Unsupported in: Firefox。指南註明支援跨文件轉場的瀏覽器都支援 `blocking="render"` 與 `<link rel="expect">`
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前多頁網站的共享元素轉場常常對到半成品 → 現在部落格列表到文章、商品卡到詳細頁的標題與主圖可以穩定地「飛」過去，不必改成 SPA。Firefox 退回一般換頁
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:consistent-cross-document-transitions:2" %%
## `rel="expect"` 不等圖片，轉場圖片要預載並給尺寸
- 做法：參與形變的圖片用 `<link rel="preload" as="image">` 預載（或預渲染目的頁），並寫 `width`/`height` 或 `aspect-ratio` 加佔位底色
- 對手：`<link rel="expect">` 只等 DOM 元素被解析，不等圖片下載解碼，沒快取的 `<img>` 在新頁快照裡是一個空矩形（引用："an uncached `<img>` may be captured as an empty rectangle in the new-page snapshot"）
- 退路：保住主要行為——不支援跨文件轉場的瀏覽器退回一般換頁；預載與尺寸屬性可在解碼前保住版面佔位
- 解鎖：（缺）

經過：元素「在」不等於圖「到了」。擋到元素出現之後，主圖仍可能是一塊空白在飛。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Cross-document view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「生命週期假設錯」

%% line-start id="mwg:consistent-cross-document-transitions:3" %%
## 只擋首屏關鍵資源，第三方載入器別加 `blocking="render"`
- 做法：`blocking="render"` 與 `rel="expect"` 只用在影響首屏的資源與元素；分析、廣告、標籤管理器不加；擋繪製的腳本保持小而快
- 對手：擋太多會延後轉場；擋繪製總時間超過約 4 秒，瀏覽器整個跳過轉場，`viewTransition.ready` 以 `InvalidStateError` 拒絕；第三方的網路延遲也算進這個逾時（引用："Their network latency counts toward the transition timeout"）
- 退路：保住主要行為——逾時或瀏覽器不支援時會跳過轉場並照常顯示頁面，不會卡死導覽
- 解鎖：（缺）

經過：想讓轉場更穩，就越擋越多；擋到一個慢的第三方腳本，轉場乾脆不做了。
%% line-end %%

### 細節（不索引）
- 對手組：優化用過頭反傷
- 支援狀態：Cross-document view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:consistent-cross-document-transitions:4" %%
## 同一頁不能有重複的 `view-transition-name`
- 做法：每個 `view-transition-name` 在同一頁只給一個元素
- 對手：名稱重複時整個轉場被跳過（引用："Duplicate names cause the entire transition to be skipped."）
- 退路：保住主要行為——名稱重複或不支援時僅跳過轉場動畫，頁面導覽功能仍正常運作
- 解鎖：（缺）

經過：清單裡每張卡都套同一個名字很容易發生，結果不是某張卡沒動畫，而是整個換頁都沒有。
%% line-end %%

### 細節（不索引）
- 對手組：轉場被跳過或錯亂
- 支援狀態：Cross-document view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「轉場被跳過或錯亂」

%% line-start id="mwg:consistent-cross-document-transitions:5" %%
## `pagereveal` 動態指定的名稱要在轉場結束後移除
- 做法：依來源頁在 `pagereveal` 裡指定 `view-transition-name`，在 `viewTransition.finished` 之後清掉；監聽器要用 `blocking="render"` 的腳本提早註冊
- 對手：沒清掉的暫時名稱干擾之後的導覽，也讓頁面進不了 bfcache；監聽器註冊太晚（例如 defer 腳本）時事件已經觸發過了（引用："Stale names interfere with subsequent navigations and prevent the page from entering the bfcache."）
- 退路：保住主要行為——不支援跨文件轉場時略過 `pagereveal` 並照常換頁，結束後移除名稱才能保住 bfcache
- 解鎖：（缺）

經過：為了讓「從列表點進來」才有的形變，臨時給標題一個名字；忘了收回，返回時的轉場和上一頁快取都受影響。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Cross-document view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：減少動態偏好下用 `navigation: none` 關掉跨文件轉場
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
