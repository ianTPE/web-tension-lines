---
guide: accordion
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/accordion.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 手風琴（Accordion）

%% line-start id="mwg:accordion" %%
## 需要個別標題時不要把 heading 塞進 summary
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用相鄰的 `<details>` 組手風琴；每一項需要自己的標題時，改用自訂 accordion
- 被什麼擋：在 `<summary>` 裡放 heading，JAWS 與 TalkBack 把 summary 當按鈕並丟掉裡面的標題，使用者無法用標題在項目間跳（引用："JAWS and TalkBack expose `summary` as a button and drop any heading inside it, so their users cannot move between items by heading."）
- 戰報：勝——改用自訂 accordion 後標題保留在無障礙樹中（官方宣稱）

經過：`<details>` 很適合當手風琴，但它的 summary 角色會吃掉內部結構。指南明確點名兩個螢幕閱讀器，這是可以實測驗證的對手。navbar 指南對 summary 角色實作不一致也有同樣警告。
%% line-end %%

### 細節（不索引）
- 對手組：原生元素角色實作不一致
- 支援狀態：details：Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:accordion:2" %%
## 不用互斥 <details name>，避免內容跳出視野
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：預設讓多個項目可同時展開，不使用 `<details name>` 的互斥行為
- 被什麼擋：互斥手風琴開一項就關另一項，內容位移出使用者的視野，對使用螢幕放大鏡的人影響很大（引用："They also can cause content to shift out of the user’s view which can cause significant problems for those using screen magnifiers."）
- 戰報：勝——不採用互斥就沒有這個位移；指南對「新功能本身就是對手」的情況給出了明確立場（官方宣稱）

經過：`<details name>` 是 2024 年才 Baseline 的新能力，但指南建議避免使用。這條線的特別之處是：對手不是舊做法，而是新功能帶來的副作用。真的需要互斥時，原文要求只在不得已時用。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Mutually exclusive <details>：Newly（2024-09-03）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:accordion:3" %%
## 用 ::details-content 收合，保留頁內搜尋與動畫
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：收合內容放在 `::details-content`，以 `content-visibility: hidden` 隱藏而非 `display: none`
- 被什麼擋：用 `display: none` 隱藏收合內容，頁內搜尋找不到、高度也無法動畫（引用："While closed it is hidden with `content-visibility: hidden`, not `display: none`, which is what keeps it findable and lets its size animate."）
- 戰報：部分改善——支援的瀏覽器裡內容可被搜尋並能滑動展開；`::details-content` 才 Newly，舊瀏覽器沒有動畫（官方宣稱）

經過：收合區塊的內容一旦 `display: none`，Ctrl+F 就找不到。`<details>` 收合時改用 `content-visibility: hidden`，內容仍在、搜得到，瀏覽器在搜尋命中時會自動打開它；`::details-content` 這個偽元素則讓收合區塊可以被選取、加樣式、對高度做動畫。反過來，不想被搜尋到時才刻意用 `display: none`。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：`<details>` 搜尋命中自動展開：Chrome 97、Firefox 148、Safari 26.2（Safari 不會正確捲到命中文字，WebKit bug 304174；web-features 未列入任何功能，沒有 Baseline 標籤）；::details-content：Newly（2025-09-16）；transition-behavior：Newly（2024-08-06）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：可以把很長的頁面全部摺起來，Ctrl+F 照樣找得到並自動展開，還能做展開動畫。長文件、FAQ、週記這類「想摺疊又怕找不到」的頁面不再兩難
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
- 變更紀錄：2026-11-12 更正「經過」：搜尋命中自動展開是 `<details>` 的行為，不是 `::details-content` 帶來的；補上三家支援資料（@mdn/browser-compat-data 8.1.8）
