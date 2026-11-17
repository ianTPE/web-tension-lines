---
guide: shadow-dom
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/shadow-dom.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# Shadow DOM、模板與 slot

%% line-start id="mwg:shadow-dom" %%
## 大量實例共用一份 adoptedStyleSheets，不要每個實例各帶一份 <style>
- 做法：模組層建立一個 `CSSStyleSheet` 並 `replaceSync()`，每個實例的 shadow root 以 `adoptedStyleSheets = [sheet]` 共用
- 對手：模板裡的 `<style>` 每個實例複製一份，數量一大就把 DOM 撐肥；改用 `<link>` 則多一個請求並有未樣式化閃爍的風險（引用："Duplicated per instance; bloats the DOM at scale."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：清單裡上百張卡片，每張 shadow 裡都有同一段 `<style>`，DOM 裡就有上百份一樣的 CSS。共用一個建構式樣式表，數量再多也只解析一次。
%% line-end %%

### 細節（不索引）
- 對手組：樣式邏輯到處重複
- 支援狀態：不適用（本指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:shadow-dom:2" %%
## 用 slotchange 與 assignedElements() 判斷 slot 有沒有內容
- 做法：監聽 slot 的 `slotchange`，用 `assignedElements()` 取得實際分配到的元素，再決定例如是否切換 `has-header`
- 對手：元素之間的空白文字節點也會被分配到預設 slot，所以預設 slot 幾乎從不真的是空的；升級時 Light DOM 子節點在 `connectedCallback` 可能還不存在（引用："Text nodes between elements (including pure whitespace) are assigned to the default slot, so a default slot is rarely truly "empty.""）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：想在沒有標題時隱藏標題列，檢查預設 slot 有沒有節點，結果永遠有（換行與縮排），標題列一直在；在 `connectedCallback` 檢查又常常太早。改看 `assignedElements()` 並在 `slotchange` 時更新。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：不適用（本指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 3 個糾錯提醒未拆：模板定義一次再 `cloneNode(true)`，不要每次重新解析 `innerHTML`；避免過深的 div 與巢狀 shadow root；`::slotted(*:first-child)` 依 DOM 順序而非 slot 內順序比對（指南只說「常常不如預期」，沒給修法）。
