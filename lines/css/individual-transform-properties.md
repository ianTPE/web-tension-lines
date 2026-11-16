---
guide: individual-transform-properties
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/individual-transform-properties.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 個別 transform 屬性

%% line-start id="mwg:individual-transform-properties" %%
## 用 translate／rotate／scale 各自動畫，不重寫整串 transform
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用獨立的 `translate`、`rotate`、`scale` 屬性，hover 或 transition 只改其中一項
- 被什麼擋：`transform` 要改其中一個變換就得重寫整條變換鏈，所以很難只動畫單一變換；hover 改 `transform` 會把正在跑的位移動畫蓋掉（引用："any changes to a single transformation require re-specifying the entire transformation chain. This makes it tricky to animate or transition a single transformation."）
- 戰報：勝——已 Widely；不同屬性的動畫與過渡互不覆蓋，例如 hover 只改 `scale`，`translate` 的漂浮動畫照常進行（官方宣稱）

經過：卡片一邊上下漂浮、一邊 hover 放大，用 `transform` 寫的話兩者搶同一個屬性。拆成獨立屬性後各走各的。代價是套用順序固定為 translate → rotate → scale → transform，要不同順序仍得用 `transform`；兩者還會疊加，`scale: 2; transform: scale(3)` 結果是 6 倍。
%% line-end %%

### 細節（不索引）
- 對手組：簡寫或屬性連動重設
- 支援狀態：Individual transform properties：Widely（2022-08-05）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有（「tricky」本身是標籤，但「得重寫整條變換鏈」與範例中「不互相覆蓋」指到了可觀察的現象）／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:individual-transform-properties:2" %%
## 會變換的元素先給恆等變換，避免 hover 時堆疊脈絡突變
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：狀態改變時可能被變換的元素，基礎狀態就先設 `translate: 0px; rotate: 0deg; scale: 1;`
- 被什麼擋：只在 hover 時才套變換，會在那一刻建立新的堆疊脈絡，造成意外的版面或 z-index 位移，也會影響錨點定位（引用："This prevents unexpected layout or z-index shifts caused by creating a new stacking context only on hover."）
- 戰報：勝——基礎狀態就有堆疊脈絡與包含區塊，hover 前後不變（官方宣稱）

經過：滑鼠移上去，元素突然跑到別的元素上面或下面，或固定定位的子元素換了參考框。原因是變換會建立堆疊脈絡與包含區塊，只在 hover 時才有就會突變。恆等變換讓它從一開始就存在。
%% line-end %%

### 細節（不索引）
- 對手組：堆疊脈絡改變層級
- 支援狀態：Individual transform properties：Widely（2022-08-05）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
