---
guide: styling-web-components
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/styling-web-components.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 替 Web Components 加樣式

%% line-start id="mwg:styling-web-components" %%
## 用繼承的自訂屬性做主題，不要用 :host-context()
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：使用端在祖先上設 `--card-bg` 這類自訂屬性，元件內以 `var(--card-bg, white)` 讀取，取代 `:host-context([theme="dark"])`
- 被什麼擋：`:host-context()` 只有 Chromium 支援，Firefox 與 Safari 已拒絕實作，CSSWG 也傾向不再發展（引用："Firefox and Safari have declined to ship it and the CSSWG is leaning toward not developing it further — treat it as a Chromium-only dead end"）
- 戰報：勝——自訂屬性可繼承、穿過 shadow 邊界，在每個瀏覽器都有效，兩邊也不互相綁死（官方宣稱）

經過：元件用 `:host-context([theme="dark"])` 偵測深色模式，在 Chrome 裡正常，換到 Firefox、Safari 元件就停在淺色。改成由頁面設定自訂屬性、元件讀取，主題在哪都會傳進去。
%% line-end %%

### 細節（不索引）
- 對手組：押注不會普及的功能
- 支援狀態：:host-context()（被取代的做法）：Limited availability，Supported by: Chrome 54, Edge 79；Unsupported in: Firefox, Safari。自訂屬性：指南原文 "works everywhere"，未附 Baseline 資料，記 Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:styling-web-components:2" %%
## 公開的自訂屬性不要在 :host 上設值，用私有別名放預設
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`:host` 上只定義私有別名 `--_card-bg: var(--card-bg, white)`，內部一律用 `--_card-bg`，公開的 `--card-bg` 保持未設定
- 被什麼擋：在 `:host` 上定義的自訂屬性，只能被直接指定宿主元素的規則覆寫，祖先上設的值傳不進來（引用："A custom property *defined* on `:host` can only be overridden by rules targeting the host element specifically."）
- 戰報：勝——公開屬性沒被宿主截斷，可以從樹上任何一層繼承覆寫，預設值也只寫一次（官方宣稱）

經過：在 `:host` 寫 `--card-bg: white` 當預設，頁面在 `body` 上設 `--card-bg: navy` 卻沒反應，因為宿主自己的宣告優先。改用私有別名，公開屬性就能從外面一路繼承進來。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：自訂屬性：指南原文 "works everywhere"，未附 Baseline 資料，記 Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:styling-web-components:3" %%
## 包住原生控制項時設 font: inherit
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：shadow tree 內被包住的 `<button>`、`<input>`、`<select>` 設 `font: inherit`（通常再加 `color: inherit`）
- 被什麼擋：表單控制項的 `font` 來自 UA 樣式表、不繼承，被包住的控制項會顯示系統字型而不是頁面字型，這是最常見的遺漏（引用："The wrapped control therefore renders in the platform font, not the page font, until you set `font: inherit`"）
- 戰報：勝——加上 `font: inherit` 後，控制項跟頁面字型一致（官方宣稱）

經過：`<my-button>` 放進頁面，周圍文字都是品牌字型，只有按鈕是系統預設字。不是邊界擋住了，而是表單控制項本來就不繼承字型。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：不適用（指南未附這項的支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:styling-web-components:4" %%
## :host 的樣式不會傳到內部控制項，用 ::part 或自訂屬性轉交
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：內部控制項標上 `part="submit"` 讓使用端以 `my-card::part(submit)` 自由設樣式，或用一組自訂屬性傳固定的值；巢狀元件以 `exportparts` 往上轉出
- 被什麼擋：在 `:host` 上設 `background`、`border`、`padding` 只會作用在宿主的盒子，不會層疊進被包住的元素（引用："Setting `background`/`border`/`padding` on `:host` styles the host box, not the control inside it."）
- 戰報：勝——`::part` 已 Widely，使用端不必知道內部結構就能針對特定元素設樣式（官方宣稱）

經過：使用端想把按鈕底色改掉，在 `my-button` 上設 background，結果外面多了一圈色塊，裡面的按鈕還是原樣。開放 part 或自訂屬性才是有意的通道；part 只開幾個高階的，開太多會變成脆弱的 API。
%% line-end %%

### 細節（不索引）
- 對手組：封裝邊界切斷關聯
- 支援狀態：Shadow parts：Widely（2020-07-28）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:styling-web-components:5" %%
## display: contents 讓宿主量不到尺寸，錨點定位會壞
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：要把任意樣式傳給被包住的原生元素時，若用 `display: contents` 加 `all: inherit`，要知道它的代價；不適合時改用 `::part` 或自訂屬性
- 被什麼擋：`display: contents` 的元素 `getBoundingClientRect()` 與 `getClientRects()` 都回傳 0，以宿主為錨點的定位因此壞掉；`all: inherit` 也會抹掉 UA 預設（引用："`getBoundingClientRect()` and `getClientRects()` return zero for `display: contents` elements, so anchor positioning against the host is broken."）
- 戰報：部分改善——這是目前唯一能把任意樣式傳進原生元素的通用做法，但量測與錨點的代價仍在，只能依情況改用 part 或自訂屬性（官方宣稱）

經過：為了讓 `<my-button>` 完全透明而把宿主設成 `display: contents`，樣式傳遞成功了，但掛在這顆按鈕上的提示框找不到位置，因為宿主沒有盒子。指南把它講成取捨，不是捷徑。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：不適用（指南未附 display: contents 的支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:styling-web-components:6" %%
## 元件要用 container query 時，先給 :host 一個區塊盒
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`:host { display: block; container-type: inline-size; }`，再用 `@container` 依元件自己的寬度調整版面
- 被什麼擋：自訂元素預設 `display: inline`，尺寸 containment 不作用在 inline 或 contents 元素上，容器查詢就失效（引用："custom elements default to `display: inline` and size containment does not apply to `inline` or `contents` elements"）
- 戰報：勝——容器查詢已 Widely；宿主是區塊盒後，同一個元件放在側欄或全寬都會依自己的空間調整（官方宣稱）

經過：在元件裡寫了 `container-type` 和 `@container`，怎麼調寬度都不變，因為宿主是 inline。補一行 `display: block` 就生效。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Container queries (size)：Widely（2023-02-14）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 3 個糾錯提醒未拆：`::slotted()` 只碰得到最上層節點且會輸給 Light DOM 規則；`:state()` 讓狀態對外唯讀（同 custom-elements 指南的 custom states，指南沒說合成屬性在哪個時刻出錯）；元件內用 `@layer` 排序自己的樣式。
