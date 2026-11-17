---
guide: breadcrumbs
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/breadcrumbs.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 麵包屑導覽

%% line-start id="mwg:breadcrumbs" %%
## 保留分隔符，讓麵包屑看起來是層級而不是同層
- 做法：用 `<nav>` + `<ol>` 建麵包屑，分隔符由 CSS 產生且對輔助技術隱藏
- 對手：做成膠囊或分段條卻拿掉分隔符，看起來像分頁或篩選器（同層項目），不像層級（引用："Pills, tags and a segmented bar without one look like tabs or filters (items on the same level), not a hierarchy."）
- 退路：不需要——HTML 列表與 CSS 分隔符已 Widely，不必退路
- 解鎖：（缺）

經過：設計上常想讓麵包屑更像按鈕列，結果外觀暗示了錯誤的結構。指南把分隔符當必要元素，並用 `ol` 而不是 `ul` 表達順序。
%% line-end %%

### 細節（不索引）
- 對手組：外觀暗示錯的結構
- 支援狀態：—
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:breadcrumbs:2" %%
## 用 border-shape 讓斜角段落的邊框與焦點框跟著形狀
- 做法：用 `corner-shape`／`border-shape` 畫斜角或箭頭形分段，邊框與焦點外框沿著形狀
- 對手：用 `clip-path` 切形狀會切掉邊框與焦點外框；強制色彩模式又移除背景，被切的段落失去輪廓（引用："`clip-path` clips borders and outlines, so under the fallback use a color/background change plus negative `outline-offset` for focus instead of an outside outline."）
- 退路：失去主要好處——退回 `clip-path`，邊框與焦點外框不再跟著形狀
- 解鎖：`border-shape` 讓不規則形狀的邊框與焦點外框沿形狀呈現

經過：箭頭形麵包屑過去多用 `clip-path`，鍵盤聚焦時外框被切掉，高對比模式下整段消失。新屬性讓邊框本身就是那個形狀，但 Firefox 與 Safari 都還不支援。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：corner-shape：Limited（Chrome/Edge 139）；border-shape：Limited（Chrome/Edge 147）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：斜角、箭頭、缺角這類形狀可以連邊框和焦點框一起跟著形狀走，不必再用 clip-path 切掉可及性。目前僅 Chromium
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
