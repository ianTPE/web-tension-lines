---
guide: natural-interactions
category: user-experience
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/user-experience/natural-interactions.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 自然的互動回饋

%% line-start id="mwg:natural-interactions" %%
## 拿掉焦點框時一定要給同樣明顯的替代
- 做法：用 `:focus-visible` 顯示鍵盤焦點框，只在滑鼠點擊時不顯示
- 對手：`outline: none` 直接拿掉焦點框，鍵盤使用者看不到自己在哪（引用："DO NOT remove focus outlines (`outline: none` or `outline: 0`) without providing an equally visible replacement with at least a 3:1 contrast ratio against the page (WCAG 1.4.11)."）
- 退路：不需要——:focus-visible 與高對比焦點外框已廣泛支援，直接套用即可同時顧及美觀與鍵盤可及性
- 解鎖：（缺）

經過：拿掉焦點框通常是為了點擊後不要出現難看的框。`:focus-visible` 把兩種需求分開，不必為了美觀犧牲鍵盤使用者。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：—
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:natural-interactions:2" %%
## 選單可以 hover 開，但不能只靠 hover
- 做法：下拉選單用 `<button popovertarget>` 宣告式觸發，點擊、觸控、鍵盤都能開，`Esc` 關閉
- 對手：只在 hover 時開選單，鍵盤和觸控使用者打不開（引用："Menus and dropdowns may open on hover, but never only on hover: they also open on click, tap, and keyboard activation, stay open while the pointer moves onto them, and close with Esc (WCAG 2.1.1, 1.4.13)."）
- 退路：保住主要行為——偵測缺 popover 時條件載入 polyfill 或改用手動 JS 退路，點擊、觸控、鍵盤與 Esc 照常可用
- 解鎖：只用 HTML popovertarget 宣告就能讓選單內建點擊、觸控、鍵盤與 Esc 關閉行為而不必寫 JS

經過：和 single-line-overflow 的 `title` 線同一組：只對滑鼠有效的互動。宣告式 popover 讓開關行為由瀏覽器提供，不必自己補鍵盤與觸控。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：Popover：Newly（2025-01-27）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：下拉、浮層用 `popovertarget` 宣告就有點擊、鍵盤、Esc、點外面關閉，從觸發點長出來的動畫也只要 CSS
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
