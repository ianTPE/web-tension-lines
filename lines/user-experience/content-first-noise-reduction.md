---
guide: content-first-noise-reduction
category: user-experience
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/user-experience/content-first-noise-reduction.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 內容優先、降低干擾

%% line-start id="mwg:content-first-noise-reduction" %%
## 用 `scroll-state(scrolled)` 在往下捲時藏起頂端列，往上捲立刻回來
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`html { container-type: scroll-state; }`，`@container scroll-state((scrolled: bottom) and (scrollable: top))` 時對 sticky 頂端列 `transform: translateY(-100%)`；底部分頁列同理往下滑出
- 被什麼擋：缺——指南只說頂端列在閱讀時應該讓開、往上一滑就回來，並強調不需腳本，沒說常駐列或腳本做法在哪個時刻出錯
- 戰報：僵持——支援時純 CSS 依捲動方向收合，`transform` 不影響版面所以內容不跳；僅 Chrome／Edge 144，其他瀏覽器頂端列不收合，要收合得加 scroll 監聽腳本（官方宣稱）

經過：手機上讀長文，頂端列一直佔掉一截畫面。往下讀時它退出去，手指一往上撥它就回來，整個過程不用一行 JS。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Container scroll-state queries：Limited availability，Supported by: Chrome 144, Edge 144；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前「往下藏、往上現」要記錄上一次的 scrollY 並處理回彈 → 現在新聞站頂端列、閱讀器工具列、手機底部分頁列都能用一條容器查詢依捲動方向收放。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:content-first-noise-reduction:2" %%
## 收合的頂端列不要藏住鍵盤焦點，也不要蓋住頁內連結的目標
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`.top-bar:focus-within { transform: none; }` 讓含焦點的列保持可見；`:target { scroll-margin-top: 4rem; }` 至少等於列高
- 被什麼擋：列被收起時焦點仍可能在裡面；黏在頂端的列會蓋住頁內連結跳到的位置（引用："so in-page link targets don't land under the bar."）
- 戰報：勝——焦點在列內時列不收；跳轉後目標落在列的下方（官方宣稱）

經過：點目錄裡的「第三節」，標題剛好被黏在頂端的導覽列蓋住；鍵盤 Tab 進導覽列時，它卻還縮在畫面外。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:content-first-noise-reduction:3" %%
## 收合條件加上 `(scrollable: top)`，按 Home 回到頂端時列一定出現
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：查詢寫成 `scroll-state((scrolled: bottom) and (scrollable: top))`，只在上方還有內容時才收合
- 被什麼擋：Home 鍵這類跳躍不會更新 `scrolled`，單看方向時列在頁首仍維持收起（引用："shows the bar at the very top, even after jumps such as the Home key, which don't update "scrolled"."）
- 戰報：僵持——支援的瀏覽器回到頁首必定顯示列；僅 Chrome／Edge 144（官方宣稱）

經過：讀到一半按 Home 回到頁首，頂端列卻沒回來，得再往上撥一下才出現。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Container scroll-state queries：Limited availability（Chrome 144, Edge 144）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:content-first-noise-reduction:4" %%
## 次要介面收進 `popover` 與抽屜，不放常駐工具列或自寫 JS 浮層
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：選單、溢出動作、提示、懸停卡、導覽提示用 `popover` 加 `popovertarget`；選項多時用固定在一側的 popover 抽屜
- 被什麼擋：缺——指南只說用 popover 取代常駐工具列與自寫 JavaScript 浮層，沒說那些做法在哪個時刻出錯
- 戰報：部分改善——點擊、Enter、Space 開關，auto popover 另有 Esc 與點外面關閉，頂層顯示不必管 z-index；Popover 為 Newly（官方宣稱）

經過：頁首塞滿了很少用的連結。收進一個「更多」按鈕後面的 popover，主畫面只剩內容，鍵盤也照樣打得開。
%% line-end %%

### 細節（不索引）
- 對手組：每顆按鈕手接JS
- 支援狀態：Popover：Baseline Newly available（2025-01-27 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前每個收合選單都要自寫開關、Esc、點外面關閉與層級管理 → 現在部落格、文件站可以把作者資訊、分享、相關連結全收進 HTML 宣告的浮層，主欄只留文章
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:content-first-noise-reduction:5" %%
## 開 popover 優先用 `popovertarget`；用 `commandfor` 時要偵測後才載 polyfill
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：按鈕用 `popovertarget` 開關；若用 `commandfor` 與 `command="toggle-popover"`，在 `'commandForElement' in HTMLButtonElement.prototype` 為 false 時動態載入 `invokers-polyfill`
- 被什麼擋：不支援 Invoker commands 的瀏覽器會忽略 `commandfor`，按鈕按了沒反應（引用："Browsers without invoker commands ignore `commandfor`, so the button does nothing there."）
- 戰報：部分改善——`popovertarget` 在支援 popover 的地方都能用；Invoker commands 為 Newly（官方宣稱）

經過：用 commandfor 寫的「更多」按鈕在舊版 Safari 上按了沒有任何反應。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Invoker commands：Baseline Newly available（2025-12-12 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 5 個糾錯提醒未拆：載入時不要彈電子報或全螢幕廣告，法規要求的通知做成小於視窗 15% 的非模態列；只有後果重大的操作才用阻擋式對話框；預留圖片與嵌入內容的空間、不在可見內容上方插入東西；常駐列小於視窗高度 12% 且不要疊多條；少用的內容（規格、FAQ）收進 `<details>`；popover polyfill 寫法同 `mwg:declarative-dialog-popover-control:4`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
