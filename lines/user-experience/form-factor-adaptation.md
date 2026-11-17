---
guide: form-factor-adaptation
category: user-experience
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/user-experience/form-factor-adaptation.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 依裝置形態調整

%% line-start id="mwg:form-factor-adaptation" %%
## 元件版面用 container query，不用視窗寬度
- 做法：元件的版面改用 container query，media query 只用來查輸入裝置與使用者設定
- 對手：用視窗寬度的 media query 排元件，同一個元件放進側欄或窄欄時無法跟著調整（引用："Use container queries instead of viewport-width media queries for component layout, so a component adapts wherever it is placed."）
- 退路：不需要——Size container queries 已廣泛支援，直接用於元件排版即可隨所處容器寬度自適應
- 解鎖：（缺）

經過：同一張卡片放在主欄與側欄，視窗寬度相同、可用寬度卻差很多。指南另提醒在 `inline-size` 容器上查高度是無效的（"it measures only width"）。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Container queries (size)：Widely（2023-02-14）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:form-factor-adaptation:2" %%
## 320px 寬度下文字與控制項都不能被切掉
- 做法：含文字的元素用 `min-block-size` 而不是固定高度，標題不用 ellipsis 截斷，父層不用 `overflow: hidden` 切控制項
- 對手：固定高度、標題截斷與父層裁切，在窄螢幕或放大文字時讓文字或按鈕被切掉（引用："DO NOT truncate headings with `text-overflow: ellipsis`, and do not clip controls with `overflow: hidden` on their parents."）
- 退路：不需要——min-block-size 與折行規範皆已廣泛支援，不截斷標題即可在 320px 視窗完整顯示
- 解鎖：（缺）

經過：WCAG 1.4.10 要求 320px 寬時內容不被裁切。這條和 single-line-overflow 的分工是：標籤可以視覺截斷，標題不行。
%% line-end %%

### 細節（不索引）
- 對手組：截字傷可及性
- 支援狀態：text-wrap: balance：Newly（2024-05-13）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
