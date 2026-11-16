---
guide: fluid-scaling
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/fluid-scaling.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 流體縮放

%% line-start id="mwg:fluid-scaling" %%
## 用容器查詢單位做流體縮放，不跟視窗寬度走
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在外層設 `container-type: inline-size`，元件內的字級、內距用 `cqi`／`cqb`，再用 `clamp()` 夾住範圍
- 被什麼擋：用視窗單位做流體縮放，元件是照螢幕寬度、而不是照自己的寬度縮放（引用："This fallback ensures that the text still scales, but it will be based on the screen width rather than the component's width."）
- 戰報：勝——container queries（size）已 Widely，元件放在哪裡都依容器寬度縮放（官方宣稱）

經過：同一張卡片放在主欄和側欄，視窗寬度一樣，可用寬度卻差很多，vw 字級在側欄就顯得過大。容器單位不需要寫 `@container` 規則，會自動對最近的容器解析。和 form-factor-adaptation 的「用容器查詢排元件」同一個對手。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Container queries（size）：Widely（2023-02-14）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:fluid-scaling:2" %%
## 流體字級的上限不超過下限的 2.5 倍，縮放時容器不能跟著變小
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`clamp()` 的最大值不超過最小值的 2.5 倍；瀏覽器放大時不讓容器變窄
- 被什麼擋：用 `clamp()` 夾住流體字級，會影響使用者縮放或調整基準字級的能力（引用："This impacts the user's ability to zoom or adjust their base font size."）
- 戰報：勝——遵守比例上限，文字可放大到 200%，符合 WCAG 1.4.4（官方宣稱）

經過：流體字級被 `clamp()` 夾住、又跟著容器寬度走，使用者放大時字級未必跟著變大。指南給了兩條規則：上下限比例不超過 2.5 倍，以及瀏覽器放大時不要讓容器變小，目的是讓文字能放大到 200%。指南只給規則，沒有示範如何驗證。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：Container queries（size）：Widely（2023-02-14）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
