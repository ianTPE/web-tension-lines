---
guide: scroll-target-on-load
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/scroll-target-on-load.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 設定初次渲染的捲動目標

%% line-start id="mwg:scroll-target-on-load" %%
## 用 `scroll-initial-target: nearest` 讓清單一開就停在指定項目
- 做法：在捲動容器裡要先露出的那個子元素設 `scroll-initial-target: nearest`（例如行事曆的今天、相簿的指定照片、動態牆的精選項目）
- 對手：以前靠 JS 的 `scrollIntoView()` 或網址片段 `#item-id`；指南只說兩者都有限制、不好做，沒說在哪個時刻出問題（引用："both of which have limitations and are tricky to implement."）
- 退路：保住主要行為——偵測不支援時在 DOMContentLoaded 用 scrollIntoView 即時定位，仍能停在目標項目
- 解鎖：只寫一行 CSS 就能在初次渲染時把容器捲到指定子項目，不必靠 JS 或網址片段處理中段起始位置

經過：行事曆一打開該停在今天，不是一月一日。屬性讓 CSS 直接宣告起始位置，不等腳本；Firefox、Safari 還是得留那段腳本。
%% line-end %%

### 細節（不索引）
- 對手組：內容要等JS才成形
- 支援狀態：scroll-initial-target：Limited availability，Supported by: Chrome 133, Edge 133；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「從中間開始」的捲動要等 JS 捲一下 → 現在月曆停在今天、聊天室停在最後一則已讀、時間軸停在現在，第一個畫面就對。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-target-on-load:2" %%
## `scroll-initial-target` 只動畫面，不動鍵盤焦點
- 做法：目標若也該是鍵盤使用者的起點，另外呼叫 `element.focus()`
- 對手：這個屬性只移動視覺上的捲動位置，鍵盤焦點留在原處（引用："This property only moves the **visual** viewport; it does not move the keyboard focus."）
- 退路：保住主要行為——鍵盤焦點本就須手動呼叫 focus() 移動，Firefox／Safari 的 JS 捲動退路一樣適用
- 解鎖：（缺）

經過：畫面停在今天，按一下 Tab 卻跳回頁首的第一個連結。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：scroll-initial-target：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-target-on-load:3" %%
## 初始目標前面的媒體要先給尺寸
- 做法：圖片與影片設 `aspect-ratio` 或固定的 `width`／`height`
- 對手：捲動位置在初次版面配置時計算，媒體載入後撐開高度，目標就被推離位置（引用："ensure images or videos have `aspect-ratio` or fixed `height`/`width` to prevent the target from shifting after the media loads."）
- 退路：保住主要行為——預先宣告媒體寬高比例屬基礎排版做法，原生與 DOMContentLoaded 退路皆不會被推走
- 解鎖：（缺）

經過：一開始確實停在精選項目，前面的圖片陸續載入後，它被一路往下推出畫面。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：scroll-initial-target：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-target-on-load:4" %%
## 網址片段與 `scroll-start` 會蓋過 `scroll-initial-target`，同一容器只設一個
- 做法：同一個捲動容器只給一個元素設 `scroll-initial-target`；記得網址片段與容器的 `scroll-start` 優先
- 對手：多個元素都設時瀏覽器只取 DOM 順序的第一個；網址帶片段時屬性被忽略（引用："A URL fragment (e.g., `example.com/#top`) and the container-level `scroll-start` property both take precedence over `scroll-initial-target`."）
- 退路：保住主要行為——單一目標規則在原生與 querySelector JS 退路下結果一致，網址片段亦同樣優先
- 解鎖：（缺）

經過：分享出去的連結帶了 `#top`，收到的人打開時清單停在最上面，而不是精選項目。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：scroll-initial-target：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：載入時需要平滑捲動動畫就不要用它（屬性是瞬間定位）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
