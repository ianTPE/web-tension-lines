---
guide: physics-based-easing
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/physics-based-easing.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 物理感緩動

%% line-start id="mwg:physics-based-easing" %%
## 用 `linear()` 多停點緩動做出彈簧與彈跳
- 做法：用工具把 JS 緩動函式或 SVG 路徑轉成 `linear(0, 0.016 0.5%, …, 1)`，存成 `--spring-easing` 之類的自訂屬性，套在 `transition`／`animation` 上並自己給時長
- 對手：`ease-in`、`cubic-bezier()` 只能畫簡單曲線，做不出彈跳或彈簧這類物理效果（引用："making it impossible to create complex physics-based effects like bounces or springs"）
- 退路：不需要——linear() 已廣泛支援，舊瀏覽器可先寫 ease-out 覆寫退路或於極需物理感時改用 JS 動畫庫
- 解鎖：（缺）

經過：會超過目標再彈回來的動作，以前只能交給 JS 動畫函式庫。現在曲線可以用一串點描出來，CSS 自己就能跑。
%% line-end %%

### 細節（不索引）
- 對手組：動畫曲線只有簡單形狀
- 支援狀態：linear() easing：Widely（2023-12-11 起 Baseline），Supported by: Chrome 113, Edge 113, Firefox 112, Safari 17.2
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:physics-based-easing:2" %%
## 彈跳緩動不要套在 `opacity` 上
- 做法：會超出 0–1 的彈跳曲線只套在 `transform`／`scale` 這類屬性上，不套 `opacity`
- 對手：值超出 0 以下或 1 以上時，`opacity` 會出現刺眼的閃爍（引用："can cause visually jarring flickering if the value overshoots below 0 or above 1"）
- 退路：不需要——linear() 已廣泛支援，不套用在 opacity 上即可在所有瀏覽器避開超界閃爍
- 解鎖：（缺）

經過：彈簧的精髓是「超過一點再回來」，透明度超過 1 沒有意義，只會變成閃一下。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：linear() easing：Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：`linear()` 不會自己算時長，一定要寫 duration；減少動態偏好下關掉或減弱
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
