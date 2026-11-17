---
guide: branded-select-styling
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/branded-select-styling.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 品牌化的下拉選單

%% line-start id="mwg:branded-select-styling" %%
## 用 appearance: base-select 做品牌下拉選單，不用 JS 從零重做
- 做法：`<select>` 與 `::picker(select)` 設 `appearance: base-select`，用內含 `<selectedcontent>` 的 `<button>` 當觸發鈕，再以 `::picker(select)`、`::picker-icon`、`option::checkmark` 分別設計選單、箭頭與勾號
- 對手：以前要做完全品牌化的下拉選單，得用 JavaScript 從零重做，常常弄壞可及性、鍵盤操作與原生表單整合（引用："Previously, achieving a fully branded select required rebuilding the control from scratch with JavaScript, which often broke accessibility, keyboard navigation, and native form integration."）
- 退路：保住主要行為——退回作業系統的下拉選單，選單功能與表單送出照常，只是外觀不是品牌樣式
- 解鎖：以前品牌化下拉得用 JavaScript 重做；現在 `base-select` 讓外觀由 CSS 決定、行為仍是原生的

經過：設計系統要求下拉選單和其他控制項一樣是虛線框、等寬字，原生 `<select>` 改不動，只好換成自製元件，結果鍵盤上下鍵、讀屏、表單送出一項項要自己補。`base-select` 讓外觀全由 CSS 決定，行為仍是原生的。代價是在 iOS 上不再有系統的滾輪選擇器。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Customizable <select>：Limited（Supported by: Chrome 135 (Apr 2025), Edge 135 (Apr 2025), and Safari 27 (Sep 2026). Unsupported in: Firefox.）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前品牌化的下拉選單等於自己寫一個 listbox 元件 → 表單裡的每個下拉都能用純 CSS 做成設計系統的樣子，鍵盤、讀屏、表單送出不用另外處理。Firefox 退回系統選單
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

未拆：picker 畫在 top layer、「z-index 衝突成為過去」只有一句帶過，沒有描述衝突的可觀察現象；開啟 `base-select` 會失去 iOS 原生滾輪選擇器、自訂顏色須自行確保 3:1 對比、寬度不再依最長選項計算，這三點是使用新做法的注意事項，不是新做法對付的對手。
