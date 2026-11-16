---
guide: design-token-reactivity
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/design-token-reactivity.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 會反應的設計 token

%% line-start id="mwg:design-token-reactivity" %%
## 用 container style queries 讓高階 token 直接寫在 CSS 裡
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在容器上設 `--density: compact` 這類自訂屬性，後代用 `@container style(--density: compact)` 套用對應樣式
- 被什麼擋：改用 `data-density` 屬性加選擇器時，同層級的選擇器特異度相同，巢狀的密度區塊無法正確覆寫，永遠由出現順序決定（引用："A major limitation of this fallback approach is that it does not support nesting elements with the `data-density` attribute set, since the selector specificity is the same, order of appearance will be used to determine the styles"）
- 戰報：部分改善——container style queries 已 Newly（2026-05-19）；指南不建議把它用在必須所有瀏覽器都可用的核心功能上，核心功能仍要用選擇器版本，也就保留了巢狀的限制（官方宣稱）

經過：密度、強調程度這類「高階 token」以往只能編成 class 命名慣例，或交給 JS 框架的 props／context。style query 查的是祖先的計算值，所以 token 可以留在樣式表裡。指南沒有明說 style query 能解決巢狀問題，這點是從「這是 fallback 的主要限制」反推的。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：Container style queries：Newly（2026-05-19；Chrome 111、Edge 111、Firefox 151、Safari 18）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：在任何祖先上設一個 `--density` 或 `--tone`，底下所有元件自動切換緊湊／寬鬆或強調樣式，而且可以一層套一層。適合「使用者可調密度」的資料表或後台介面，不必經過框架的 context 傳遞
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
