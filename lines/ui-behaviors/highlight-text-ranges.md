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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `TreeWalker` 收集文字節點，建立 `Range`，包成 `new Highlight(...ranges)`，以 `CSS.highlights.set("search-results", h)` 註冊，再用 `::highlight(search-results)` 上色；重疊時用 `priority` 決定誰在上面
- 被什麼擋：退路把符合的文字包進 `<mark>` 會改動 DOM，要小心保住事件監聽器、別弄壞文件結構（引用："This modifies the DOM, so take care to preserve event listeners and avoid breaking the document structure."）
- 戰報：部分改善——任意文字範圍可以上色而 DOM 結構不變；Custom highlights 為 Newly，不支援時退回包 `<mark>`（官方宣稱）

經過：頁內搜尋、語法上色、協作游標以前都要把文字切開包元素，切一次就可能把別人掛的監聽器和結構弄掉。現在範圍只是一份登記，樣式由瀏覽器畫上去。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：Custom highlights：Newly（2026-03-24），Supported by: Chrome 105, Edge 105, Firefox 149, Safari 17.2
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前標示文字要拆 DOM → 現在筆記 app 的站內搜尋、程式碼區塊的即時語法上色、多人協作的他人選取範圍，可以疊在框架渲染的內容上而不打架
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:highlight-text-ranges:2" %%
## 有意義的標示用 `<mark>`，不用自訂高亮
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：自訂高亮只用在搜尋結果、語法上色這類暫時的視覺效果；文字的標示本身有意義時用 `<mark>`；錯誤標示另加波浪底線、標籤或圖示
- 被什麼擋：自訂高亮純粹是外觀，不在無障礙樹裡，讀屏使用者感受不到標示傳達的意義（引用："Custom highlights are purely presentational and are not exposed to the accessibility tree."）
- 戰報：部分改善——有意義的標示經 `<mark>` 讓輔助技術也拿得到（官方宣稱）

經過：同一個黃底，在搜尋結果裡只是提示，在教學文件裡可能就是重點；後者交給 highlight 畫，讀屏使用者就漏掉了。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Custom highlights：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:highlight-text-ranges:3" %%
## 註冊新高亮前先清掉舊的
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每次更新前 `CSS.highlights.clear()`，再 `set()` 新的高亮；文字節點清單快取起來，DOM 內容變了才重建
- 被什麼擋：沒清掉時，過期的範圍留在頁面上（引用："to avoid stale ranges persisting on the page"）
- 戰報：部分改善——畫面上只剩這一次的結果（官方宣稱）

經過：搜尋詞換了，上一個詞的標示卻還亮著；登記表不會自己過期。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Custom highlights：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:highlight-text-ranges:4" %%
## `::highlight()` 只吃少數幾個屬性
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`::highlight()` 只用 `color`、`background-color`、`text-decoration`、`text-shadow`、`-webkit-text-stroke-*`、`-webkit-text-fill-color`
- 被什麼擋：`background-image`、`font-size`、`padding` 這類屬性寫了會被忽略（引用："Properties like `background-image`, `font-size`, or `padding` are ignored."）
- 戰報：部分改善——在允許的屬性內設計，樣式就會生效（官方宣稱）

經過：高亮不是元素，沒有盒子；要加粗、加框、改字級的設計在這裡做不到。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Custom highlights：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：高亮與文字、相鄰顏色的對比要符合 WCAG（4.5:1／3:1），且不只靠顏色
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
