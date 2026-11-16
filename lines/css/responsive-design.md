---
guide: responsive-design
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/responsive-design.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 響應式設計

%% line-start id="mwg:responsive-design" %%
## 用 dvh／dvw 取代 vh／vw，網址列出現或收起時版面不壞
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：版面高度、寬度改用動態視窗單位 `dvh`、`dvw`，取代 `vh`、`vw`
- 被什麼擋：行動瀏覽器的網址列等介面出現或收起時，用 `vh`／`vw` 的版面會壞掉（引用："to prevent layout breakage when mobile browser UI elements (like address bars) appear or disappear."）
- 戰報：勝——動態視窗單位跟著實際可見區域變化，版面不再因網址列伸縮而壞（官方宣稱）

經過：滿版區塊用 `100vh` 排，手機上網址列一出現或一收起，可見高度就變了，版面跟著破。指南只用一句話帶過，要的是改用會跟著瀏覽器介面變動的動態單位；具體壞成什麼樣子，指南沒有展開。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:responsive-design:2" %%
## 用 aspect-ratio 替圖片、影片先留位置
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `<img>`、`<video>` 等媒體元素上設 `aspect-ratio`，載入前就保留對應的高度
- 被什麼擋：媒體載入前沒有預留空間，載入後把下方內容推開，造成累積版面位移（引用："to reserve space during loading and prevent Cumulative Layout Shift (CLS)."）
- 戰報：勝——比例先決定了尺寸，資源載入前後版面不動（官方宣稱）

經過：讀者正在看的段落，因為上方圖片剛下載完而突然往下跳。先宣告比例，瀏覽器在圖片抵達前就知道要留多大的位置。這一點與 css-layout 指南的第二條是同一件事。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:responsive-design:3" %%
## 流體字級用 clamp() 混合 vw 與 rem，且上限不超過下限 2.5 倍
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：字級寫成 `clamp(2rem, 1rem + 5vw, 4rem)` 這種形式，上下限用字級相對單位，且最大值不超過最小值的 2.5 倍；不單獨用 `vw` 當字級
- 被什麼擋：視窗單位不會隨使用者縮放而變大，只用 `vw` 的字級在極端螢幕上太小或太大，放大頁面時文字也不跟著放大（引用："Viewport units don't grow when users zoom"）
- 戰報：勝——上限不超過下限 2.5 倍時，瀏覽器縮放到 500% 仍能讓文字放大到 200%，符合 WCAG 1.4.4（官方宣稱）

經過：標題用 `5vw`，在超寬螢幕上大得誇張，在小手機上小到看不清；低視力使用者按放大，字也幾乎不動，因為 `vw` 只看視窗寬度。混入 `rem` 並夾在兩個字級相對的界限之間，文字才會回應縮放。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

未拆：開頭「用 `@container` 讓元件依容器而非視窗調整」只是指向 size-aware-styling 指南，已在那裡拆（`mwg:size-aware-styling`）。
