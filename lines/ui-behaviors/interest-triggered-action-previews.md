---
guide: interest-triggered-action-previews
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/interest-triggered-action-previews.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 由興趣觸發的動作預覽

%% line-start id="mwg:interest-triggered-action-previews" %%
## 用 `interestfor` 在按下之前預覽動作效果
- 做法：按鈕或連結寫 `interestfor="目標id"`，目標上監聽 `interest`／`loseinterest`，依 `event.source` 套用或撤銷預覽；`:interest-source`／`:interest-target` 設樣式，`interest-delay-start`／`-end` 調延遲
- 對手：指南只說讓使用者在確定前先預覽動作會有幫助，沒說舊做法在哪個時刻出問題（引用："It can be beneficial to provide users a preview of their actions before they commit to them."）
- 退路：保住主要行為——偵測不支援時載入 interestfor polyfill 並配 `:is()` 與 CSS 變數，Firefox／Safari 也能預覽
- 解鎖：按鈕或連結加上屬性就能宣告興趣關係，不用自組 hover 與延遲腳本即可在確認前先預覽動作效果

經過：滑過「粗體」「斜體」就先看到效果，以前要自己接 hover、focus、離開與延遲。現在「興趣」是一種宣告好的關係，事件和延遲都由瀏覽器管。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：Interest invokers：Limited availability，Supported by: Chrome 149, Edge 149；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前預覽要手寫 hover/focus/延遲 → 現在主題挑選器、字體選單、濾鏡按鈕可以「滑過就試穿、離開就還原」，鍵盤聚焦也一樣。原生僅 Chromium，其他靠 polyfill
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interest-triggered-action-previews:2" %%
## 興趣觸發的預覽不要用 live region 播報
- 做法：預覽本身就是提示，不用 live region 播報套用與撤銷
- 對手：移動指標或 Tab 經過附近按鈕就會觸發興趣，套用／撤銷的播報很快變成噪音，蓋掉使用者真正在意的內容（引用："apply/unapply announcements quickly become noise that can drown out content the user actually cares about"）
- 退路：保住主要行為——不用 live region 播報，在原生與 polyfill 環境皆不製造讀屏噪音且預覽照常觸發
- 解鎖：（缺）

經過：滑鼠掃過一排按鈕，讀屏就連唸五次「正在預覽」；看不到預覽的人也不會因為聽到這句話而受益。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：Interest invokers：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：polyfill 下偽類要寫成 `:is(:interest-source, .interest-source)`，延遲要經 CSS 變數
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
