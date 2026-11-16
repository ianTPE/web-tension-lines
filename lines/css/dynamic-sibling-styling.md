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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `calc()` 裡用 `sibling-index()`、`sibling-count()` 算出每個兄弟元素的色相、旋轉角度或圓周位置（可搭配 `sin()`／`cos()`）
- 被什麼擋：（缺）只說過去要寫複雜的 `:nth-child` 迴圈或用 JS 注入行內樣式，沒說那樣做在哪個時刻出錯（引用："Historically, applying unique styles to each sibling in a list required complex `:nth-child` loops or JavaScript to inject inline styles."）
- 戰報：部分改善——已 Newly（2026-08-18）；舊瀏覽器要用 JS 注入 `--sibling-index`／`--sibling-count`，原生函式包在 `@supports` 裡覆寫（官方宣稱）

經過：色譜、扇形展開、環狀排列都需要「我是第幾個、總共幾個」。新函式讓這兩個數字直接進 CSS，項目增減時版面自動跟著算。指南要求 fallback 注入的序號從 1 開始，才能和原生函式一致。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：sibling-count()／sibling-index()：Newly（2026-08-18；Chrome 138、Edge 138、Firefox 154、Safari 26.2）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：項目數量不固定的視覺化可以純 CSS 排：環狀選單、扇形展開的手牌、依數量自動分色的標籤雲，新增或刪除項目時位置和顏色自己重算，不必寫 JS 迴圈
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
