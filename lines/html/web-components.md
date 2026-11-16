---
guide: web-components
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/web-components.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# Web Components 導覽

%% line-start id="mwg:web-components" %%
## 包住真正的 <button>，不要重做原生語意
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只有需要封裝狀態、可腳本化的 API 或原生元素做不到的行為時才寫自訂元素；需要包裝時，把真正的 `<button>` 包在裡面，而不是用 `<my-button>` 重做焦點、啟動與 ARIA
- 被什麼擋：缺——指南說重做原生語意是最常見的誤用、只有沿用原生元素才能免費繼承可及性，但沒說重做版在哪個時刻出錯
- 戰報：勝——沿用原生元素，焦點、啟動、可及性都由平台提供（官方宣稱）

經過：為了換個外觀就從零寫一個按鈕元件，焦點、Enter／Space、角色都要自己補。指南的判準是：需要的是封裝狀態或可腳本化的 API，而不只是不同的樣子；只是變色的按鈕用 `<button>` 加 CSS 就好。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:web-components:2" %%
## shadow root 用 open 模式
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`attachShadow({ mode: 'open' })`，宣告式則用 `shadowrootmode="open"`
- 被什麼擋：`mode: 'closed'` 會讓頁面腳本、測試工具與會走訪 shadow tree 的自動無障礙檢查器都拿不到 `element.shadowRoot`（引用："`mode: 'closed'` hides `element.shadowRoot` from page scripts, test harnesses, and automated accessibility checkers that walk shadow trees."）
- 戰報：勝——open 模式下工具與 hydrate 腳本都能進入 shadow tree（官方宣稱）

經過：為了「封裝得更徹底」用了 closed，結果自動化無障礙檢查掃不到元件內部，測試也只能從外面猜。封裝靠的是 shadow 邊界本身，不是把 root 藏起來。
%% line-end %%

### 細節（不索引）
- 對手組：封裝邊界切斷關聯
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:web-components:3" %%
## 不要用自訂內建元素（is="…"）
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：不用 `extends HTMLButtonElement` 加 `is="…"`，改用自主自訂元素包住原生元素
- 被什麼擋：Safari 已永久拒絕實作自訂內建元素（引用："Avoid *customized built-in elements* (`extends HTMLButtonElement` with `is="…"`); Safari has permanently declined to ship them."）
- 戰報：勝——用包裝的自主自訂元素，所有瀏覽器行為一致（官方宣稱）

經過：`<button is="fancy-button">` 看起來最優雅，原生語意全保留，但在 Safari 上它只是一顆普通按鈕，擴充的行為全部不存在，而且不會有支援的一天。
%% line-end %%

### 細節（不索引）
- 對手組：押注不會普及的功能
- 支援狀態：不適用（本指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 4 條未拆（與既有線同一個對手）：`super()` 要先呼叫（同 `mwg:custom-elements:4`）；ARIA id 參照不能跨 shadow 邊界（同 `mwg:accessible-web-components`）；shadow 模板裡用語意元素；標籤名要 kebab-case 且含連字號。另有選用判準（已有框架時優先用框架元件、靜態標記優先用 HTML＋CSS）未拆，屬於取捨建議，沒有對手。
