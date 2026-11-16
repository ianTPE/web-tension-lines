---
guide: motion
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/motion.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 動態效果

%% line-start id="mwg:motion" %%
## 被裁切或遮罩的可聚焦元素，焦點框畫在父層
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `clip-path`、`mask-image` 做形狀揭露或淡出時，若元素可聚焦（例如 `tabindex="0"` 的捲動容器），焦點指示畫在沒被裁切的父元素上
- 被什麼擋：`clip-path` 與 `mask-image` 也會裁掉元素自己的焦點外框（引用："Both also clip the element's own focus outline"）
- 戰報：勝——焦點指示不被效果吃掉（官方宣稱）

經過：為了邊緣淡出加的遮罩，順便把鍵盤使用者唯一的位置提示也淡掉了。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：clip-path／mask-image：本指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:motion:2" %%
## 非必要的捲動連動效果用捲動驅動動畫
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：捲動相關的裝飾效果用 `animation-timeline: scroll()`
- 被什麼擋：指南只說用它取代 JS 監聽器，沒說監聽器在哪個時刻出問題（引用："Use **Scroll-Driven Animations** (`animation-timeline: scroll()`) for non-essential scroll-bound effects instead of JS listeners."）
- 戰報：缺——本指南沒說換成捲動驅動動畫後改善了什麼

經過：總覽指南只留了方向，細節見 mwg:scroll-progress-indicator、mwg:parallax-scroll-effects。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：本指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 缺
- 類型：新能力
- 解鎖（發想，非指南原文）：同 mwg:scroll-progress-indicator：進度條、視差、捲動揭露可以純 CSS 綁在捲動位置上
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:motion:3" %%
## 複雜版面狀態之間用 View Transitions 過渡
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：版面在兩個狀態之間大幅改變時用 View Transitions 做動畫
- 被什麼擋：指南只說可以在複雜版面狀態之間無縫過渡，沒說不這麼做時出了什麼事（引用："Use **View Transitions** to animate between complex layout states seamlessly."）
- 戰報：缺——本指南沒說具體改善

經過：一句方向，細節見 mwg:group-element-transitions、mwg:directional-navigation-transitions。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：本指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 缺
- 類型：新能力
- 解鎖（發想，非指南原文）：同 mwg:group-element-transitions：清單、格狀版面的重排可以讓每個項目平滑走到新位置
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:motion:4" %%
## `transition-behavior: allow-discrete` 寫在 `transition` 之後、分開寫
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`transition` 列出 `opacity`、`display`、`overlay`，另起一行寫 `transition-behavior: allow-discrete`
- 被什麼擋：寫進簡寫或寫在簡寫之前，會被簡寫重設，或在舊瀏覽器失效（引用："Separate after transition so the shorthand doesn't reset it or fail in older browsers"）
- 戰報：部分改善——離散屬性的進出場能過渡，舊瀏覽器保有其他過渡（官方宣稱）

經過：和 mwg:animate-element-entry-exit:3 同一個坑，在總覽指南再提醒一次。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：本指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:motion:5" %%
## 暫停鈕的標籤會在 Pause／Play 間切換時，不再加 `aria-pressed`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：自動播放超過五秒的動態內容旁放一顆可用鍵盤操作的暫停 `<button>`；標籤已在 Pause 與 Play 間切換時，不加 `aria-pressed`
- 被什麼擋：標籤切換又加 `aria-pressed`，讀屏會唸出「已按下的 Play 按鈕」（引用："or screen readers announce a pressed "Play" button"）
- 戰報：勝——按鈕名稱本身就說明狀態，不再自相矛盾（官方宣稱）

經過：兩種狀態表示法疊在一起，「已按下的播放」到底是在播還是沒播，聽的人無從判斷。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：ARIA 用法：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:motion:6" %%
## 關掉動畫時元素仍要停在最終狀態
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：減少動態時預設靜態、在 `no-preference` 裡才加動畫，並確認元素落在最終狀態
- 被什麼擋：動畫被關掉後元素停在起始值，內容被留在隱藏狀態（例如 `opacity: 0`），焦點與選取指示也不出現（引用："so content isn't left hidden (for example, at `opacity: 0`)"）
- 戰報：勝——不論動態偏好，內容與指示都看得到（官方宣稱）

經過：淡入動畫的起點是透明，動畫一關，內容就永遠停在透明。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：prefers-reduced-motion：本指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:motion:7" %%
## 從動畫事件拿 Animation 物件用 `event.animation`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `animationstart`、`transitionend` 等事件裡直接用 `event.animation`；可用 `'animation' in AnimationEvent.prototype` 偵測
- 被什麼擋：用 `event.target.getAnimations()` 依名稱過濾時，WAAPI 動畫沒有名稱對不到、同名動畫分不出來，也分不出是元素還是偽元素上的動畫（引用："`event.target` always points to the originating DOM element, so it does not distinguish between animations running on the element itself versus one of its pseudo-elements"）
- 戰報：勝——拿到的就是觸發事件的那個動畫，偽元素可從 `effect.pseudoElement` 得知（官方宣稱）

經過：照名字找動畫多數時候能用，直到同一個元素和它的 `::before` 都在跑 fade-in。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：event.animation：指南只給偵測方式、未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:motion:8" %%
## 減少動態時 `animationend` 不會來，別只等它
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：等動畫結束才移除或隱藏元素的程式，在 `element.getAnimations()` 回傳空陣列時直接繼續，或保留一個短的 opacity 過渡
- 被什麼擋：動畫只在 `no-preference` 裡套用、設成 `none` 或零時長時，`animationend`／`transitionend` 永遠不觸發，等著它的移除或隱藏永遠不發生（引用："`animationend` and `transitionend` never fire"）
- 戰報：勝——不論動態偏好，元素都會被移除或隱藏（官方宣稱）

經過：為減少動態偏好關掉動畫，結果通知關不掉，因為關閉邏輯在等一個不會發生的事件。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 4 個糾錯提醒未拆：優先動畫 `opacity` 與 `transform`；考慮預設靜態讓使用者選擇開啟；閃爍不超過每秒三次且不能靠 `no-preference` 解套；不要全域設 `animation-duration: 0.01ms`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
