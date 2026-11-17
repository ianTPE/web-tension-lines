---
guide: color
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/color.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 色彩

%% line-start id="mwg:color" %%
## 邊框、分隔線與狀態不要只靠背景圖、陰影或 `border-image`，強制色彩下會消失
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `@media (forced-colors: active)` 裡為色彩 token 定義系統色退路，用 `outline` 或 `border` 配 `CanvasText`、`LinkText`、`Highlight` 等關鍵字表達邊界與狀態；`forced-color-adjust: none` 只留給顏色本身就是資訊的地方（語法上色、色票），而且要自己給一組合格的文字與背景色
- 被什麼擋：強制色彩模式會覆蓋作者顏色、移除 `box-shadow` 與漸層背景，`border-image` 與 `url()` 背景可能消失或保留原色而失去對比（引用："In forced colors they disappear or keep their own colors, which may not contrast with the system colors (and they often disappear in print too)."）
- 戰報：勝——邊界與狀態改用系統色畫出，高對比模式與列印都看得到（官方宣稱）

經過：用內陰影畫的輸入框邊線，在 Windows 高對比模式下整個不見，使用者找不到要在哪裡打字。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:color:2" %%
## 動態產生深淺色不要只改 oklch 的亮度，改用 `color-mix()` 或兩者混用
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：先找現成的設計 token；真要動態產生時用 `color-mix(in oklab, …, white/black)`，或把亮度調整（不超過 30%）和 `color-mix()` 混合使用
- 被什麼擋：瀏覽器還沒實作色域映射，直接改 `oklch`／`oklab` 的亮度得到的顏色無法預期（引用："browsers do not yet implement gamut mapping, so the resulting color is unpredictable."）
- 戰報：部分改善——`color-mix()` 讓顏色留在色域內，但容易過度去飽和、偏灰；兩者混用取平衡（官方宣稱）

經過：用相對色彩語法把品牌藍的亮度拉到 0.9，在不同螢幕上出來的顏色各不相同，有的還偏紫。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：指南本篇未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：不要只用顏色表示元件或狀態（成功／錯誤要有圖示或文字）；文字 4.5:1、大字與圖示 3:1、元件邊界與狀態 3:1；`prefers-contrast: more` 只能加強已達標的顏色，因為它只觸及開了設定的人，修不了不及格的預設
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
