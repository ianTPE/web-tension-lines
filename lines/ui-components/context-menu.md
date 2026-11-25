---
guide: context-menu
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/context-menu.md
first_seen: 2026-11-25（v1.0.2）
license: CC-BY-4.0（上游指南）
---

# 右鍵選單

%% line-start id="mwg:context-menu" %%
## 用零尺寸錨點加錨點定位把右鍵選單開在游標處，不手算座標
- 做法：在卡片裡、可見按鈕正前方放一個零尺寸、`position: fixed` 的隱形錨點；`contextmenu` 事件只擋掉瀏覽器預設選單，`pointerup` 時把錨點移到 `clientX`／`clientY`，再呼叫 `popover.showPopover({ source: menuAnchor })`；選單用 `position-area: block-end span-inline-end` 加 `position-try: flip-inline, flip-block, flip-start`
- 對手：用 JavaScript 算 `inset` 座標擺選單，不會處理溢出，在視窗邊緣按右鍵時選單會超出畫面（引用："you must manually calculate the `inset` coordinates of the popover in JavaScript … but note that this does not handle overflow."）
- 退路：失去主要好處——改用腳本把選單擺在點擊處，失去溢出時的自動翻邊
- 解鎖：右鍵選單可以對齊游標位置，又由 CSS 錨點定位避免溢出

經過：看板卡片的右鍵選單以前讀滑鼠座標直接擺上去，點在右下角時選單就跑出視窗，得再自己算邊界。現在只把一個看不見的點移到游標，翻邊交給 CSS。沒有錨點定位的瀏覽器仍會退回手算座標，溢出問題照舊。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：Anchor positioning：記 Newly（核心屬性 2026-01-13 起 Baseline）。指南寫 "Browser support for Anchor positioning: Limited availability. Supported by: Chrome 157 (Nov 2026), Edge 157 (Nov 2026), and Safari 27 (Sep 2026). Unsupported in: Firefox."，群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線未用 `position-visibility`。Popover：Newly（2025-01-27）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前自製右鍵選單要自己算座標與碰撞 → 現在網頁版檔案管理器、看板、畫布編輯器、地圖標點都可以做出貼著游標、靠邊自動翻面的右鍵選單，定位只靠 CSS。與 `mwg:menu:4` 同一招，這份指南補上完整的右鍵觸發流程
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:context-menu:2" %%
## 右鍵選單之外再放一顆一直看得見的按鈕，共用同一個選單
- 做法：每個項目放一顆 `command="toggle-popover"`、`commandfor` 指向同一個選單的按鈕，`aria-label` 帶上項目名稱，`aria-expanded` 跟著 popover 狀態更新；按鈕一直顯示，不等 hover 或聚焦才出現
- 對手：長按不一定會觸發右鍵選單，iOS Safari 就不會，只靠右鍵時觸控使用者打不開（引用："On some platforms (though notably not iOS Safari) this may also be triggered with a long press, but that is not a universal behavior."）
- 退路：保住主要行為——不支援 Invoker Commands 時改用 `popovertarget`，按鈕照樣開選單
- 解鎖：（缺）

經過：刪除、分享都收在右鍵選單裡，桌機上很順手，iPhone 使用者長按卡片卻什麼都沒出來。多一顆「⋯」按鈕，觸控、鍵盤與語音控制都走得到同一份選單。只有右鍵的版本，指南只接受項目可先選取、同樣動作別處也有的情況。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Invoker commands：Newly（2025-12-12），Supported by: Chrome 135, Edge 135, Firefox 144, Safari 26.2；Popover：Newly（2025-01-27）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-25（v1.0.2）首次拆出

%% line-start id="mwg:context-menu:3" %%
## 用 `ToggleEvent.source` 分辨選單是右鍵還是按鈕打開的
- 做法：在 popover 的 `beforetoggle` 讀 `event.source`，把來源元素的標籤名寫成選單上的屬性，再用 `[popover][source="button" i]` 給按鈕開啟時不同的 `position-area`
- 對手：（缺）指南只說這樣可以依來源調整位置，沒說分不出來源時出了什麼事（引用："To differentiate between the source, for instance to adjust the positioning, check `event.source` in the popover's `beforetoggle` event"）
- 退路：保住主要行為——沒有 `source` 時改在各觸發點的監聽裡設 `position-area`
- 解鎖：同一個選單可依是誰打開它，換不同的位置與樣式

經過：同一份選單，右鍵打開要對齊游標，按「⋯」打開要對齊按鈕另一側。開啟事件自己帶著來源，選單就能在一處決定擺法，不必每個觸發點各記一次。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：ToggleEvent source：Newly（2026-05-11），Supported by: Chrome 140, Edge 140, Firefox 145, Safari 26.5
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前一個彈出層被多個入口共用時，要另外記是誰開的 → 現在一張動作選單、說明卡或顏色面板可以掛在多個入口上，依來源換位置、換標題，開啟邏輯只寫一處
- 註：指南的退路範例程式有誤：`!'source' in ToggleEvent.prototype` 會先算 `!'source'`，條件永遠為假；`style.setAttribute()` 也不是 CSSStyleDeclaration 的方法。退路分類依指南的文字說明判定，照抄範例不會生效
- 另有 5 個糾錯提醒未拆：右鍵選單不要跨項目共用、各有唯一 id；按鈕至少 24×24 CSS 像素；開啟後在 `toggle` 裡把焦點移到第一顆可用按鈕（同 `mwg:menu:6`）；popover polyfill 載入前用 `@supports not selector(:popover-open)` 先藏住 popover；focusgroup polyfill 不會注意到後來才隱藏或顯示的項目，要加 `focusgroup="none"`
- 變更紀錄：2026-11-25（v1.0.2）首次拆出
