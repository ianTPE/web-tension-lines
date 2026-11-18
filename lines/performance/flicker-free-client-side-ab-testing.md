---
guide: flicker-free-client-side-ab-testing
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/flicker-free-client-side-ab-testing.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 不閃爍的前端 A/B 測試

%% line-start id="mwg:flicker-free-client-side-ab-testing" %%
## 用 blocking="render" 讓實驗腳本在第一次繪製前跑完，取代整頁隱藏的防閃爍片段
- 做法：把實驗腳本放在 `<head>`，加 `async`（外部檔）或 `type="module"`（內嵌）再加 `blocking="render"`；動態插入的變體樣式表也加 `blocking="render"`；變體用 `<html>` 上的 data 屬性切換
- 對手：腳本在頁面開始建構後才改 DOM，使用者先看到原版再閃成變體；傳統防閃爍片段用 `opacity: 0` 把整頁藏到腳本跑完或約 4 秒逾時，犧牲漸進渲染、讓人誤點看不見的內容（引用："This approach sacrifices progressive rendering, allows accidental clicks on invisible content, and introduces unnecessary paint cycles."）
- 退路：失去主要好處——Firefox 退回 `opacity: 0` 防閃爍片段，仍犧牲漸進渲染並可能誤點隱藏內容
- 解鎖：用 `blocking="render"` 讓實驗腳本在首次繪製前跑完卻不擋解析，免去防閃爍片段

經過：A/B 工具的老問題是兩害取一：不擋就閃，擋就整頁白幾秒還可能被誤點。`blocking="render"` 讓腳本享有和樣式表一樣的阻擋渲染行為，只延後繪製、不延後解析。Firefox 仍需要舊片段。
%% line-end %%

### 細節（不索引）
- 對手組：內容要等JS才成形
- 支援狀態：blocking="render"：Limited availability。Supported by: Chrome 105, Edge 105, Safari 18.2；Unsupported in: Firefox
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：存在 localStorage 的主題、字級、語系偏好可以用一小段 render-blocking 模組在第一次繪製前套好，不再先閃一下預設樣式再跳成使用者的設定。Firefox 不支援
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:flicker-free-client-side-ab-testing:2" %%
## render-blocking 腳本慢或 CDN 掛掉，整頁就不會繪製
- 做法：render-blocking 的腳本只放套用變體的小 stub（例如執行時間 100ms 以內），追蹤與分析另外用 `async`／`defer` 載入；分析等不影響畫面的腳本不加 `blocking="render"`；效能關鍵頁考慮改在伺服器端分流
- 對手：渲染會一直等到腳本執行完，大或慢的腳本直接延後第一次繪製；第三方 CDN 故障時可能整頁不渲染，而且開發者沒有可控的逾時（引用："If the experiment SDK is hosted on a third-party CDN, a CDN outage could block rendering entirely."）
- 退路：保住主要行為——Firefox 忽略此屬性並退回有逾時控制的防閃爍或伺服器分流，不會無限卡死繪製
- 解鎖：（缺）

經過：把整包實驗 SDK 加上 `blocking="render"`，閃爍沒了，但每次都要等它下載完才看到頁面；SDK 主機一出事，整站白屏，而且只能等瀏覽器自己的逾時。
%% line-end %%

### 細節（不索引）
- 對手組：優化用過頭反傷
- 支援狀態：blocking="render"：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆（不要同時用 `blocking="render"` 與舊的防閃爍片段，只說會造成不必要的延遲）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「優化用過頭反傷」
