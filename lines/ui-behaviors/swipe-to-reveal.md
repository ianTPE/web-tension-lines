---
guide: swipe-to-reveal
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/swipe-to-reveal.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 滑動揭露

%% line-start id="mwg:swipe-to-reveal" %%
## 用捲動吸附做滑開動作列，不攔 wheel、touchmove、pointermove
- 做法：外層 `.SwipeReveal` 是兩欄 grid（`100% max-content`）的水平捲動容器，`scroll-snap-type: x mandatory`，內容吸附 `start`、動作面板吸附 `end`
- 對手：在主執行緒攔截手勢事件自己平移內容，會擋住合成器驅動的捲動、破壞原生慣性、拖慢反應（引用："Main-thread gesture interception blocks compositor-driven scrolling, breaks native scroll momentum, and degrades responsiveness."）
- 退路：不需要——Scroll snap 已廣泛支援，以水平捲動容器取代主執行緒攔截手勢事件即可通用
- 解鎖：（缺）

經過：手寫滑動的列表在低階手機上卡頓，放手後停得很生硬。改成會吸附的水平捲軸，滑開的手感和原生 app 一樣。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Scroll snap：Baseline Widely available（2020-01-15 起）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:swipe-to-reveal:2" %%
## 外層滑動容器設 `overscroll-behavior: chain`：照樣串接捲動，但不回彈
- 做法：外層 `.SwipeReveal` 設 `overscroll-behavior: chain`；內層可捲動的內容窗格保留預設 `auto`
- 對手：預設的 `auto` 會讓外層包裝在邊界回彈、選單跟著彈；`contain`、`none` 又會把捲動困住，傳不到外面的頁面（引用："avoid on the outer swipe wrapper where it causes the menu to bounce"）
- 退路：失去主要好處——退回 overscroll-behavior:auto，串接保留但選單邊界回彈
- 解鎖：在不截斷父層捲動串接的前提下，單獨消掉外層滑動容器在邊界產生的局部回彈效果

經過：滑開動作列時整條連同按鈕一起橡皮筋彈一下，很廉價。以前只能在「會彈」和「捲動被困住」之間二選一，新關鍵字把串接和回彈拆開了。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：overscroll-behavior：Limited availability，Supported by: Chrome 144, Edge 144, Firefox 150；Unsupported in: Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前巢狀捲動只能選「回彈」或「困住」 → 現在直向動態牆裡可以放滑開動作的列、可側滑的卡片或橫向膠囊列，邊界不回彈、多餘捲動自然傳給外層。Safari 仍會回彈
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:swipe-to-reveal:3" %%
## 滑開面板用 `mandatory` 吸附，不用 `proximity`
- 做法：外層設 `scroll-snap-type: x mandatory`
- 對手：`proximity` 下輕輕一滑，動作按鈕或側選單會停在半露狀態（引用："With `proximity`, a light swipe can leave the action buttons or side menu partially exposed at rest."）
- 退路：不需要——Scroll snap 已廣泛支援，改設 x mandatory 即可在各瀏覽器防止動作面板停在半露狀態
- 解鎖：（缺）

經過：列表裡好幾列都露著半顆「刪除」按鈕。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：Scroll snap：Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:swipe-to-reveal:4" %%
## 滑開才看得到的動作，要有觸發按鈕可以打開
- 做法：內容裡放一顆名稱含項目名的觸發按鈕（`aria-expanded`），按下時捲動到面板、把面板按鈕的 `tabindex` 改成 0；再按一次反向操作
- 對手：只能靠滑動取得的功能，違反路徑型手勢準則（引用："functionality must not be available solely through swiping gestures."）
- 退路：不需要——可見觸發按鈕與 tabindex 管理屬基礎無障礙規範，鍵盤與輔助技術在所有環境皆可操作
- 解鎖：（缺）

經過：鍵盤使用者知道每列有「釘選」「封存」，卻找不到任何方法打開它們。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:swipe-to-reveal:5" %%
## 左側面板用 `scroll-initial-target` 讓列一開始停在內容欄
- 做法：左右兩側都有面板（`max-content 100% max-content`）時，把前導面板放在內容前面，內容設 `scroll-initial-target: nearest`
- 對手：不支援的瀏覽器從捲動位置 0 開始渲染，左側面板一開始就露在外面（引用："browsers that do not support `scroll-initial-target: nearest` will initially render at scroll offset `0` with the leading panel exposed."）
- 退路：保住主要行為——偵測不支援時在 load 以 scrollTo instant 跳回內容欄，僅短暫仰賴 JS 定位而不捲動整頁
- 解鎖：純 CSS 就能讓含左側面板的滑動列於初次渲染時直接停在中間內容欄，不必在載入後寫 JS 捲回

經過：郵件列左滑封存、右滑刪除，在 Safari 打開時每一列都先露出左邊的封存鈕。
%% line-end %%

### 細節（不索引）
- 對手組：內容要等JS才成形
- 支援狀態：scroll-initial-target：Limited availability，Supported by: Chrome 133, Edge 133；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前雙向滑動的列要 JS 先捲到中間 → 現在郵件、待辦、聊天列表可以純 CSS 做「左滑一組動作、右滑另一組」的雙側列，載入時就停在中間。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:swipe-to-reveal:6" %%
## 覆寫既有的 `contain`／`none` 時，先寫 `auto` 再寫 `chain`
- 做法：基礎樣式已設 `overscroll-behavior: contain` 或 `none` 時，在 `chain` 前面緊接著宣告 `overscroll-behavior: auto`
- 對手：不認得 `chain` 的瀏覽器會丟掉這行，留下先前的 `contain`／`none`，捲動被困住（引用："declare `overscroll-behavior: auto` immediately before `overscroll-behavior: chain` so browsers that do not yet support `chain` still chain scrolling to the parent rather than trapping it."）
- 退路：保住主要行為——先寫 auto 再寫 chain，不支援的 Safari 會回退到 auto 並照常將捲動串接回父層
- 解鎖：（缺）

經過：工具類別預設 `overscroll-behavior: none`，換成 Safari 後在這一列上下滑整頁都不動。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：overscroll-behavior：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：內容窗格可聚焦時，用 `focusin` 加 `:focus-visible` 判斷，把內容捲回起點以關閉面板
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
