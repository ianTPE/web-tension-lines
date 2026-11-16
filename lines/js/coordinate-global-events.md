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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`Temporal.ZonedDateTime.from()` 建立有時區的時間；`disambiguation: 'reject'` 在時刻不存在或重複時丟 `RangeError` 以警告使用者，`'compatible'` 自動挑一個合理時間；`.withTimeZone()` 換算其他城市
- 被什麼擋：日光節約轉換時，某些時刻會被跳過或重複，舊 `Date` 很難安排這類跨時區事件（引用："especially around Daylight Saving Time (DST) transitions when hours can be skipped or repeated."）
- 戰報：部分改善——Temporal 讓衝突可偵測、解決方式可選擇；用 `PlainDateTime` 則無法處理日光節約；Safari 需 polyfill（官方宣稱）

經過：會議排在紐約 2025-03-09 02:30，那一刻因為日光節約根本不存在。`'reject'` 讓排程介面能直接提示「這個時間落在時鐘調整的空隙」，再用 `withTimeZone` 給東京與會者看對應時間。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability。Supported by: Chrome 144, Edge 144, Firefox 139；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：跨國團隊的排程工具可以在使用者選到「不存在」或「出現兩次」的時刻時當場提醒，並同時列出每位與會者的當地時間。Safari 要 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 1 個糾錯提醒未拆：顯示時間用 `toLocaleString()`，不要手動補零。
