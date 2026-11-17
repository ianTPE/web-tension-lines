---
guide: component-specific-light-dark-theme
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/component-specific-light-dark-theme.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 元件專屬的明暗主題

%% line-start id="mwg:component-specific-light-dark-theme" %%
## 在元件上設 `color-scheme`，讓整個子樹改用另一套明暗
- 做法：頁面以 `light-dark()` 定義色彩 token 後，在程式碼區塊、媒體播放器、相簿、只支援單一配色的嵌入等「自成視覺脈絡」的區塊設 `color-scheme: dark`（要強制時用 `only dark`），子樹裡的 token、表單控制項、捲軸都改照這個配色解析；按鈕這類只是換色的淺層容器不用
- 對手：指南只列出適用情境，並說舊瀏覽器要在根元素用 `prefers-color-scheme` 切自訂屬性、避免在個別元件上用 media query，沒說舊做法在哪個時刻出問題（引用："Avoid using the media query on individual components unless the component requires a very specific type of dark mode customization beyond colors."）
- 退路：失去主要好處——退回根元素的 media query 與 token，失去元件級原生 UI 配色
- 解鎖：單一元件可覆寫配色，讓子樹 token、表單控制項與捲軸一起切換

經過：淺色頁面裡想要一塊深色的程式碼區塊，以前得替它另寫一套顏色，連裡面的捲軸都還是淺色的。現在在那塊上宣告配色，token 自己重新解析。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：color-scheme：Widely available（2022-02-03）；light-dark()：Newly available（2024-05-13），Supported by: Chrome 123, Edge 123, Firefox 120, Safari 17.5
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前元件要固定深色就得複製一套顏色、內建控制項還跟不上 → 現在淺色文件站裡的程式碼區塊、影片播放器、地圖、元件預覽可以各自固定配色，連捲軸、勾選框都一起變，不必寫第二套樣式
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:component-specific-light-dark-theme:2" %%
## 改了 `color-scheme` 的元素要重新指定繼承的顏色屬性
- 做法：在設 `color-scheme` 的元素上重新寫一次 `color`、`accent-color` 等繼承的顏色屬性（就算是同一個 token）；設計 token 不要用 `@property` 註冊成 `<color>`；這類元素上不要對顏色屬性用 `inherit`
- 對手：`light-dark()` 在計算值階段就解析，繼承下去的只有其中一個顏色；元件改成深色，子樹的 `accent-color` 仍是淺色那一個（引用："any inherited `<color>` properties set to a `light-dark()` color will only pass down one of the two colors to their descendants"）
- 退路：保住主要行為——不支援 `light-dark()` 時用 media query 切 token，並重設元件顏色
- 解鎖：（缺）

經過：換了配色，背景變深了，強調色卻還是給淺色背景用的藍。因為傳下來的是已經算好的顏色，不是那個會依配色變的式子。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：light-dark()：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:component-specific-light-dark-theme:3" %%
## 不要在沒有背景的元素上設 `color-scheme`
- 做法：只在自己有背景、能建立獨立視覺脈絡的複雜區塊上覆寫 `color-scheme`
- 對手：在沒有背景的元素上設 `color-scheme`，背景與文字顏色來自不同配色，文字讀不出來（引用："Do not set `color-scheme` on elements without a background, as that risks mixing background and text color pairs from different color-schemes, resulting in unreadable text."）
- 退路：不需要——`color-scheme` 已 Widely，不必退路
- 解鎖：（缺）

經過：文字跟著元素變成深色模式的淺字，背景卻還透出頁面的淺色，結果是白底白字。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：color-scheme：Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:component-specific-light-dark-theme:4" %%
## Safari 不把嵌入端的配色傳進 iframe，要明確傳遞
- 做法：兩邊都能控制時，用網址參數（`?theme=dark`）或 `postMessage()` 把父頁的配色傳給 iframe，iframe 依此在 `<html>` 設 class 或 `color-scheme`；只控制被嵌入頁時，在嵌入 API 提供明確的主題參數並寫進文件
- 對手：Safari 不依嵌入端的 `color-scheme` 渲染 iframe，iframe 裡的 `prefers-color-scheme` 仍照系統設定（引用："Safari does not, and resolves `prefers-color-scheme` to the system setting even inside iframes."）
- 退路：不需要——`color-scheme` 已 Widely，不必退路
- 解鎖：（缺）

經過：Chrome 與 Firefox 會讓 iframe 跟著外面的配色走，Safari 不會。深色頁面裡嵌了一塊亮白的小工具，只能請兩邊用參數溝通。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：color-scheme：Widely（iframe 行為的差異見指南原文）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
