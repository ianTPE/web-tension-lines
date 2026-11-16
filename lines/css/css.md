---
guide: css
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/css.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# CSS 現代架構

%% line-start id="mwg:css" %%
## 用 :not() 排除，不用後面的規則蓋回去
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：要排除不相關的狀態或目標時用 `:not()`，例如 `li:not(:last-child)`、`button:hover:not(:disabled)`
- 被什麼擋：先套樣式再用另一條規則覆寫回去，一旦兩條規則對調順序，停用的按鈕也會出現 hover 背景；覆寫也可能誤蓋掉別處設定的值（引用："If we reorder the two rules, we will get a hover background on disabled buttons!"）
- 戰報：勝——不過度匹配的選擇器與規則順序無關（官方宣稱）

經過：「全部加框線、最後一個再拿掉」是很常見的寫法，但它表達的不是真正的意圖，而且依賴規則順序。指南區分兩種情況：排除不相關的目標用 `:not()`；特化（一般按鈕是灰的、主要按鈕是藍的）用覆寫就沒問題。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:css:2" %%
## 排除巢狀子樹用 @scope，不用 :not() 加後代選擇器
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `@scope (.card) to (.content) { … }` 選取卡片內、但不在 `.content` 裡的元素
- 被什麼擋：`.card :not(.content *)` 遇到巢狀卡片就不如預期，排除範圍選錯元素（引用："For example, `.card :not(.content *)` will not work as expected for nested cards."）
- 戰報：勝——`@scope` 考慮層級距離，巢狀卡片也正確（官方宣稱）

經過：`:not()` 只看「有沒有某個祖先」，不看「最近的是哪一個」，所以元件一巢狀就失準。`@scope` 的下界讓排除範圍跟著最近的 scope 根走。同一份指南也用 `@scope` 解決 `.dark .invert`／`.light .invert` 巢狀時永遠解析成同一個主題的問題。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料；不自行補 @scope 的支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯（指南未標示 @scope 是新 API，也沒有支援資料，依規則不判為新能力）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:css:3" %%
## 不寫套在 * 上的全域 reset
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：reset 只套在特定元素類型或條件上，不寫在 `*`
- 被什麼擋：套在 `*` 的 reset，web component 和優先序較低的 cascade layer 都覆寫不了，除非動用 `!important`（引用："they cannot be overridden by web components or lower-priority cascade layers (without `!important`)."）
- 戰報：缺——指南只說改套到特定元素，沒說這樣做之後對手的情況（官方宣稱）

經過：`* { box-sizing: border-box; margin: 0 }` 幾乎是起手式，但它直接命中每個元素，包括 web component 內部想自己決定的部分。指南提倡用 `@layer` 與 `:where()` 管理優先序，全域 reset 和這個方向正好衝突。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

未拆：§3 開頭「用 `:has()` 取代 JS 管理 class」只是指向 child-state-based-styling／content-based-styling 兩份指南，已在那裡拆；`@scope` 解決主題 class 巢狀（`.dark .invert`）一處併入第二條的經過；BEM、邏輯屬性、設計 token 分層等段落沒有可觀察的對手。
