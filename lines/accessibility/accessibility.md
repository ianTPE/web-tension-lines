---
guide: accessibility
category: accessibility
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/accessibility/accessibility.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 無障礙程式設計準則

%% line-start id="mwg:accessibility" %%
## 每頁只放一個 h1，讓讀屏找得到主標題
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：頁面主標題只用一個 `<h1>`，其餘標題依層級用 `<h2>`–`<h6>`（對話框內的主標題例外）
- 被什麼擋：一頁放了好幾個 `<h1>`，螢幕閱讀器使用者分不出哪一個才是主標題（引用："Having more than one `<h1>` element on a page makes it difficult for screen reader users to identify the actual main heading."）
- 戰報：勝——只留一個 `<h1>` 就沒有歧義；這是純標記規則，指南沒有給支援資料（官方宣稱）

經過：讀屏使用者常靠標題清單或「跳到 h1」快速定位，多個 h1 讓這個入口失效。指南把 `<dialog>`／`role="dialog"` 裡的 h1 列為例外，因為對話框是獨立視窗。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:accessibility:2" %%
## 需要當標題的展開鈕，不要把 heading 塞進 summary
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：標題要兼當展開觸發時，改用 heading 包住 button 的 ARIA 手風琴／disclosure，不用 `<details>`／`<summary>`
- 被什麼擋：部分瀏覽器把 `<summary>` 當按鈕暴露，連帶拿掉子元素的所有角色，裡面的標題就消失了（引用："Some browsers still expose this element as a button, which removes all roles from its children including headings."）
- 戰報：勝——heading 包住 button 時，標題留在無障礙樹裡（官方宣稱）

經過：和 accordion、navbar 指南是同一個對手：`summary` 的角色在各家實作不一致。這份通用準則沒有點名哪個讀屏，只說「some browsers」。
%% line-end %%

### 細節（不索引）
- 對手組：原生元素角色實作不一致
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:accessibility:3" %%
## 清單標記只給真正的清單
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<ul>`／`<ol>` 只用在重複、連續的項目；段落文字不要包成清單
- 被什麼擋：把分開的段落標成清單，讀屏每次都唸出清單資訊，使用者聽到混亂又多餘的內容（引用："screen readers will announce list information when they encounter lists, therefore leading to a screen reader hearing potentially confusing and redundant information about the related content."）
- 戰報：勝——不是清單就不會被唸成清單（官方宣稱）

經過：清單標記會讓讀屏先報「清單，N 項」，所以用錯地方就變成噪音。同一節還提到核取方塊與單選鈕本身就會報數量，再包一層清單會重複播報。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有約 30 條未拆（清單式指南，幾乎每一項都有自己的對手，例如表格排版、正數 tabindex、`title`／`placeholder` 當標籤、`touch-action: none`、焦點框只用 `box-shadow` 等）。
