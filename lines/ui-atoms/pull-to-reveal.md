---
guide: pull-to-reveal
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/pull-to-reveal.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 下拉顯示

%% line-start id="mwg:pull-to-reveal" %%
## 用 `scroll-initial-target` 讓搜尋列一載入就藏在上方
- 做法：搜尋列放在捲動容器的第一個，主內容緊接在後並設 `scroll-initial-target: nearest`；容器 `scroll-snap-type: y mandatory`，兩者都 `scroll-snap-align: start`，讓搜尋列不是全露就是全藏
- 對手：以前靠 `scrollIntoView()` 或網址片段 `#content-id` 達成，指南只說兩者「有限制、不好做」，沒說在哪個時刻出問題（引用："both of which have limitations and are tricky to implement."）
- 退路：保住主要行為——不支援時用 `scrollIntoView()` 即時捲到主內容
- 解鎖：捲動容器可在初次渲染時直接停在主內容，把上方控制項藏起來

經過：手機 app 常見的「往下拉才出現搜尋」，在網頁上一直要等載入完再用 JS 捲一下。新屬性讓 CSS 直接宣告「一開始捲到這裡」。
%% line-end %%

### 細節（不索引）
- 對手組：內容要等JS才成形
- 支援狀態：scroll-initial-target：Limited availability。Supported by: Chrome 133, Edge 133。Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前初始捲動位置要等 JS 跑完才設定 → 現在收件匣、筆記列表、聊天紀錄可以一開就停在主內容，往上拉才露出搜尋、篩選或「載入更早的訊息」。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:pull-to-reveal:2" %%
## `scroll-initial-target` 不會移動鍵盤焦點
- 做法：目標若應該是鍵盤使用者的起點，自己呼叫 `element.focus()`
- 對手：這個屬性只移動視覺上的捲動位置，不移動鍵盤焦點（引用："This property only moves the **visual** viewport; it does not move the keyboard focus."）
- 退路：保住主要行為——不支援時用 `scrollIntoView()` 並自行設定鍵盤焦點
- 解鎖：（缺）

經過：畫面從主內容開始，Tab 卻從被藏起來的搜尋列開始，第一下按下去畫面就跳回頂端。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:pull-to-reveal，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:pull-to-reveal:3" %%
## 每個下拉動作都要有一顆可見的按鈕
- 做法：替每個下拉顯示的動作提供可見的按鈕（或選單項目），單擊或按 Enter 就完成同一件事；至少 24×24 CSS 像素，並以作用的對象命名
- 對手：只能靠下拉手勢叫出的功能，不符合 WCAG 2.5.1 對路徑型手勢的要求（引用："give every pull to reveal action a visible button (or menu item) that performs the same action with a single click or the Enter key, as WCAG 2.5.1 Pointer Gestures requires for path-based gestures."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：下拉是觸控螢幕上的手勢，滑鼠、鍵盤、開關裝置的使用者根本不知道上面藏了東西。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：按鈕：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：同一容器只能有一個 `scroll-initial-target`（多個時取 DOM 順序第一個）；網址片段與 `scroll-start` 優先於它
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
