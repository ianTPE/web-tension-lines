---
guide: 2d-panning
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/2d-panning.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 二維平移

%% line-start id="mwg:2d-panning" %%
## 用 `scroll-axis-lock: none` 關掉二維平移的軸鎖定
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在建立二維捲動的元素本身（`overflow: auto`）設 `scroll-axis-lock: none`；它不繼承，設在外層包裝無效，巢狀的一維面板保留預設的 `auto`；一般文章、動態牆、一維清單維持 `auto`
- 被什麼擋：手勢一開始若明顯偏向某一軸，瀏覽器把捲動鎖在該軸、忽略垂直方向的位移，通常整個手勢都鎖著；地圖、放大的圖片、無限畫布、節點圖上斜向或 L 形的平移因此卡住（引用："the browser locks the scroll to that single horizontal or vertical axis and ignores perpendicular deltas—often for the remainder of the gesture."）
- 戰報：僵持——支援時保有合成器執行緒捲動、慣性、原生捲軸與鍵盤導覽，又不鎖軸；僅 Chrome 153，其他瀏覽器要嘛接受鎖軸，要嘛用 `wheel` 加 `pointermove` 改 `scrollLeft`／`scrollTop` 的 JS 退路，代價是捲動移到主執行緒、觸控放手後沒有慣性（官方宣稱）

經過：鎖軸是為了讀文章時不會往旁邊飄，放到地圖上卻變成：想往右下拖，畫面只肯往右。以前只能自己寫平移引擎，現在一個屬性就能告訴瀏覽器這裡是二維的。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：scroll-axis-lock：Limited availability。Supported by: Chrome 153。Unsupported in: Edge, Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前要自由斜向平移就得放棄原生捲動、自寫拖曳引擎 → 現在白板、心智圖、大型試算表、平面圖檢視器可以直接用原生捲動容器做二維平移，捲軸、鍵盤、慣性都是瀏覽器的。目前僅 Chrome 153
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:2d-panning:2" %%
## 二維平移區要擋住捲動串接與滑動換頁
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：二維捲動容器加 `overscroll-behavior: none` 或 `contain`
- 被什麼擋：平移到邊界時捲動串接到父頁面，或觸發瀏覽器的左右滑動上一頁／下一頁、下拉重新整理（引用："so that reaching an edge does not chain scrolling to the parent page or trigger accidental browser overscroll navigations (such as horizontal back/forward swipe navigation or pull-to-refresh)."）
- 戰報：勝——平移停在容器邊界，不會帶動整頁，也不會意外離開頁面（官方宣稱）

經過：在地圖上往左拖到底，瀏覽器以為你要回上一頁。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：overscroll-behavior：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:2d-panning:3" %%
## 平移改 `scrollLeft`／`scrollTop`，不要用 `transform`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：自己處理平移時，把位移加到 `scrollLeft` 與 `scrollTop`
- 被什麼擋：用 CSS `transform` 平移內容，元素不再是捲動容器，原生捲軸、邊界夾限、方向鍵捲動、`scroll` 事件、IntersectionObserver、scroll-driven animations 全部失效（引用："Translating the surface with `transform` stops the element from functioning as a scroll container"）
- 戰報：勝——元素仍是真正的捲動容器，瀏覽器自動夾限位置、捲軸同步，鍵盤捲動與事件照常運作（官方宣稱）

經過：用 transform 拖畫布很直覺，但從那一刻起，瀏覽器就不知道這是一個可以捲的區域。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：scrollLeft／scrollTop：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:2d-panning:4" %%
## `touch-action` 只在 JS 退路裡設，而且用 `pinch-zoom`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只在 `@supports not (scroll-axis-lock: none)` 的 JS 指標退路啟用時設 `touch-action: pinch-zoom`，不用 `none`
- 被什麼擋：無條件設 `touch-action` 會關掉原生的合成器觸控捲動；設成 `none` 還連雙指縮放一起關掉（引用："restricting it disables native compositor touch scrolling."）
- 戰報：部分改善——支援 `scroll-axis-lock` 的瀏覽器保留原生觸控捲動；退路裡雙指縮放仍可用（WCAG 1.4.4），但放手後沒有慣性（官方宣稱）

經過：為了讓 JS 接手觸控平移而關掉瀏覽器的手勢處理，一不小心就連使用者放大文字的能力也拿走了。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：touch-action：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：沒有可聚焦子元素的平移區要加 `tabindex="0"`、角色、名稱與 `:focus-visible` 外框，讓鍵盤使用者能用方向鍵平移（沒說不加時的具體後果）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
