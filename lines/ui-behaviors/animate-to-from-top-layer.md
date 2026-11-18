---
guide: animate-to-from-top-layer
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/animate-to-from-top-layer.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 進出頂層的動畫

%% line-start id="mwg:animate-to-from-top-layer" %%
## 用 `overlay` 與 `allow-discrete` 讓 dialog 與 popover 進出頂層都有動畫
- 做法：`dialog`、`[popover]` 的基礎狀態寫關閉時的值，`transition-property` 列入 `display` 與 `overlay`，另寫 `transition-behavior: allow-discrete`；在開啟狀態的選擇器裡（或之後）放 `@starting-style`；`::backdrop` 也一樣過渡；縮放只在 `prefers-reduced-motion: no-preference` 時套用
- 對手：頂層元素在 `display: none` 與可見之間切換，一直很難動畫；離場時沒過渡 `overlay`，元素會提早離開頂層，被其他元素或視窗裁掉（引用："This ensures the element stays in the top layer for the duration of the animation, preventing it from being clipped by other elements or the viewport prematurely."）
- 退路：保住主要行為——Firefox／Safari 退回 `data-closing` 仍保進場與對話框離場動畫，僅 popover 輕點關閉無動畫
- 解鎖：用 `overlay` 與 `allow-discrete` 讓原生 `<dialog>` 與 `popover` 進出頂層都能做動畫而不被裁切

經過：原生 `<dialog>` 開關都是瞬間的，很多人因此改用自製 modal。現在開啟可以淡入縮放、背景漸暗，關閉時元素也能留在頂層直到動畫結束；只是離場目前只有 Chromium 原生做得到。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：@starting-style：Newly（2024-08-06）；overlay：Limited availability，Supported by: Chrome 117, Edge 117，Unsupported in: Firefox, Safari；transitionable display：Limited（Chrome 117, Edge 117, Safari 18）；Popover：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前想要有動畫的對話框就得放棄原生 `<dialog>` → 現在確認框、側邊抽屜、浮動選單可以保留原生的焦點管理、Esc 關閉與頂層行為，同時有淡入縮放與背景漸暗。離場動畫目前僅 Chromium 原生
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:animate-to-from-top-layer:2" %%
## 不要只靠 `CSS.supports()` 判斷能不能過渡 `display`
- 做法：用暫時的探針元素實測 `display` 過渡是否生效，並同時檢查 `CSS.supports('overlay', 'auto')`；在需要時才延遲評估（探針需要 `document.body`）；不支援時改走 `data-closing` 退路，並把 `cancel` 事件（Esc、`closedby`）導到同一個關閉函式
- 對手：Firefox 129+ 認得 `transition-behavior: allow-discrete`（`CSS.supports()` 回傳 true），實際上不過渡 `display`，元素離場時立刻消失（引用："Firefox 129+ parses `transition-behavior: allow-discrete` (`CSS.supports('transition-behavior', 'allow-discrete')` returns `true`) without actually transitioning the `display` property"）
- 退路：保住主要行為——改以 `overlay` 支援與探針實測分流，讓 Firefox／Safari 走 `data-closing` 保住離場動畫
- 解鎖：（缺）

經過：偵測說支援，對話框卻直接消失。對頂層元素還要多查一個 `overlay`，兩者都成立才能放心交給 CSS。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：transitionable display、overlay：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:animate-to-from-top-layer:3" %%
## `allow-discrete` 不要寫進 `transition` 簡寫
- 做法：另寫一條 `transition-behavior: allow-discrete`，放在 `transition` 之後
- 對手：把 `allow-discrete` 寫進 `transition` 簡寫，舊瀏覽器會忽略整條 `transition` 宣告（引用："it will make older browsers ignore the entire `transition` declaration."）
- 退路：保住主要行為——拆開宣告後，舊瀏覽器仍保留透明度等一般屬性過渡而不整條丟棄
- 解鎖：（缺）

經過：和一般元素的進出場一樣，一個新關鍵字就能讓舊瀏覽器把整條過渡丟掉。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：transition-behavior：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：`@starting-style` 要放在開啟狀態選擇器裡或之後；`@starting-style` 不能拿來寫離場；popover polyfill 的兩個坑（與前幾批一致，不另拆）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「不認得的語法讓整條規則失效」
