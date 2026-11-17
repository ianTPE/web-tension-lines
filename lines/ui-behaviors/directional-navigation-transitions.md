---
guide: directional-navigation-transitions
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/directional-navigation-transitions.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 有方向的導覽轉場

%% line-start id="mwg:directional-navigation-transitions" %%
## 用帶類型的 view transition 讓 SPA 換頁有前進後退方向
- 做法：`document.startViewTransition({ update, types: [direction] })` 傳入 `forward`／`backward`，CSS 用 `html:active-view-transition-type(forward)::view-transition-old(root)` 套對應的 `transform` 滑動動畫，`::view-transition-group(root)` 用非線性緩動
- 對手：SPA 換畫面時內容直接被替換，沒有任何轉場（引用："By default, the content is simply replaced, without any transitions."）
- 退路：失去主要好處——退回立即更新 DOM，畫面仍沒有方向性轉場
- 解鎖：單頁應用不必依賴動畫函式庫，就能依前進或後退方向滑動換頁並強化視圖間的空間方向感

經過：SPA 的「下一頁」只是把內容換掉，使用者感覺不到自己往哪走。把方向當成轉場類型傳進去，同一組 CSS 就能分出前進與後退。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：View transitions：Newly（2025-10-14）；Active view transition：Newly（2026-01-13）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前方向感要靠動畫函式庫加狀態管理 → 現在分步驟表單、投影片（上下）、商品瀏覽（左右）可以用一個 `types` 參數決定滑動方向
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:directional-navigation-transitions:2" %%
## 沒有 `startViewTransition` 時仍要直接更新 DOM
- 做法：導覽函式先檢查 `document.startViewTransition`，不存在就直接呼叫 `updateDOM()`
- 對手：不支援的瀏覽器裡 `document.startViewTransition` 是 `undefined`，沒做偵測就直接呼叫，畫面不會更新（引用："In unsupported browsers, `document.startViewTransition` will be `undefined`."）
- 退路：保住主要行為——能力偵測缺失時略過轉場並直接執行 DOM 更新，確保舊瀏覽器照常換頁不卡死
- 解鎖：（缺）

經過：轉場是加分項，換頁本身不是。把轉場包在偵測裡，壞掉的只會是動畫。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：View transitions：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：滑動用 `transform` 而非 inset 屬性；減少動態偏好下關掉 `::view-transition-group(root)` 動畫
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
