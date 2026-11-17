---
guide: progress
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/progress.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 自訂樣式的進度條

%% line-start id="mwg:progress" %%
## 原生 `<progress>` 要嘛只用安全屬性，要嘛 `appearance: none` 整套重做，別半調子
- 做法：用原生 `<progress>`（`max`、`value`、`<label for>`）；輕度樣式只用 `accent-color`、`inline-size`、`writing-mode`、`opacity`、`filter` 這類；需要更多時 `appearance: none`、`border: 0 solid`、`overflow: clip`，軌道畫在元素本身，填色畫在 `::-webkit-progress-value`／`::-moz-progress-bar`
- 對手：`border-radius`、`background`、`border` 這類屬性會默默關掉預設的進度條樣式（引用："Certain properties (e.g. `border-radius`, `background`, `border`) will silently disable the default progress bar styling."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：只是想把進度條改成圓角，加了 `border-radius` 之後填色整個不見，變成一條灰色長方形。
%% line-end %%

### 細節（不索引）
- 對手組：簡寫或屬性連動重設
- 支援狀態：`<progress>`、`appearance: none`：指南未給支援資料，記 不適用；accent-color：指南記 Limited availability（Chrome 93, Edge 93, Firefox 92, Safari 26.2）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress:2" %%
## `-webkit-` 與 `-moz-` 進度條偽元素分開寫，不要放在同一條規則
- 做法：`::-webkit-progress-value` 與 `::-moz-progress-bar` 各寫一條規則、各出現一次；狀態差異用 `progress` 上的自訂屬性傳進去
- 對手：合在同一個選擇器清單時，瀏覽器不認得另一家的偽元素，整條規則被判無效而忽略；`:is()`、`:where()` 也救不了（引用："The rule will be deemed invalid and will be ignored. `:is()` and `:where()` do not help here, as they don't support pseudo-elements."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：為了少寫幾行把兩個偽元素用逗號併在一起，結果 Chrome 和 Firefox 的填色同時失效。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress:3" %%
## 不確定進度的滑塊用 `translate` 配 `cqi` 移動，不用 margin 或 `scale`
- 做法：`progress` 設 `container-type: inline-size`；keyframes 用真的 `inline-size` 定長度、`translate: -100%` 到 `100cqi` 移動，`from, to` 加 `margin-right: auto`；RTL 在 `:dir(rtl)` 反轉動畫
- 對手：用 margin 移動在 RTL 會壞：Firefox 只看實體左邊距，滑塊根本不動；Chromium／WebKit 的 margin 超過軌道時左邊距被忽略，滑塊跳到邊緣；用 `scale` 改長度又會扭曲填色上的圖樣（引用："Firefox positions the indeterminate fill using only its physical left margin, so `margin-inline-start` has no effect in RTL and the fill never moves."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：阿拉伯文介面上的載入條，Firefox 裡滑塊停在原地不動，Chrome 裡滑塊一跳一跳。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：container query 單位、`translate`：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress:4" %%
## 減少動態時把不確定進度的動畫放慢，不要 `animation: none`
- 做法：在 `prefers-reduced-motion: reduce` 下把 `--progress-bar-indeterminate-animation-duration` 拉長到 10s
- 對手：不確定狀態的填色只靠動畫存在，關掉動畫後在 Chromium 留下寬度為零的填色（引用："Never disable the indeterminate animation (`animation: none` leaves a zero-width fill in Chromium)."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：為了尊重減少動態設定把動畫關掉，結果進度條變成一條空軌道，看起來像卡住。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress:5" %%
## 用 `revert-rule` 讓動畫變數沒設定時不覆蓋任何東西
- 做法：偽元素上寫 `animation: var(--progress-bar-animation, revert-rule)`，只有設了變數（例如不確定狀態或決定狀態的閃光效果）才覆蓋動畫
- 對手：缺——指南只說這樣「最大化可組合性」，沒說不用 `revert-rule` 時在哪個時刻出錯
- 退路：保住主要行為——不支援 `revert-rule` 時，未設變數仍是無害的無動畫狀態
- 解鎖：動畫掛鉤可用 `revert-rule` 只在有設值時覆蓋預設動畫

經過：元件庫想讓使用者自己加閃光動畫，又不想在沒加時蓋掉預設行為。`revert-rule` 讓「沒設定」真的等於沒寫。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：revert-rule：Baseline Newly available（2026-09-14 起），Supported by: Chrome 148, Edge 148, Firefox 150, Safari 27
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「變數沒設就別覆蓋」要多寫一層選擇器或 `@supports` → 現在設計系統元件可以開放任意自訂屬性當掛鉤，沒用到的掛鉤完全不影響預設樣式
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress:6" %%
## 背景任務完成用 `role="status"` 播報，不要把焦點移到 `<progress>`
- 做法：不在 `<progress>` 上設 `tabindex` 或呼叫 `.focus()`；完成時更新一個 polite 的狀態元素
- 對手：`<progress>` 不可互動，把焦點移過去會打亂鍵盤使用者（引用："it is non-interactive and moving focus to it disrupts keyboard users."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：上傳一完成焦點就被拉到進度條上，使用者原本在填的欄位跟著失焦。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:progress:7" %%
## 載入中的區塊直接用 `hidden` 藏起來，不要在無名 `<div>` 上掛 `aria-busy` 加 `aria-describedby`
- 做法：區域內容還沒準備好時用 `hidden` 或 `aria-hidden="true"` 藏起來，進度本身交給有標籤的 `<progress>`
- 對手：`aria-busy` 的讀屏支援不一致，沒有角色也沒有名稱的 `<div>` 上的 `aria-describedby` 會被輔助技術忽略（引用："`aria-busy` has inconsistent screen reader support, and `aria-describedby` on an unnamed `<div>` without a role is ignored by assistive technologies."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：在載入中的卡片上掛了 aria-busy 和描述，讀屏照樣把半空的卡片唸出來，描述一個字也沒唸。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：`<progress>` 內的替代文字不會被使用；客製後要確認填色與軌道的對比；與內容並排的不確定動畫可能讓人分心
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
