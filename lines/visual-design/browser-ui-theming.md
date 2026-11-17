---
guide: browser-ui-theming
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/browser-ui-theming.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 為瀏覽器產生的介面上主題

%% line-start id="mwg:browser-ui-theming" %%
## 先用 CSS 掛鉤客製瀏覽器內建介面，確定不夠用才重做
- 做法：用 `::selection`、`accent-color`、`color-scheme`、`scrollbar-color`、`::placeholder`、`field-sizing: content`、`appearance: base-select` 加 `::picker(select)`、`label:has(:checked)`、`::file-selector-button`、滑桿的軌道與拇指偽元素等，替表單控制項、捲軸、選取文字換外觀
- 對手：重做內建介面會失去瀏覽器免費提供的語意、鍵盤操作、輸入法與輔助技術整合（引用："most notably losing accessible semantics, keyboard handling, IME, and AT integration that the native UI provides for free."）
- 退路：不需要——支援狀態不適用，多數樣式在舊瀏覽器會優雅降級
- 解鎖：（缺）

經過：為了換下拉選單的顏色重寫了一個元件，結果中文輸入法選字、讀屏、鍵盤上下鍵全都要自己補。其實大部分外觀，原生控制項本來就讓你改。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：指南本篇未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:browser-ui-theming:2" %%
## `user-select: none` 只用在介面外框，不要套在內容文字上
- 做法：只在拖曳把手、工具列、重複的按鈕文字上設 `user-select: none`
- 對手：套在內容文字上會破壞複製貼上、翻譯工具與輔助技術的「從這裡開始朗讀」（引用："breaks copy-paste, translation tools, and AT "read from here" gestures."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：想複製文章裡的一段地址，怎麼拖都選不起來，翻譯外掛也抓不到文字。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:browser-ui-theming:3" %%
## `scrollbar-width` 維持 `auto`，除非另有可及的捲動方式
- 做法：不把 `scrollbar-width` 設成 `thin` 或 `none`，除非提供其他可及的捲動控制
- 對手：`thin` 雖然還有拇指，但目標太小，有些使用者操作不了（引用："Although `scrollbar-width: thin` does provide a thumb, the target size of the thumb will be too small for some users to operate."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：手部不穩的使用者想拖細捲軸，試了好幾次都抓不到。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 註：`adapt-scrollbar-to-contrast-preferences` 與 `dark-mode` 的範例都用 `scrollbar-width: thin`，與本指南的建議相左；各照原文
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:browser-ui-theming:4" %%
## 驗證樣式用 `:user-invalid`／`:user-valid`，並排除範圍滑桿
- 做法：用 `:user-invalid`／`:user-valid` 取代 `:invalid`／`:valid`；廣泛套用時寫成 `input:not(input[type="range"]):user-valid`
- 對手：`:invalid` 一載入就把空白的必填欄位標成錯誤；不排除滑桿時，調整滑桿也會套上欄位的驗證邊框或底色（引用："avoiding the hostile default of flagging required-empty fields as errors on page load."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：註冊頁一打開整排欄位就是紅框；拖一下音量滑桿，它也被套上綠色的「有效」邊框。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 4 個糾錯提醒未拆：文字對比至少 4.5:1（大字 3:1）、非文字 3:1；`<textarea>` 不要 `resize: none` 而沒有其他調整方式；不要用 `<input type="button|submit|reset">`，改用 `<button>`；捲軸拇指與軌道對比至少 3:1
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
