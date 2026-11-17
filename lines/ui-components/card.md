---
guide: card
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/card.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 卡片

%% line-start id="mwg:card" %%
## 卡片內容多或有其他動作時，改用「延伸連結」，不要整張包在 `<a>` 裡
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：整張卡片只有一個目的地且內容短，才用一個 `<a>` 包住 `<article>`；否則只讓標題裡的 `.card-link` 是連結，用 `::after` 加 `inset: 0` 把點擊範圍延伸到整張卡
- 被什麼擋：整張包在連結裡時，連結的可及名稱就是卡片的全部文字（引用："Because the link's accessible name is all of the card's text, keep the content short"）
- 戰報：勝——連結名稱只剩標題，整張卡片仍可點（官方宣稱）

經過：讀屏使用者在連結清單裡聽到一整段摘要、作者、日期才知道這是哪篇文章。只讓標題當連結、用偽元素撐大點擊區，聽起來和點起來都對了。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:card:2" %%
## 「閱讀更多」連結要有以可見文字開頭的完整名稱
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：寫成 `Read more<span>（視覺隱藏）about poached eggs</span>`；不要再加其他重複標題網址的連結
- 被什麼擋：一模一樣的「閱讀更多」在讀屏的連結清單裡無法分辨（引用："identical "read more" links are ambiguous in a screen reader's link list."）
- 戰報：勝——每個連結名稱各自指出目的地（官方宣稱）

經過：連結清單裡排了十個「閱讀更多」。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:card:3" %%
## 選擇卡片被選取時，不要改會影響版面的屬性
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<label class="card">` 內放勾選框或單選鈕，用 `:has(> :checked)` 只改透明邊框的顏色、`outline` 或 `box-shadow`
- 被什麼擋：選取時改 `border-width`、`padding`、`font-weight`，這張卡和旁邊的卡都會跳動（引用："Never change layout-affecting properties such as `border-width`, `padding`, or `font-weight` on selection, because the card and its neighbors jump"）
- 戰報：勝——選取只改顏色，版面不動（官方宣稱）

經過：方案比較卡一點選，整排卡片往右擠了兩像素。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:card:4" %%
## 延伸連結只能有一個，其他互動元素逐一提升層級
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每張卡只在一個連結上加 `.card-link`；其他 `a`、`button`、`input` 等元素依類型設 `position: relative; z-index: 1`，不要對整個容器設 `z-index`
- 被什麼擋：多個連結都延伸時最後一個蓋住整張卡；對整個容器設 `z-index` 則會攔下不產生任何動作的點擊（引用："each would stretch its own overlay and the last one would capture the whole card"；"Do NOT apply `z-index` to entire containers as that would make them capture pointer events that don't produce any action."）
- 戰報：勝——卡片其他區域點了走主連結，按鈕各自可按（官方宣稱）

經過：點卡片上的「收藏」卻打開了文章；點頁尾空白處什麼事都沒發生。
%% line-end %%

### 細節（不索引）
- 對手組：堆疊脈絡改變層級
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:card:5" %%
## 以卡片自己為容器查詢排版，不看視窗或格線父層
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：卡片設 `container-type: inline-size`，用 `@container` 規則調整子元素；有媒體的卡片才用 `:has(> img)` 開側欄
- 被什麼擋：卡片的實際寬度取決於欄數、間距等，用父層訂的斷點很不準（引用："the card's actual width can depend on column count, gaps and so on, making parent-based breakpoints are noisy."）
- 戰報：勝——窄時依原始順序堆疊、寬時媒體靠邊，放到哪都對（官方宣稱）

經過：同一張卡在三欄格線裡太擠、在側欄裡卻用了寬版排法。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：區塊不要再包 `.card__body` 之類的 wrapper（無法用選擇器定位各區）；沒有媒體的卡片不要保留空的媒體欄；隱藏的選擇控制項要保持可聚焦、不用 `display: none`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
