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
## macOS 上 `scrollbar-color` 要搭 `scrollbar-width` 才會生效，拇指也不能靠軌道顏色才看得見
- 做法：自訂顏色時一併設 `scrollbar-width`（`thin` 或 `auto`）；要顯示軌道底色再加 `scrollbar-gutter: stable`；拇指顏色要能在透明軌道上單獨辨識
- 對手：macOS 使用覆蓋式捲軸，預設忽略 `scrollbar-color` 與 `::-webkit-scrollbar`；即使生效，軌道預設透明、只在滑過時出現（引用："On macOS, `scrollbar-color` (standard) and `::-webkit-scrollbar` (legacy) properties are ignored by default because macOS uses native "overlay" scrollbars."）
- 退路：保住主要行為——退回 `::-webkit-scrollbar` 或系統預設捲軸仍可捲動，僅失去標準樣式控制
- 解鎖：（缺）

經過：在 Windows 上調好的高對比捲軸，到 Mac 上完全沒變；好不容易出現了，拇指又和透明軌道後面的背景混在一起。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：scrollbar-color：Newly（2025-12-12 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

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
