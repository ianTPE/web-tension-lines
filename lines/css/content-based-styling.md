---
guide: content-based-styling
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/content-based-styling.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依內容設定樣式

%% line-start id="mwg:content-based-styling" %%
## 用 :has() 依有沒有某個子元素切換版面
- 做法：在元件容器上用 `:has(img)` 切換成並排版面，用 `:not(:has(img))` 指定沒有圖片時的樣式
- 對手：（缺）只說過去要用 JS 或模板條件注入 `.card--has-image` 之類的修飾 class，沒說那樣做在哪個時刻出錯（引用："Historically, applying different layouts to a component based on its content required either JavaScript or conditional logic in your HTML templating language to inject modifier classes"）
- 退路：不需要——`:has()` 已 Widely，不必退路
- 解鎖：容器可直接依子內容有無切換 CSS 版面，不必注入修飾 class

經過：同一個卡片元件有圖、沒圖要兩種排法，以往得讓產生 HTML 的那一端先知道內容再加 class。`:has()` 讓樣式表自己看內容。需要 fallback 時，指南建議由伺服器端模板加 class，因為內容在算繪時就知道了。
%% line-end %%

### 細節（不索引）
- 對手組：用JS補樣式狀態
- 支援狀態：:has()：Widely（2023-12-19）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
