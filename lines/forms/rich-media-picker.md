---
guide: rich-media-picker
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/rich-media-picker.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 富媒體選擇器（可自訂的 select）

%% line-start id="mwg:rich-media-picker" %%
## 用 appearance: base-select 讓 option 放圖示與說明，擋掉「只能純文字、只好自製下拉」
- 做法：`<select>` 與 `::picker(select)` 都設 `appearance: base-select`，在 `<option>` 裡放 SVG、圖片、標題與說明，按鈕內用 `<button><selectedcontent>` 自動映出選中內容
- 對手：原生 `<option>` 裡的標記會被瀏覽器剝掉，只剩純文字，想要圖示加說明的選項只能改用沉重的自製元件（引用："Prior to this API, the browser would strip tags from `<option>` tags and render only plain text."）
- 退路：保住主要行為——退回作業系統的下拉選單，選單功能與表單送出照常，只是選項只剩純文字
- 解鎖：以前原生 `<option>` 只能放純文字，要圖示加說明得改用沉重的自製元件；現在 option 能直接裝 HTML、行為仍是原生的

經過：角色、方案、帳號這類選項需要圖示和一行說明，原生 select 一律剝成純文字，於是大家改用 JS 框架做的假下拉。`base-select` 讓 option 直接裝 HTML，picker 在 top layer、用錨點定位對齊按鈕。不支援的瀏覽器仍是可用的原生下拉，只是失去圖文版面。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Customizable `<select>`：Limited availability。Supported by: Chrome 135, Edge 135, Safari 27；Unsupported in: Firefox
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：帶頭像的指派人選單、帶色票的標籤選單、帶圖示與一行說明的方案選擇，都能用原生 `<select>` 做，直接參與表單送出，不必再載下拉元件庫。目前 Firefox 退回純文字
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:rich-media-picker:2" %%
## option 文字要能獨立讀懂，擋掉退回時黏成一串的選項
- 做法：在 option 的標題後補上視覺隱藏的句點與「Responsibilities include:」這類銜接文字，讓整段文字脫離版面也通順
- 對手：不支援可自訂 select 的瀏覽器會把 option 內所有文字串成一行，失去視覺設計後意思走樣（引用："would be rendered as "Frontend Developer React, Vue, CSS", in a browser that doesn't support customizable selects."）
- 退路：保住主要行為——退回系統下拉時 option 只剩文字，補上銜接詞後讀起來仍然通順
- 解鎖：（缺）

經過：圖文選項在 Chrome 看起來分層清楚，到 Firefox 變成「Frontend Developer React, Vue, CSS」一串，讀屏也這樣唸。補上視覺隱藏的標點與銜接詞，無論支不支援，文字內容都說得通。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：Customizable `<select>`：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:rich-media-picker:3" %%
## 不要在 option 上加 aria-label 覆寫文字
- 做法：不在 `<option>` 上用 `aria-label` 取代內容，而是讓 option 的完整文字本身就能獨立讀懂
- 對手：`aria-label` 會覆寫 option 的文字，沒寫進 label 的可見文字，讀屏使用者就聽不到；日後改了選項文字也容易漏改（引用："This will result in people missing visible text that hasn't been included in the `aria-label`."）
- 退路：保住主要行為——退回系統下拉時本來就沒有 `aria-label` 可覆寫，選項文字照原樣呈現
- 解鎖：（缺）

經過：為了讓富內容的選項唸起來短一點，在 option 上加 `aria-label`，結果畫面上的說明文字讀屏全聽不到，兩邊內容各自漂移。指南改要求文字本身寫通順，不另外造一個名字。
%% line-end %%

### 細節（不索引）
- 對手組：可及名稱蓋掉可見文字
- 支援狀態：Customizable `<select>`：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:rich-media-picker:4" %%
## 不要在 option 裡放互動元素
- 做法：`<option>` 裡只放文字、圖示等靜態內容，不放連結、按鈕或帶互動語意的元素
- 對手：option 裡的互動元素與語意，讀屏使用者聽不到，因此不會知道那裡還有東西（引用："People using screen readers will not hear the announcements, and as a result, won't be able to determine that further information is present."）
- 退路：保住主要行為——退回系統下拉時選項裡的標記被剝掉，本來就不會出現可操作的內容
- 解鎖：（缺）

經過：option 能放 HTML 之後，很容易順手塞一個「詳情」連結或資訊按鈕。視覺使用者看得到，讀屏使用者完全不知道它存在。需要額外資訊時放在 select 外面。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：Customizable `<select>`：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:rich-media-picker:5" %%
## base-select 不再依最長選項定寬，要自己給寬度
- 做法：開啟 `appearance: base-select` 後，替 select 設固定寬度或用 flex／grid 限制尺寸
- 對手：`base-select` 拿掉了瀏覽器依最長選項決定 select 寬度的預設行為，選項一換寬度就跟著變，造成版面位移（引用："Setting `appearance: base-select` removes the default browser behavior of sizing the select based on its longest option width."）
- 退路：保住主要行為——退回系統選單會照最長選項自動量寬度，不會有版面位移
- 解鎖：（缺）

經過：原生 select 會預先量最長的選項，所以選什麼寬度都不變。換成 base-select 後按鈕寬度跟著選中內容走，選一個長名字整排表單就被推開。補一個寬度限制就好。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Customizable `<select>`：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 2 個糾錯提醒未拆：展開時要有不只靠顏色的選中標示；picker 在 top layer，不要對它設 `z-index`。
