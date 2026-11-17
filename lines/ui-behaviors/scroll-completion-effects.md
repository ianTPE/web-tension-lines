---
guide: scroll-completion-effects
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/scroll-completion-effects.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 程式捲動完成後觸發效果

%% line-start id="mwg:scroll-completion-effects" %%
## `await scrollIntoView()` 等捲動真的停下，不再用 `setTimeout` 猜時間
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把處理函式寫成 `async`，直接 `await element.scrollIntoView({ behavior: 'smooth' })`（或 `scrollTo()`、`scrollBy()`），之後才加高亮、啟動動畫或移動焦點
- 被什麼擋：用 `setTimeout()` 猜捲動時間，長距離捲動太早觸發、短距離太晚；包一層 `scrollend` promise 又在目標已在畫面內、根本沒捲動時永遠等不到（引用："fires too early on long scrolls and too late on short ones … `scrollend` does not fire when the target is already in view and no scrolling occurs"）
- 戰報：僵持——支援的瀏覽器中 promise 在捲動結束時 resolve、目標已在畫面內就立刻 resolve；僅 Chrome／Edge 150，其他瀏覽器 `await` 會立刻往下跑，要準確就得回到 `scrollend` 加逾時的舊做法（官方宣稱）

經過：點目錄跳到某段並閃一下高亮，結果高亮在段落還在畫面外時就閃完了。捲動方法自己回傳 promise 後，時間點不用猜；但在 Firefox、Safari 還得保留舊的拼裝版本。
%% line-end %%

### 細節（不索引）
- 對手組：完成時機靠猜
- 支援狀態：Scroll method promises：Limited availability，Supported by: Chrome 150, Edge 150；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前「捲到那裡再做事」要猜時間或拼 scrollend → 現在導覽教學、程式碼逐行講解、地圖清單可以一步一步 `await` 捲動再高亮，流程寫成直線。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-completion-effects:2" %%
## 被打斷的平滑捲動也會 resolve，用遞增 ID 擋掉過期的後續效果
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每次捲動前遞增一個操作 ID，`await` 之後若已不是最新 ID 就直接 return
- 被什麼擋：新的捲動打斷進行中的平滑捲動時，瀏覽器會讓所有等待中的 promise resolve 而不是 reject，舊的後續效果照樣執行（引用："the browser aborts the ongoing smooth scroll and **resolves** (does not reject) all pending scroll promises on that container."）
- 戰報：部分改善——只有最後一次捲動的效果會跑（官方宣稱）

經過：使用者快速連點三個章節，三個章節都閃了高亮。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Scroll method promises：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-completion-effects:3" %%
## 捲動完再聚焦時加 `{ preventScroll: true }`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`await` 捲動之後呼叫 `focus({ preventScroll: true })`
- 被什麼擋：`focus()` 預設會自己再捲一次，和剛完成的捲動打架，畫面跳動（引用："so the browser does not jump or scroll a second time."）
- 戰報：勝——焦點移過去、畫面不再跳第二次（官方宣稱）

經過：平滑捲到位、置中好了，聚焦標題時畫面又猛地一跳把標題頂到最上面。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：focus() 的 preventScroll：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 備註：與 `mwg:html:4`（不要隨手用 preventScroll）不衝突：這裡是捲動已經完成後才聚焦
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-completion-effects:4" %%
## Chrome 捲動根捲動器時 promise 會太早 resolve，不要為此多包捲動容器
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：知道這個 bug 存在；巢狀捲動容器上的 `scrollIntoView()` 正常，但不要為了繞過 bug 把內容包進 `overflow-y: auto` 的 div
- 被什麼擋：Chrome 捲動的是文件根捲動器時，`scrollIntoView()` 回傳的 promise 太早 resolve（引用："Chrome has a bug where the `Promise` returned by `scrollIntoView()` resolves too early when it is the document's root scroller that is scrolling."）
- 戰報：僵持——指南只說不要用包容器繞過，沒有給出修正，整頁捲動時效果仍可能提早觸發（官方宣稱）

經過：同一段程式在側欄清單裡時間點剛好，用在整頁時高亮又提早閃了。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Scroll method promises：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：重要資訊不要只靠捲動完成後的視覺變化，要有足夠對比的文字並用 live region 播報
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
