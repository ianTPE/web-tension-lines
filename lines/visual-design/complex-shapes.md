---
guide: complex-shapes
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/complex-shapes.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 複雜形狀

%% line-start id="mwg:complex-shapes" %%
## 筆刷、有機紋理這類形狀用 `mask-image`，不用只有硬邊的 `clip-path`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`mask-image` 指向帶透明度的 PNG／SVG、CSS 漸層，或頁內 SVG 的 `<mask>`（`maskContentUnits="objectBoundingBox"` 讓遮罩隨元素縮放），並同時寫 `-webkit-mask-*`；SVG 遮罩預設看亮度，要看透明度時設 `mask-type: alpha`
- 被什麼擋：`clip-path` 只能切出幾何或向量形狀，做不出半透明、柔邊與複雜紋理（引用："it supports semi-transparency, allowing for soft edges and complex textures that are difficult or impossible to achieve with `clip-path`."）
- 戰報：勝——元素可以用任意灰階或透明度的圖決定可見範圍；Masks 為 Widely，不支援時顯示為一般矩形（官方宣稱）

經過：想讓主視覺照片的邊緣像水彩刷過一樣漸漸淡掉，`clip-path` 切出來只能是一條銳利的邊。改用遮罩圖，邊緣就有了筆觸。
%% line-end %%

### 細節（不索引）
- 對手組：裁切只有硬邊
- 支援狀態：Masks：Baseline Widely available（2023-12-07 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：不支援遮罩時確認內容在矩形下仍可讀，可用 `@supports` 給一個 `clip-path: inset(… round …)` 的簡單形狀
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
