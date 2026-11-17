---
guide: accessible-web-components
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/accessible-web-components.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 無障礙的 Web Components

%% line-start id="mwg:accessible-web-components" %%
## 用 ariaLabelledByElements 等元素參照跨過 shadow 邊界，擋掉 id 參照默默失效
- 做法：shadow tree 內的控制項用 `ariaLabelledByElements`、`ariaDescribedByElements` 這類反射 ARIA 元素屬性，直接拿 Light DOM（或 slot 進來的內容）的元素當標籤或描述
- 對手：`aria-labelledby`、`aria-describedby` 這類 id 參照只在自己那棵樹裡解析，Light DOM 指不到 shadow 裡的 id、反之亦然，參照會被默默忽略（引用："An `id`-based attribute in the Light DOM cannot point at an `id` inside a shadow tree, and vice versa; the reference is silently ignored."）
- 退路：失去主要好處——退回同樹 id 或 `aria-label`，失去跨 shadow 的元素參照
- 解鎖：shadow 內控制項可直接參照 Light DOM 的標籤與描述元素

經過：元件把真正的 `<input>` 包在 shadow 裡，頁面上的說明文字卻在 Light DOM，`aria-describedby` 寫了也沒有作用，讀屏聽不到說明，而且沒有任何錯誤訊息。元素參照屬性讓 shadow 內的控制項直接指向外面的節點。反方向仍是空白。
%% line-end %%

### 細節（不索引）
- 對手組：封裝邊界切斷關聯
- 支援狀態：Element.ariaLabelledByElements：Newly（2025-04-04）。Supported by: Chrome 135, Edge 135, Firefox 136, Safari 16.4
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：設計系統的輸入元件可以讓使用端把標籤、說明、錯誤訊息寫在自己的頁面裡，元件內部的原生控制項照樣被正確標示，不必把整段說明搬進 shadow 或改用 aria-label
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:accessible-web-components:2" %%
## 宿主自帶角色時不要開 delegatesFocus
- 做法：宿主本身就是控制項（以 `ElementInternals` 設角色與狀態）時，在 `connectedCallback` 裡把宿主放進 Tab 順序；只有包住內部原生控制項時才用 `delegatesFocus: true`
- 對手：`delegatesFocus: true` 與宿主上的角色／狀態同時使用，焦點會落到內部元素，略過宿主的狀態（引用："Do not combine `delegatesFocus: true` with a role/state on the host, or focus will land on the inner element and skip the host's state."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：開關元件在宿主上宣告 `role="switch"` 與 `aria-checked`，又順手開了 `delegatesFocus`，Tab 進去焦點跑到內部某個元素，讀屏聽不到「開／關」。兩種模式擇一。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：ARIA attribute reflection：Widely（2023-10-24）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:accessible-web-components:3" %%
## tabIndex 在 connectedCallback 設，不要在 constructor 設
- 做法：`connectedCallback` 裡 `if (!this.hasAttribute('tabindex')) this.tabIndex = 0`
- 對手：在 constructor 裡設 tabindex，`document.createElement` 建立元素時會丟例外（引用："setting tabIndex in the constructor throws on createElement"）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：元件在 HTML 裡寫死時看起來正常，換成用 JS `createElement` 建立就直接拋錯。constructor 階段不能加屬性，把設定挪到 `connectedCallback`。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：不適用（指南未附這項的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 1 個糾錯提醒未拆：角色與狀態用 `ElementInternals` 設成元件的預設值，不寫在宿主屬性上，避免使用端意外蓋掉（指南沒說蓋掉後的具體現象）。
