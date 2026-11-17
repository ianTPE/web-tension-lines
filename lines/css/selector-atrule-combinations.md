---
guide: selector-atrule-combinations
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/selector-atrule-combinations.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 組合選擇器與 @ 規則的條件

%% line-start id="mwg:selector-atrule-combinations" %%
## 把「系統偏好或手動切換」的組合條件存進自訂屬性，用 style query 只寫一次規則
- 做法：在 `:root` 依 `@media (prefers-color-scheme)` 與 `:has(meta[name="color-scheme"])`／class 設 `--color-scheme`，各狀態的規則改用 `@container style(--color-scheme: dark)` 與 `not style(...)` 套用
- 對手：（缺）只說直覺寫法會產生重複程式碼——同一組深色規則在 media query 與 `:root.dark` 底下各寫一次——沒說重複在哪個時刻造成可觀察的問題（引用："The naive approach leads to duplicated code"）
- 退路：失去主要好處——關鍵分支退回各狀態重複規則，失去條件與樣式解耦
- 解鎖：跨類型條件可先存成自訂屬性，再用 style query 共用一組規則

經過：深色模式可能來自作業系統偏好，也可能來自網站上的手動切換，兩種來源要套同一組樣式，只好把規則抄兩份。把「現在是不是深色」先算成一個自訂屬性，規則只認這個屬性。限制是屬性必須設在所有要比對規則的祖先上。
%% line-end %%

### 細節（不索引）
- 對手組：樣式邏輯到處重複
- 支援狀態：Container style queries：Newly（2026-05-19）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前跨類型的條件（media 加 selector 加 container）只能把規則複製到每個組合底下 → 主題、密度、「寬螢幕且使用者選了精簡模式」這類組合條件可以先算成一個旗標，所有元件只認旗標，新增一種觸發來源不用改元件樣式
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
