---
guide: highlight-text-ranges
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/highlight-text-ranges.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 標示文字範圍

%% line-start id="mwg:highlight-text-ranges" %%
## 用 CSS Custom Highlight API 標示文字，不動 DOM
- 做法：用 `TreeWalker` 收集文字節點，建立 `Range`，包成 `new Highlight(...ranges)`，以 `CSS.highlights.set("search-results", h)` 註冊，再用 `::highlight(search-results)` 上色；重疊時用 `priority` 決定誰在上面
- 對手：退路把符合的文字包進 `<mark>` 會改動 DOM，要小心保住事件監聽器、別弄壞文件結構（引用："This modifies the DOM, so take care to preserve event listeners and avoid breaking the document structure."）
- 退路：失去主要好處——退回 <mark> 包住文字，仍須改 DOM 並保護監聽器與結構
- 解鎖：不用改動 DOM 結構或拆開文字節點，就能替任意文字範圍套用搜尋結果與語法上色等樣式

經過：頁內搜尋、語法上色、協作游標以前都要把文字切開包元素，切一次就可能把別人掛的監聽器和結構弄掉。現在範圍只是一份登記，樣式由瀏覽器畫上去。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：Custom highlights：Newly（2026-03-24），Supported by: Chrome 105, Edge 105, Firefox 149, Safari 17.2
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前標示文字要拆 DOM → 現在筆記 app 的站內搜尋、程式碼區塊的即時語法上色、多人協作的他人選取範圍，可以疊在框架渲染的內容上而不打架
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:highlight-text-ranges:2" %%
## 有意義的標示用 `<mark>`，不用自訂高亮
- 做法：自訂高亮只用在搜尋結果、語法上色這類暫時的視覺效果；文字的標示本身有意義時用 `<mark>`；錯誤標示另加波浪底線、標籤或圖示
- 對手：自訂高亮純粹是外觀，不在無障礙樹裡，讀屏使用者感受不到標示傳達的意義（引用："Custom highlights are purely presentational and are not exposed to the accessibility tree."）
- 退路：保住主要行為——語意標示本來就應採用所有瀏覽器皆支援的 `<mark>` 與輔助標記，無障礙樹一致保留
- 解鎖：（缺）

經過：同一個黃底，在搜尋結果裡只是提示，在教學文件裡可能就是重點；後者交給 highlight 畫，讀屏使用者就漏掉了。
%% line-end %%

### 細節（不索引）
- 對手組：只改外觀沒改語意或焦點
- 支援狀態：Custom highlights：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「只改外觀沒改語意或焦點」

%% line-start id="mwg:highlight-text-ranges:3" %%
## 註冊新高亮前先清掉舊的
- 做法：每次更新前 `CSS.highlights.clear()`，再 `set()` 新的高亮；文字節點清單快取起來，DOM 內容變了才重建
- 對手：沒清掉時，過期的範圍留在頁面上（引用："to avoid stale ranges persisting on the page"）
- 退路：保住主要行為——不支援 API 時不註冊任何高亮，退回純文字或重建 `<mark>` 皆不會有殘留範圍
- 解鎖：（缺）

經過：搜尋詞換了，上一個詞的標示卻還亮著；登記表不會自己過期。
%% line-end %%

### 細節（不索引）
- 對手組：新屬性的隱藏前提
- 支援狀態：Custom highlights：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「新屬性的隱藏前提」

%% line-start id="mwg:highlight-text-ranges:4" %%
## `::highlight()` 只吃少數幾個屬性
- 做法：`::highlight()` 只用 `color`、`background-color`、`text-decoration`、`text-shadow`、`-webkit-text-stroke-*`、`-webkit-text-fill-color`
- 對手：`background-image`、`font-size`、`padding` 這類屬性寫了會被忽略（引用："Properties like `background-image`, `font-size`, or `padding` are ignored."）
- 退路：保住主要行為——只使用支援的文字色彩與裝飾屬性，若退回 `<mark>` 元素則各類盒模型樣式仍可使用
- 解鎖：（缺）

經過：高亮不是元素，沒有盒子；要加粗、加框、改字級的設計在這裡做不到。
%% line-end %%

### 細節（不索引）
- 對手組：新屬性的隱藏前提
- 支援狀態：Custom highlights：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：高亮與文字、相鄰顏色的對比要符合 WCAG（4.5:1／3:1），且不只靠顏色
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「新屬性的隱藏前提」
