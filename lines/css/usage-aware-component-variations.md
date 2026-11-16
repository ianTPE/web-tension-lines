---
guide: usage-aware-component-variations
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/usage-aware-component-variations.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依語意情境切換元件變體

%% line-start id="mwg:usage-aware-component-variations" %%
## 用 style query 讓元件回應情境旗標，不用後代選擇器綁死兩端
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在情境容器上設語意旗標（`--surface: featured`），元件用 `@container style(--surface: featured)` 自行決定要顯示徽章、改成實心按鈕或換排列方向；不設 `container-type`
- 被什麼擋：後代選擇器（`.featured .button`）必須同時寫出兩端，任何一端改變都得改選擇器，也穿不過 shadow DOM 邊界（引用："the selector must encode both sides of the relationship and must change whenever either side does."）
- 戰報：部分改善——container style queries 為 Newly；fallback 用 `:where(.featured)` 選擇器先給預設，支援時由 style query 覆寫，但 fallback 期間元件仍綁在 class 名稱與 DOM 位置上（官方宣稱）

經過：新增一種「精選」區塊，就得回頭在每個會變化的元件選擇器裡補一條；新增一個會變化的元件，又得列出所有精選區塊。改成旗標後，產生情境的一方和回應情境的一方互不點名，各自擴充。只是固定、一次性的關係，指南仍建議用後代選擇器。
%% line-end %%

### 細節（不索引）
- 對手組：樣式規則綁死結構
- 支援狀態：Container style queries：Newly（2026-05-19）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前元件要依所在區塊變化，就得讓選擇器知道所有區塊的名字，web component 內部還碰不到 → 元件庫可以發布「在促銷情境下自動換實心按鈕、亮出徽章」的元件，頁面只要在任何祖先上設 `--surface: featured`，連 shadow DOM 裡的元件都會跟著變
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
