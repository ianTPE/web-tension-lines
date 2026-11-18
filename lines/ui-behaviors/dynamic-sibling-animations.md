---
guide: dynamic-sibling-animations
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/dynamic-sibling-animations.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 製作錯開動畫

%% line-start id="mwg:dynamic-sibling-animations" %%
## 用 `sibling-index()` 讓清單項目依序錯開進場
- 做法：`animation-delay: calc(sibling-index() * var(--stagger-time))`，每個項目依在父層中的位置延遲；減少動態偏好下關掉動畫；舊瀏覽器用 JS 設的 `--sibling-index` 當基本宣告，`sibling-index()` 那條包進以字面時間值偵測的 `@supports`
- 對手：指南只描述錯開動畫的效果，沒說舊做法（逐個 `:nth-child` 或 JS 設延遲）在哪個時刻出問題（引用："multiple ordered elements animate sequentially with a slight delay between each, rather than all animating at once"）
- 退路：保住主要行為——不支援時由 JS 寫入 --sibling-index、sibling-index() 包進 @supports，舊瀏覽器仍能錯開進場
- 解鎖：只寫純 CSS 就能讓清單或選單項目依序錯開進場，項目數量變動時也不必手動重算延遲

經過：錯開動畫的延遲以前得靠 JS 或一長串 nth-child 給。現在 CSS 自己知道「我是第幾個」，項目增減不必重算。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：sibling-count() and sibling-index()：Newly（2026-08-18），Supported by: Chrome 138, Edge 138, Firefox 154, Safari 26.2
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前錯開進場要 JS 逐個設延遲 → 現在搜尋結果、通知列表、儀表板卡片可以純 CSS 一張接一張浮現，資料筆數變了也自動對齊
- 退路細節：v1.0.1 起指南明說舊寫法（兩條 `animation-delay` 依序覆蓋、不包 `@supports`）會失效：含 `var()` 的那條在不支援的瀏覽器照樣被接受，計算時才判無效，延遲重設為 `0s`；`@supports` 也不可寫 `var()`，否則永遠為真。不想用 JS 時可把 `:nth-child()` 延遲包進 `@supports not (...)`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18（v1.0.1）上游改寫退路：原本「把退路宣告放前面、不必包 @supports」的做法被指出會讓延遲歸零，做法與退路句隨之更新，退路分類與戰報不變
