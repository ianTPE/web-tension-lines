---
guide: precise-text-alignment
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/precise-text-alignment.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 精準的文字對齊

%% line-start id="mwg:precise-text-alignment" %%
## 用 `text-box: trim-both cap alphabetic` 修掉字型內建的上下留白
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在包含文字的元素上（它不繼承）設 `text-box: trim-both cap alphabetic`；只對齊頂端時用 `trim-start cap alphabetic`，兩個邊緣都要寫；用在標題、按鈕、標籤，不用在長篇內文
- 被什麼擋：字型的行高與上下伸部留白讓文字看起來比圖示高或低、按鈕上下內距不等、標題無法和旁邊圖片頂端切齊，只能靠負邊距的魔術數字（引用："Text appears visually lower or higher than an adjacent icon even when using `align-items: center`."）
- 戰報：部分改善——元素的盒子貼合大寫字高與基線，`align-items: center` 和 `padding` 都以看得見的字為準；Chrome、Edge、Safari 支援，Firefox 保留預設留白（官方宣稱）

經過：按鈕裡的圖示和文字明明垂直置中了，文字卻總是偏下一兩像素，換個字型又偏到另一邊。修掉留白後，置中就是看起來的置中。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：text-box：Limited availability，Supported by: Chrome 133, Edge 133, Safari 18.2；Unsupported in: Firefox
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前設計稿的「文字到邊框 12px」要依字型調負邊距 → 現在設計系統的徽章、按鈕、標籤可以直接把設計稿的間距寫進 CSS，換字型也不必重調。Firefox 尚未支援
- 另有 2 個糾錯提醒未拆：小寫字為主時可改用 `ex` 邊緣；多行文字只修第一行上方與最後一行下方，行與行之間仍由 `line-height` 決定
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
