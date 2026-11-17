---
guide: customize-scrollbar-color-and-thickness
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/customize-scrollbar-color-and-thickness.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 自訂捲軸顏色與粗細

%% line-start id="mwg:customize-scrollbar-color-and-thickness" %%
## 用標準的 `scrollbar-color` 換捲軸配色，拇指對軌道與底下背景都要有 3:1
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在捲動容器上設 `scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)` 與 `scrollbar-width`，拇指與軌道顏色各放一個變數
- 被什麼擋：拇指對比不足時使用者看不到它、也看不出捲了多遠；macOS 覆蓋式捲軸的軌道透明，拇指得對容器背景也有對比（引用："so users can see the thumb and how far they've scrolled (WCAG 1.4.11 Non-text Contrast)."）
- 戰報：部分改善——標準屬性就能換顏色與粗細；scrollbar-color 為 Newly，需要時以 `@supports not` 包住 `::-webkit-scrollbar` 退路（官方宣稱）

經過：深色側欄配上淡灰捲軸，在 Mac 上軌道透明，拇指和背景幾乎同色，使用者不知道清單還有下半段。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：scrollbar-color：Baseline Newly available（2025-12-12 起）；scrollbar-width：Newly（2024-12-11 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前捲軸配色要寫非標準偽元素、各家分開處理 → 現在聊天側欄、程式碼面板、深色儀表板的捲軸都能兩行標準 CSS 配進主題，變數一換全站跟著換
- 另有 1 個糾錯提醒未拆：舊式退路包在 `@supports not (scrollbar-color: auto)` 裡，避免兩套同時生效衝突
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
