---
guide: visually-texture-content
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/visually-texture-content.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 為內容加上視覺質感

%% line-start id="mwg:visually-texture-content" %%
## 用 `mask-image` 紋理讓內容本身斑駁，而不是蓋一層紋理圖
- 做法：`mask-image` 指向可重複的紋理圖（`mask-repeat: repeat`、`mask-size` 控制比例），或用 CSS 漸層組出幾何圖樣，同時寫 `-webkit-mask-*`；注意來源決定模式：頁內 SVG `<mask>` 預設看亮度，圖檔與漸層預設看透明度，要改用 `mask-mode`
- 對手：把紋理當背景或疊層貼上去，只是蓋在內容上面或後面，內容自己的透明度不變，底下的背景透不出來（引用："You can use a background image or an overlay as a fallback to simulate the texture, although it will not affect the transparency of the content itself."）
- 退路：不需要——遮罩功能已 Widely，不必另設退路
- 解鎖：（缺）

經過：復古海報風的標題要有印刷磨損感，疊一張髒污 PNG 在上面，磨損處卻是白點而不是透出底下的牛皮紙。換成遮罩後，磨掉的地方真的變透明。
%% line-end %%

### 細節（不索引）
- 對手組：手工重現瀏覽器渲染
- 支援狀態：Masks：Baseline Widely available（2023-12-07 起）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
