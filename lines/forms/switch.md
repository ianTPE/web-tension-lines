---
guide: switch
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/switch.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 無障礙的開關控制項

%% line-start id="mwg:switch" %%
## 用 <input type="checkbox" switch> 做原生開關
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在一般 checkbox 上加布林屬性 `switch`，配 `<label>`，用 `accent-color` 換色、`:focus-visible` 補焦點框；不支援時依 `'switch' in HTMLInputElement.prototype` 有條件載入 `input-switch-polyfill`
- 被什麼擋：缺——指南只說 `switch` 保住原生表單送出、鍵盤操作與讀屏語意，沒說自製開關在哪個時刻出錯
- 戰報：僵持——只有 Safari 17.4 起支援，Chrome、Edge、Firefox 都要靠 polyfill（補上 `role="switch"`、開關外觀與拖曳）（官方宣稱）

經過：開關本質就是 checkbox，但長久以來只能自己畫。`switch` 屬性讓瀏覽器直接畫出開關並暴露 switch 角色，送出值和 checkbox 一樣。目前只有 Safari 原生支援，其他瀏覽器都得載 polyfill。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：`<input type="checkbox" switch>`：Limited availability。Supported by: Safari 17.4；Unsupported in: Chrome, Edge, Firefox
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：設定頁的每個開關都是一行 HTML，表單送出、鍵盤、讀屏「開／關」語意都由瀏覽器處理，不必維護開關元件。目前僅 Safari 原生，其他瀏覽器靠 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
