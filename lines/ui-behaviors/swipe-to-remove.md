---
guide: swipe-to-remove
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/swipe-to-remove.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 滑動移除

%% line-start id="mwg:swipe-to-remove" %%
## 用捲動吸附加 IntersectionObserver 做滑動移除，不手寫指標事件
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每列是一條三欄（左空白、內容、右空白）的水平 `scroll-snap-type: x mandatory` 軌道；以軌道為 root 的 IntersectionObserver 觀察內容，可見比例低於 `activateThreshold` 時放大圖示、低於 `commitThreshold` 時立刻提交並開始收合動畫
- 被什麼擋：用 `pointerdown`／`pointermove`／`pointerup` 自己驅動 transform，會失去原生捲動免費提供的慣性、回彈與鍵盤捲動（引用："You'll lose the momentum, snap-back, and keyboard scrolling that native scrolling gives you for free."）
- 戰報：勝——手勢交給瀏覽器的捲動引擎，慣性與吸附都是原生的；用到的捲動吸附、IntersectionObserver、MutationObserver、Web Animations 都是 Widely（官方宣稱）

經過：手寫拖曳的刪除列，放手後不會順著慣性滑走，速度判斷也怪。把列做成會吸附的水平捲軸，手指甩出去就是原生的手感，程式只負責看「內容還剩多少在畫面上」。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Scroll snap、Intersection observer、MutationObserver、Web animations：Baseline Widely available
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:2" %%
## 軌道設 `overscroll-behavior-x: none`，擋掉滑過頭觸發上一頁
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在每列的水平捲動軌道上設 `overscroll-behavior-x: none`
- 被什麼擋：沒有它時，滑過頭會觸發 iOS／Android 瀏覽器的返回上一頁手勢（引用："Without it, an over-swipe can trigger the browser's back-navigation gesture on iOS/Android."）
- 戰報：部分改善——滑動被關在列內；指南標 overscroll-behavior 為 Limited，但說這裡軌道一定可捲動，各瀏覽器行為一致、不需退路（官方宣稱）

經過：用力往右甩想封存一封信，整個頁面卻回到上一頁。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：overscroll-behavior：Limited availability，Supported by: Chrome 144, Edge 144, Firefox 150；Unsupported in: Safari（指南註明該限制只影響沒有可捲動溢出的容器）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:3" %%
## 吸附用 `mandatory`，不用 `proximity`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：軌道設 `scroll-snap-type: x mandatory`
- 被什麼擋：`proximity` 讓列可以停在一半，動作底色露出半截（引用："With `proximity`, the row can rest partially scrolled, leaving the action background half-visible."）
- 戰報：勝——列永遠停在內容或空白欄上（官方宣稱）

經過：輕輕一撥，那一列就卡在半開，紅色底露出一塊。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：Scroll snap：Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:4" %%
## 每個滑動動作都要有可見按鈕當替代
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每列放一顆至少 24×24 CSS px、名稱含項目名的原生按鈕，按下時走和滑動同一個 `commit` 函式
- 被什麼擋：滑動無法用鍵盤、單擊或讀屏完成，只能滑的功能違反路徑型手勢準則（引用："functionality must not be available solely through swiping gestures."）
- 戰報：勝——語音控制、鍵盤、讀屏使用者都能執行同一個動作（官方宣稱）

經過：用語音控制的人說得出「刪除」卻滑不了，那封信永遠刪不掉。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:5" %%
## 列裡有按鈕時不要讓軌道可聚焦，並提供復原
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：已經有動作按鈕的列不在軌道上加 `tabindex`；移除後考慮顯示復原提示
- 被什麼擋：軌道可聚焦時，按方向鍵捲動軌道就會直接提交動作、沒有任何確認；滑動本身也很容易誤觸（引用："arrow keys on a focused track commit the action with no confirmation."；"the gesture is fast and easy to trigger by accident."）
- 戰報：勝——鍵盤只能透過按鈕刪除，誤觸有復原路徑（官方宣稱）

經過：鍵盤使用者 Tab 到某一列、想往下看按了方向鍵，結果那一列被刪掉了。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發（新開，見下）
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 新開對手組理由：既有的「表單意外送出」只涵蓋表單送出；這裡（以及 dialog、menu、navigation-drawer 的幾條）是一般的破壞性或關閉動作被鍵盤、指標或手勢誤觸發，形狀相同但不限於表單
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:6" %%
## Safari 慣性還在跑時移除節點，下一列會自己捲走
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：偵測 `GestureEvent`（Safari 專有）時，先把列設 `inert`，延後幾秒才真正 `remove()`
- 被什麼擋：Safari 的捲動鎖定 bug：手勢慣性還沒結束就移除節點，補上來的下一列繼承了捲動，立刻把自己捲出畫面（引用："causes the next item (which slides up into this one's place) to inherit the scroll and immediately scroll itself off-screen."）
- 戰報：部分改善——延後移除可避開，代價是節點在 DOM 裡多留幾秒（官方宣稱）

經過：在 iPhone 上刪掉一封信，下一封也跟著滑出去，看起來像連刪兩封。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：瀏覽器 bug，指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:7" %%
## `scroll-initial-target` 要等軌道真的變成捲動容器才套用
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把內容的 `scroll-initial-target: nearest` 包在 `.is-initialized` 選擇器裡，JS 接好之後才生效
- 被什麼擋：軌道還不是捲動容器時，這個屬性會往上找最近的可捲動祖先（通常是整頁），改掉頁面的初始捲動位置（引用："would let the property walk up to the nearest scrollable ancestor (typically the document) and shift the page's initial scroll position"）
- 戰報：部分改善——屬性只在列自己的軌道上生效（官方宣稱）

經過：清單在頁面中段，一打開頁面卻直接被捲到某一列。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：scroll-initial-target：Limited availability，Supported by: Chrome 133, Edge 133；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:8" %%
## 退路的程式捲動要在接上觀察器之前執行
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：不支援 `scroll-initial-target` 時，在加上 `.is-initialized` 之後、接上內層 IntersectionObserver 之前設 `track.scrollLeft = track.clientWidth`；再用 ResizeObserver 在尺寸變化時補設，移除前記得取消觀察
- 被什麼擋：順序反了，初始的程式捲動會被當成一次滑動，馬上觸發提交（引用："Otherwise the initial programmatic scroll past the left spacer will be observed as a "swipe" and immediately fire the commit handler."）
- 戰報：部分改善——順序正確時列安靜地停在內容上（官方宣稱）

經過：在 Firefox 打開收件匣，每一列一出現就自己刪掉了。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：scroll-initial-target：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:9" %%
## 每列在進入畫面時才初始化，後來加入的列用 MutationObserver 接上
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：外層 IntersectionObserver 在列第一次進入畫面時才 `setupItem()`，離開時暫停內層觀察；`<ul>` 上的 MutationObserver 把新增的列交給外層觀察器
- 被什麼擋：頁面載入時就全部接好，會在列還沒渲染時讀到為 0 的 `clientWidth`；之後加入的列則根本沒被接上（引用："`setupItem` reads layout-dependent values like `clientWidth`, which return 0 until the item is rendered"；"Without it, items appended after page load won't get wired up."）
- 戰報：勝——每列都拿到真實尺寸，觀察器數量和畫面上看得到的列成正比（官方宣稱）

經過：無限捲動載入的新信件滑不動，舊信件的退路捲動又捲到 0。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Intersection observer、MutationObserver：Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:10" %%
## 移除結果寫進頁面上原本就有的 `role="status"`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：頁面一開始就放一個空的 `role="status"`，移除時寫入「Item One removed」
- 被什麼擋：一列消失本身不會被播報；而讀屏只播報「變動前就存在」的 live region（引用："A row disappearing isn't announced"；"screen readers only announce changes to live regions that existed before the change."）
- 戰報：勝——讀屏使用者知道哪一項被移除（官方宣稱）

經過：讀屏使用者按了移除，聽不到任何回應，不確定到底刪了沒。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:11" %%
## 移除聚焦中的列之前，先把焦點移到下一列
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：移除前若焦點在列內，移到下一列（或上一列、清單標題），並保持同一種元素（軌道對軌道、按鈕對按鈕）
- 被什麼擋：移除或 inert 掉含焦點的列，焦點會掉回 `<body>`（引用："Removing or inerting the row drops focus to <body> if focus is inside it"）
- 戰報：勝——鍵盤使用者可以連續處理下一列（官方宣稱）

經過：按鈕刪掉一封信後，下一個 Tab 從頁首重新開始。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:swipe-to-remove:12" %%
## 強制色彩模式下改用 `CanvasText` 加遮罩畫動作圖示
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`@media (forced-colors: active)` 時設 `forced-color-adjust: none`，背景用 `CanvasText`、以圖示當 `mask`
- 被什麼擋：強制色彩把動作底色換成 `Canvas`，白色圖示就看不見了（引用："Forced colors replaces the action background with Canvas, which hides the white icon."）
- 戰報：勝——圖示在強制色彩下仍可見（官方宣稱）

經過：高對比模式的使用者滑開一列，只看到一片空白，不知道會發生什麼。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
