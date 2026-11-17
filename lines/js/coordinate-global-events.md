---
guide: coordinate-global-events
category: js
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/js/coordinate-global-events.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Temporal 協調跨時區事件

%% line-start id="mwg:coordinate-global-events" %%
## 用 ZonedDateTime 的 disambiguation 偵測日光節約跳過或重複的時刻
- 做法：`Temporal.ZonedDateTime.from()` 建立有時區的時間；`disambiguation: 'reject'` 在時刻不存在或重複時丟 `RangeError` 以警告使用者，`'compatible'` 自動挑一個合理時間；`.withTimeZone()` 換算其他城市
- 對手：日光節約轉換時，某些時刻會被跳過或重複，舊 `Date` 很難安排這類跨時區事件（引用："especially around Daylight Saving Time (DST) transitions when hours can be skipped or repeated."）
- 退路：保住主要行為——Safari 沒有原生 API 時動態載入 temporal-polyfill，時刻不存在的警告照樣做得出來
- 解鎖：有——以前日光節約跳過或重複的時刻只能自己算風險；現在建立有時區的時間時可直接指定跳過時刻就丟錯

經過：會議排在紐約 2025-03-09 02:30，那一刻因為日光節約根本不存在。`'reject'` 讓排程介面能直接提示「這個時間落在時鐘調整的空隙」，再用 `withTimeZone` 給東京與會者看對應時間。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability。Supported by: Chrome 144, Edge 144, Firefox 139；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：跨國團隊的排程工具可以在使用者選到「不存在」或「出現兩次」的時刻時當場提醒，並同時列出每位與會者的當地時間。Safari 要 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 1 個糾錯提醒未拆：顯示時間用 `toLocaleString()`，不要手動補零。
