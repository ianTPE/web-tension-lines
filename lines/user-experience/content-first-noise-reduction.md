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
- 做法：`html { container-type: scroll-state; }`，`@container scroll-state((scrolled: bottom) and (scrollable: top))` 時對 sticky 頂端列 `transform: translateY(-100%)`；底部分頁列同理往下滑出
- 對手：缺——指南只說頂端列在閱讀時應該讓開、往上一滑就回來，並強調不需腳本，沒說常駐列或腳本做法在哪個時刻出錯
- 退路：保住主要行為——不支援時列維持精簡可見，或用 CSS.supports 偵測後改以輕量 scroll 監聽切換收合
- 解鎖：只靠 CSS scroll-state 容器查詢就能隨捲動方向自動收放頂端列，閱讀時騰出畫面且不需寫 JS

經過：手機上讀長文，頂端列一直佔掉一截畫面。往下讀時它退出去，手指一往上撥它就回來，整個過程不用一行 JS。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Container scroll-state queries：Limited availability，Supported by: Chrome 144, Edge 144；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「往下藏、往上現」要記錄上一次的 scrollY 並處理回彈 → 現在新聞站頂端列、閱讀器工具列、手機底部分頁列都能用一條容器查詢依捲動方向收放。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:content-first-noise-reduction:2" %%
## 收合的頂端列不要藏住鍵盤焦點，也不要蓋住頁內連結的目標
- 做法：`.top-bar:focus-within { transform: none; }` 讓含焦點的列保持可見；`:target { scroll-margin-top: 4rem; }` 至少等於列高
- 對手：列被收起時焦點仍可能在裡面；黏在頂端的列會蓋住頁內連結跳到的位置（引用："so in-page link targets don't land under the bar."）
- 退路：不需要——:focus-within 與 scroll-margin-top 已普遍支援，不論純 CSS 或腳本退路皆可避免藏焦點與遮目標
- 解鎖：（缺）

經過：點目錄裡的「第三節」，標題剛好被黏在頂端的導覽列蓋住；鍵盤 Tab 進導覽列時，它卻還縮在畫面外。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:content-first-noise-reduction:3" %%
## 收合條件加上 `(scrollable: top)`，按 Home 回到頂端時列一定出現
- 做法：查詢寫成 `scroll-state((scrolled: bottom) and (scrollable: top))`，只在上方還有內容時才收合
- 對手：Home 鍵這類跳躍不會更新 `scrolled`，單看方向時列在頁首仍維持收起（引用："shows the bar at the very top, even after jumps such as the Home key, which don't update "scrolled"."）
- 退路：保住主要行為——Firefox／Safari 不支援時列常駐或走看 scrollY 的腳本退路，按 Home 回頁首同樣顯示
- 解鎖：（缺）

經過：讀到一半按 Home 回到頁首，頂端列卻沒回來，得再往上撥一下才出現。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Container scroll-state queries：Limited availability（Chrome 144, Edge 144）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:content-first-noise-reduction:4" %%
## 次要介面收進 `popover` 與抽屜，不放常駐工具列或自寫 JS 浮層
- 做法：選單、溢出動作、提示、懸停卡、導覽提示用 `popover` 加 `popovertarget`；選項多時用固定在一側的 popover 抽屜
- 對手：缺——指南只說用 popover 取代常駐工具列與自寫 JavaScript 浮層，沒說那些做法在哪個時刻出錯
- 退路：保住主要行為——偵測缺 popover 時條件載入 @oddbird/popover-polyfill 或手動 JS 退路，選單開關照常運作
- 解鎖：用原生 HTML popover 與 popovertarget 收納次要介面，免寫開關與層級 JS 即享頂層渲染與多種關閉

經過：頁首塞滿了很少用的連結。收進一個「更多」按鈕後面的 popover，主畫面只剩內容，鍵盤也照樣打得開。
%% line-end %%

### 細節（不索引）
- 對手組：每顆按鈕手接JS
- 支援狀態：Popover：Baseline Newly available（2025-01-27 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前每個收合選單都要自寫開關、Esc、點外面關閉與層級管理 → 現在部落格、文件站可以把作者資訊、分享、相關連結全收進 HTML 宣告的浮層，主欄只留文章
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:content-first-noise-reduction:5" %%
## 開 popover 優先用 `popovertarget`；用 `commandfor` 時要偵測後才載 polyfill
- 做法：按鈕用 `popovertarget` 開關；若用 `commandfor` 與 `command="toggle-popover"`，在 `'commandForElement' in HTMLButtonElement.prototype` 為 false 時動態載入 `invokers-polyfill`
- 對手：不支援 Invoker commands 的瀏覽器會忽略 `commandfor`，按鈕按了沒反應（引用："Browsers without invoker commands ignore `commandfor`, so the button does nothing there."）
- 退路：保住主要行為——優先改用 popovertarget，或偵測缺屬性時載入 invokers-polyfill，按鈕都能正常觸發開關
- 解鎖：（缺）

經過：用 commandfor 寫的「更多」按鈕在舊版 Safari 上按了沒有任何反應。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Invoker commands：Baseline Newly available（2025-12-12 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 5 個糾錯提醒未拆：載入時不要彈電子報或全螢幕廣告，法規要求的通知做成小於視窗 15% 的非模態列；只有後果重大的操作才用阻擋式對話框；預留圖片與嵌入內容的空間、不在可見內容上方插入東西；常駐列小於視窗高度 12% 且不要疊多條；少用的內容（規格、FAQ）收進 `<details>`；popover polyfill 寫法同 `mwg:declarative-dialog-popover-control:4`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
