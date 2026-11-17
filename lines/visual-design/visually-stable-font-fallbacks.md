---
guide: visually-stable-font-fallbacks
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/visually-stable-font-fallbacks.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 視覺穩定的字型退路

%% line-start id="mwg:visually-stable-font-fallbacks" %%
## 用 `font-size-adjust: from-font` 讓退路字型和網頁字型一樣大，換字時不跳
- 做法：在文字容器設 `font-size-adjust: from-font`，讓瀏覽器從首選網頁字型取出 x 高度比例套到退路字型；全大寫標題用 `cap-height from-font`、等寬字用 `ch-width`；也可直接寫數值；封鎖網頁字型驗證版面不動
- 對手：網頁字型載入後取代尺寸不同的退路字型，即使 `font-size` 相同也會造成版面位移，x 高度差太多時文字還難以辨讀（引用："This causes "layout shift" (Cumulative Layout Shift) and can make text illegible if the fallback's lowercase letters (x-height) are significantly different than the preferred font."）
- 退路：保住主要行為——退回 `@font-face` 的 `size-adjust` 等描述子仍能穩定退路字型，但需逐一計算
- 解鎖：設 `font-size-adjust: from-font` 即可自動依首選字型比例縮放退路字型，消除換字位移

經過：文章頁先用 Arial 顯示，網頁字型一到，整段字變小、段落往上縮，讀者剛看到的那行跑掉了。加上 from-font，Arial 先被縮放成網頁字型的大小，換字時幾乎看不出來。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：font-size-adjust：Baseline Newly available（2024-07-25 起），Supported by: Chrome 127, Edge 127, Firefox 118, Safari 17
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前要壓掉換字跳動，得為每個退路字型逐一算 `size-adjust` 與上下伸部覆寫 → 現在新聞站、部落格、多語系文件可以放心用網頁字型，一行宣告就讓任何退路字型和它等大，Core Web Vitals 的 CLS 不再被字型拖累
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
