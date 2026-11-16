---
guide: form-fields-automatically-fit-contents
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/form-fields-automatically-fit-contents.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 表單欄位自動貼合內容

%% line-start id="mwg:form-fields-automatically-fit-contents" %%
## 用 field-sizing: content 讓輸入框、文字區、下拉選單隨內容伸縮
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `<input>`、`<textarea>`、`<select>` 上設 `field-sizing: content`，並把全域樣式繼承來的 `width`／`height` 重設為 `auto`
- 被什麼擋：表單控制項預設是固定尺寸，不管使用者輸入或選了多少內容都不變，超出的內容只能在欄位裡捲動；要在舊瀏覽器做到自動長高，得用隱藏偽元素即時鏡像輸入內容的 Grid 技巧（引用："Their sizes remain constant, regardless of the amount of content the user enters or selects."）
- 戰報：部分改善——`field-sizing` 為 Newly（2026-06-16）；不支援時退回固定尺寸、內容在欄位內捲動（官方宣稱）

經過：留言框只有三行高，寫長一點就得在小框裡上下捲；要它自己長高，以往得複製一份樣式、用 JS 同步文字到隱藏元素撐開容器。一個屬性取代這整套鏡像。指南建議多數情況直接接受舊瀏覽器的固定尺寸，不必硬做 fallback。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸不跟內容走
- 支援狀態：field-sizing：Newly（2026-06-16；Supported by: Chrome 123, Edge 123, Firefox 152, Safari 26.2）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前「隨打字長高的輸入框」要 JS 鏡像或量測 → 聊天輸入列、行內改名欄位、標籤輸入框可以純 CSS 貼合文字長度，看起來像一般文字、點了就能改
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:form-fields-automatically-fit-contents:2" %%
## 自動寬度的欄位要同時設最小與最大寬度
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `field-sizing: content` 的文字輸入框設 `min-inline-size`（例如 `15ch`）與 `max-inline-size`（例如 `50ch`）；`<select>` 也設 `max-inline-size`
- 被什麼擋：沒有最小寬度時，空欄位縮成寬度 0、點不到；沒有最大寬度時，欄位無限延伸，撐破頁面版面（引用："A minimum size prevents the input from collapsing to a width of zero when empty (making it unclickable), and a maximum size ensures it doesn't expand indefinitely and break the page layout."）
- 戰報：部分改善——上下限讓欄位在兩端都停住；`field-sizing` 本身為 Newly（官方宣稱）

經過：沒有 placeholder 的空輸入框，開了 `field-sizing` 之後直接消失；使用者貼進一長串網址，欄位又把整列推出畫面。給它一段合理的伸縮區間。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：field-sizing：Newly（2026-06-16）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:form-fields-automatically-fit-contents:3" %%
## 自動長高的 textarea 要給固定寬度
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<textarea>` 用 `field-sizing: content` 時設明確寬度（`width: 50ch` 或 `100%`），只讓高度跟著內容長，另設 `min-block-size: 3lh`、`max-block-size: 10lh`
- 被什麼擋：文字區允許水平自動伸縮時，有長 placeholder 的欄位在使用者打下第一個字時會突然縮窄（引用："a textarea with a long placeholder will abruptly shrink horizontally when the user types a single character"）
- 戰報：部分改善——寬度固定後只有高度隨內容換行增長，打字時不會左右跳；`field-sizing` 本身為 Newly（官方宣稱）

經過：placeholder 寫了一整句提示，文字區就撐到那麼寬；使用者一開始打字，placeholder 消失，框瞬間縮成一個字寬。把寬度釘住，只讓它往下長，長到上限再出現捲軸。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：field-sizing：Newly（2026-06-16）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 2 條未拆：全域 CSS 設了 `width: 100%` 等明確尺寸會蓋過 `field-sizing`，得重設為 `auto`（已併入第一條的動作）；Grid／Flexbox 預設拉伸子元素，欄位不肯縮時要加 `align-self: start` 或 `justify-self: start`。
