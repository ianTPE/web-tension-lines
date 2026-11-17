---
guide: contrast-color
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/contrast-color.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 背景色動態變化時確保文字可讀

%% line-start id="mwg:contrast-color" %%
## 用 `contrast-color()` 依背景色自動選黑或白文字，擋掉換主題後字看不見
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`color: contrast-color(var(--badge-bg))`，背景與文字共用同一個變數；主題、使用者自訂色都只改那個變數；不支援時用相對色彩語法在 `xyz-d65` 空間以亮度門檻 0.17913 算出黑或白
- 被什麼擋：背景是動態的，卻為每個狀態寫死文字顏色，文字色和背景就會對不上（引用："Hard-code a separate text color for each interaction state when the background is dynamic. Doing so reintroduces the very mismatch `contrast-color()` exists to prevent."）
- 戰報：部分改善——瀏覽器在黑白之間選出對比最大者，主題一換文字跟著換；contrast-color() 為 Newly，退路的 `color(xyz)` 計算以 Newly 的相對色彩語法達到 WCAG 1.4.3（官方宣稱）

經過：使用者把標籤顏色選成淡黃色，標籤上的白字就看不見了。現在文字顏色從背景算出來，選什麼顏色都讀得到。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：contrast-color()：Baseline Newly available（2026-04-10 起），Supported by: Chrome 147, Edge 147, Firefox 146, Safari 26；Relative colors：Newly（2024-09-16 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前讓使用者自選顏色，就得在 JS 裡算亮度再決定字色 → 現在專案標籤、看板欄位、行事曆分類、使用者自訂主題都能開放任意顏色，文字自動黑或白
- 另有 2 個糾錯提醒未拆：`contrast-color()` 只用在前景（文字、邊框），不要拿來算 `background-color`；其他退路（文字描邊、`paint-order`、半透明遮罩、文字陰影、SVG 濾鏡）各有外觀代價
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
