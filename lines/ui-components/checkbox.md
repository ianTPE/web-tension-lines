---
guide: checkbox
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/checkbox.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 核取方塊樣式

%% line-start id="mwg:checkbox" %%
## 用 `accent-color` 或 `appearance: none` 改核取方塊外觀，保留原生 `<input>`
- 做法：簡單換品牌色用 `accent-color`（保留原生繪製、鍵盤、驗證與系統焦點框）；要控制形狀、尺寸與狀態時，在 `<input type="checkbox">` 上設 `appearance: none`，用 `::before` 加 `mask` 畫勾號與 `:indeterminate` 的橫線
- 對手：指南沒說舊做法哪裡壞，只說這兩種做法能保留原生行為或讓 `<input>` 仍是互動目標（引用："This removes the native visual styling while leaving the `<input>` as the interactive target."）
- 退路：保住主要行為——不支援 `accent-color` 時用預設控制項顏色，只失去品牌色
- 解鎖：原生核取方塊可直接換品牌色，或自訂形狀、尺寸與狀態圖示

經過：品牌化的勾選框常被做成 div 加圖示。現在一行 accent-color 就換色，要更大膽的造型也能直接在 input 上畫，鍵盤、表單、讀屏都不用另外補。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：accent-color：Limited availability，Supported by: Chrome 93, Edge 93, Firefox 92, Safari 26.2（指南標 Limited 但列出四大瀏覽器，同 `mwg:brand-consistent-forms`）；Masks：Widely
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前品牌化勾選框得自製元件 → 現在待辦清單、權限設定、批次選取的「全選（部分）」狀態都能用原生 input 做出設計稿的樣子，indeterminate 也有對應圖示
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:checkbox:2" %%
## Safari 的 `accent-color` 不一定保證勾號對比，要實測
- 做法：在 Safari 的淺色與深色配色下測試重要的 accent-color 組合，勾選與部分勾選狀態維持至少 3:1 對比
- 對手：Safari 可能固定用白（淺色）或黑（深色）勾號、改的是背後的強調色，不一定對每個顏色都有足夠對比（引用："This adjustment does not always provide sufficient contrast for every supplied color"）
- 退路：保住主要行為——不支援 `accent-color` 時用預設顏色，核取方塊仍可操作
- 解鎖：（缺）

經過：品牌黃在 Chrome 上配黑勾很清楚，到 Safari 變成白勾，幾乎看不出有沒有勾。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：accent-color：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:checkbox:3" %%
## `appearance: none` 之後要自己給尺寸
- 做法：用相對單位設 `--checkbox-size`、`--checkbox-icon-size`，圖示比方框小
- 對手：`appearance: none` 連瀏覽器預設尺寸一起拿掉（引用："`appearance: none` removes the browser’s default dimensions."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：拿掉原生外觀後，勾選框縮成一個看不見的點。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：appearance：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：`:indeterminate` 要與勾選、未勾選明顯不同；不要 `outline: none`；標籤點擊區至少 44×44px
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
