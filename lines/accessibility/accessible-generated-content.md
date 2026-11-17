---
guide: accessible-generated-content
category: accessibility
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/accessibility/accessible-generated-content.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 無障礙的 CSS 產生內容

%% line-start id="mwg:accessible-generated-content" %%
## 用 content 的替代文字參數讓裝飾符號閉嘴
- 做法：在 `content` 用 `/` 加替代文字：裝飾文字寫 `content: " →" / "";`，有意義的圖示寫 `content: url(icon.svg) / "Save";`
- 對手：沒有 `/` 語法時，`::after` 插入的裝飾符號會被讀屏照唸（引用："Fallback: render the glyph in browsers without `/` support (screen readers there will still announce it)"）
- 退路：失去主要好處——退回單值 `content` 時符號照樣顯示，但讀屏那邊仍會照唸，雜音又回來了
- 解鎖：以前 CSS 插入的內容沒辦法指定讀屏要念什麼，現在可以在 `content` 的替代文字參數裡宣告有意義的圖示念什麼、純裝飾的不念

經過：箭頭、分隔點這類用 CSS 加的裝飾，在讀屏裡會變成「right arrow」之類的雜音。新語法讓 CSS 自己宣告「這個不要唸」或「這個唸成什麼」。指南同時強調這只是減害：有意義的文字仍然要放在 DOM 裡。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：Alt text for generated content：Newly（2024-07-09；Chrome 77、Edge 79、Firefox 128、Safari 17.4）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：用 CSS 插入的箭頭、分隔符、狀態圖示可以直接在樣式表裡宣告「不唸」或「唸成某句話」，不必為每個圖示多包一個 `aria-hidden` 的 span。圖示系統可以全放在 CSS 裡而不製造讀屏雜音
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:accessible-generated-content:2" %%
## DOM 裡已經有的字，不要再寫進 content 的替代文字
- 做法：替代文字參數只在文字和主要值不同、且 DOM 裡還沒有時使用
- 對手：按鈕文字是「Save」，又在 `::before` 的圖示寫 `/ "Save"`，讀屏唸成「Save save」（引用："A screen reader would read it out as "Save save"."）
- 退路：保住主要行為——退回單值 `content` 時圖示照樣顯示但沒有替代文字，不會跟按鈕文字重複播報
- 解鎖：（缺）

經過：新語法容易被當成「每個圖示都該補 alt」，結果和按鈕本身的文字疊在一起。指南也說圖片本來就預設為裝飾，不要再寫空字串；emoji 的替代文字只在和官方名稱不同時才寫。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：Alt text for generated content：Newly（2024-07-09）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯（新功能的誤用，不產生新應用）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
