---
guide: animate-to-intrinsic-sizes
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/animate-to-intrinsic-sizes.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 動畫到固有尺寸

%% line-start id="mwg:animate-to-intrinsic-sizes" %%
## 用 interpolate-size 讓 height: auto 也能過渡
- 做法：在 `:root` 設 `interpolate-size: allow-keywords`，讓 `block-size` 從固定長度過渡到 `auto`／`max-content` 等關鍵字；需要在固有尺寸上做加減時改用 `calc-size()`
- 對手：不支援的瀏覽器裡，尺寸會直接跳到目標值，沒有過渡（引用："Browsers that do not support them will perform an instant jump to the target size."）
- 退路：失去主要好處——不支援時版面與開關照常，但直接跳到目標尺寸，失去過渡動畫
- 解鎖：固定長度與 `auto` 等固有尺寸關鍵字之間可原生過渡

經過：「展開更多」、可關閉的提示框要從 0 長到內容高度，過去只能用 JS 量高度或 `max-height` 硬湊。新屬性讓瀏覽器自己插值，但兩端不能都是關鍵字，至少一端要是長度或百分比。指南也要求收合到 0 後要把元素設 `hidden`，並尊重 `prefers-reduced-motion`。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：interpolate-size：Limited（Chrome 129、Edge 129）；calc-size()：Limited（Chrome 129、Edge 129）；Firefox、Safari 皆不支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：任何「高度隨內容」的區塊（通知、展開說明、可收合側欄）都能用一行 CSS 做平滑展開與收合，不必 JS 量尺寸。適合大量動態內容的儀表板卡片；目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」
