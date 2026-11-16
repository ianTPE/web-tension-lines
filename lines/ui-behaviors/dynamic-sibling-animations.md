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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`animation-delay: calc(sibling-index() * var(--stagger-time))`，每個項目依在父層中的位置延遲；減少動態偏好下關掉動畫；舊瀏覽器先寫一條用 JS 設的 `--sibling-index` 的宣告當退路
- 被什麼擋：指南只描述錯開動畫的效果，沒說舊做法（逐個 `:nth-child` 或 JS 設延遲）在哪個時刻出問題（引用："multiple ordered elements animate sequentially with a slight delay between each, rather than all animating at once"）
- 戰報：部分改善——純 CSS 依位置算出延遲；`sibling-index()` 為 Newly，舊瀏覽器需用 JS 寫入自訂屬性退路（官方宣稱）

經過：錯開動畫的延遲以前得靠 JS 或一長串 nth-child 給。現在 CSS 自己知道「我是第幾個」，項目增減不必重算。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：sibling-count() and sibling-index()：Newly（2026-08-18），Supported by: Chrome 138, Edge 138, Firefox 154, Safari 26.2
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前錯開進場要 JS 逐個設延遲 → 現在搜尋結果、通知列表、儀表板卡片可以純 CSS 一張接一張浮現，資料筆數變了也自動對齊
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
