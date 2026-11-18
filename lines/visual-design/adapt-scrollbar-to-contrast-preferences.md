---
guide: adapt-scrollbar-to-contrast-preferences
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/adapt-scrollbar-to-contrast-preferences.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 讓捲軸配合高對比偏好

%% line-start id="mwg:adapt-scrollbar-to-contrast-preferences" %%
## 用 `prefers-contrast: more` 把客製捲軸換成高對比配色
- 做法：捲軸顏色放在 `--scrollbar-thumb`／`--scrollbar-track` 變數，經 `scrollbar-color` 套用；`@media (prefers-contrast: more)` 裡改成純黑拇指配白軌道
- 對手：缺——指南只說開啟高對比的使用者期待強烈的前後景分隔，而不是淡灰或主題色，沒說低對比捲軸在哪個時刻出問題
- 退路：保住主要行為——退回 `::-webkit-scrollbar` 或原生系統捲軸，僅失去標準化自訂配色
- 解鎖：用標準 `scrollbar-color` 搭 `prefers-contrast: more`，讓品牌捲軸在高對比模式下自動切換黑白

經過：品牌主題的捲軸是淡灰配更淡的灰，好看但難找。開了高對比的使用者，這時會看到黑白分明的版本，其他人照舊。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：scrollbar-color：Baseline Newly available（2025-12-12 起），Supported by: Chrome 121, Edge 121, Firefox 64, Safari 26.2
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前捲軸配色只能靠 `-webkit-` 偽元素、Firefox 另寫一套 → 現在程式碼編輯器、聊天側欄、資料表可以讓捲軸跟主題同色，同時在使用者要求高對比時自動換成黑白
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:adapt-scrollbar-to-contrast-preferences:2" %%
## 覆蓋式捲軸的軌道可能透明，拇指顏色要同時對軌道與容器背景有對比
- 做法：挑拇指顏色時，同時對照軌道色與捲動容器本身的背景色，不靠軌道把拇指框出來
- 對手：覆蓋式捲軸（例如 macOS 預設）只在捲動時替拇指上色，軌道可能維持透明，只和軌道色有對比的拇指會融進容器背景（引用："With overlay scrollbars (such as the macOS default), `scrollbar-color` styles the thumb while scrolling, whereas the track may remain transparent."）
- 退路：保住主要行為——退回 `::-webkit-scrollbar` 或系統預設捲軸仍可捲動，僅失去標準樣式控制
- 解鎖：（缺）

經過：在 Windows 上調好的高對比捲軸，拇指和淺灰軌道對比足夠；到了覆蓋式捲軸的環境，軌道透明，拇指直接疊在背景上，顏色一接近就看不見。指南要求拇指對兩者都要有對比。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：scrollbar-color：Newly（2025-12-12 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 備註：v1.0.1 另加一條提醒：計算值不是 `auto` 的 `scrollbar-width` 或 `scrollbar-color`（含繼承來的）會停用 `::-webkit-scrollbar`，所以退路區塊要在 `@supports not (scrollbar-color: auto)` 裡把 `scrollbar-width` 重設回 `auto`（同見 customize-scrollbar-color-and-thickness、dark-mode）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18（v1.0.1）上游刪除「macOS 預設忽略 scrollbar-color、須搭 scrollbar-width 與 scrollbar-gutter」的說法，對手改為覆蓋式捲軸的透明軌道，做法刪去 `scrollbar-width`／`scrollbar-gutter`；2026-11-18 對手組由「新功能的副作用」改為「焦點或狀態指示消失」

%% line-start id="mwg:adapt-scrollbar-to-contrast-preferences:3" %%
## 不要對 `scrollbar-color` 做動畫或過渡
- 做法：切換主題或高對比時直接換值，不加 `transition`
- 對手：WebKit 的 bug 讓 `scrollbar-color` 每次改變時捲軸都會閃爍（引用："A [WebKit bug](https://bugs.webkit.org/show_bug.cgi?id=311752) causes the scrollbar to flicker every time `scrollbar-color` changes."）
- 退路：保住主要行為——退回 `::-webkit-scrollbar` 或預設捲軸仍可正常顯示與切換，不會閃爍
- 解鎖：（缺）

經過：主題切換時給捲軸加了 0.2 秒的淡入，Safari 上捲軸跟著閃了好幾下。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：scrollbar-color：Newly（2025-12-12 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：舊式 `::-webkit-scrollbar` 退路要包在 `@supports not (scrollbar-color: auto)` 裡，以免兩套同時生效時互相衝突
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
