---
guide: shaped-cutouts
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/shaped-cutouts.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 造型挖空

%% line-start id="mwg:shaped-cutouts" %%
## 有文字的卡片把遮罩套在旁邊的裝飾元素上，不套在文字容器上
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：卡片拆成不加遮罩的 `.card-body`（放文字）和空的 `.card-accent`（套 SVG `mask-image`，`maskContentUnits="objectBoundingBox"`），兩者同底色拼成一張造型卡；父層用 `filter: drop-shadow()` 讓陰影沿合併後的輪廓走。沒有文字的頭像、插圖才直接遮罩，簡單缺口用 `radial-gradient` 遮罩
- 被什麼擋：直接對含文字的元素套遮罩可能把文字切掉（引用："Apply the mask to an adjacent element rather than the parent element containing text. This ensures that text doesn't get clipped and remains readable."）
- 戰報：勝——文字容器維持矩形、完整可讀；Masks 為 Widely，不支援時裝飾元素是同色矩形，整張卡退成乾淨的長方形（官方宣稱）

經過：會員卡右側要有一道內凹弧線，整張卡套遮罩後，文字換行到右邊時被弧線吃掉一截。把弧線移到旁邊的空 div 上，文字就安全了。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：Masks：Baseline Widely available（2023-12-07 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：SVG 遮罩的挖空路徑要延伸超出邊界（例如到 x=1.1），避免邊緣留下次像素細線
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
