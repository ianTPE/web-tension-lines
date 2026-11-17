---
guide: dynamic-sibling-styling
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/dynamic-sibling-styling.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依兄弟數量與序號設定樣式

%% line-start id="mwg:dynamic-sibling-styling" %%
## 用 sibling-index() 與 sibling-count() 讓每個項目自己算樣式
- 做法：在 `calc()` 裡用 `sibling-index()`、`sibling-count()` 算出每個兄弟元素的色相、旋轉角度或圓周位置（可搭配 `sin()`／`cos()`）
- 對手：（缺）只說過去要寫複雜的 `:nth-child` 迴圈或用 JS 注入行內樣式，沒說那樣做在哪個時刻出錯（引用："Historically, applying unique styles to each sibling in a list required complex `:nth-child` loops or JavaScript to inject inline styles."）
- 退路：保住主要行為——不支援時用 JS 注入序號與總數自訂屬性，保留動態樣式
- 解鎖：CSS 可直接取得兄弟序號與總數，項目增減時自動重算樣式

經過：色譜、扇形展開、環狀排列都需要「我是第幾個、總共幾個」。新函式讓這兩個數字直接進 CSS，項目增減時版面自動跟著算。指南要求 fallback 注入的序號從 1 開始，才能和原生函式一致。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：sibling-count()／sibling-index()：Newly（2026-08-18；Chrome 138、Edge 138、Firefox 154、Safari 26.2）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：項目數量不固定的視覺化可以純 CSS 排：環狀選單、扇形展開的手牌、依數量自動分色的標籤雲，新增或刪除項目時位置和顏色自己重算，不必寫 JS 迴圈
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
