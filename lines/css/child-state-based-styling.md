---
guide: child-state-based-styling
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/child-state-based-styling.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依子元素狀態設定樣式

%% line-start id="mwg:child-state-based-styling" %%
## 用 :has() 讓容器反應子元素狀態，不用 JS 切 class
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在容器上用 `:has()` 搭配狀態偽類（`:checked`、`:invalid`、`:focus`…），例如 `.theme-card:has(.theme-toggle:checked)` 改寫容器的自訂屬性
- 被什麼擋：（缺）只說不再需要 JS 在父元素切換 `.is-active`、`.has-error` 這類修飾 class，沒說手寫切換在哪個時刻出錯（引用："without needing JavaScript to toggle "modifier" classes (like `.is-active` or `.has-error`) on parent elements."）
- 戰報：勝——`:has()` 已 Widely，容器樣式直接由子元素狀態決定（官方宣稱）

經過：CSS 選擇器過去只能往下選，父層要跟著子元素變就得靠事件監聽加 class。`:has()` 讓表單群組高亮錯誤、卡片在子連結聚焦時浮起都能純 CSS 完成。指南提醒要把 `:has()` 限縮在最近的元件容器，別掛在 `body` 上，以免觸發大範圍重算。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：:has()：Widely（2023-12-19）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
