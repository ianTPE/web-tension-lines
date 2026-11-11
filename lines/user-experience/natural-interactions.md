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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `:focus-visible` 顯示鍵盤焦點框，只在滑鼠點擊時不顯示
- 被什麼擋：`outline: none` 直接拿掉焦點框，鍵盤使用者看不到自己在哪（引用："DO NOT remove focus outlines (`outline: none` or `outline: 0`) without providing an equally visible replacement with at least a 3:1 contrast ratio against the page (WCAG 1.4.11)."）
- 戰報：勝——`:focus-visible` 為 Widely，滑鼠點擊不出框、鍵盤操作有框（官方宣稱）

經過：拿掉焦點框通常是為了點擊後不要出現難看的框。`:focus-visible` 把兩種需求分開，不必為了美觀犧牲鍵盤使用者。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：—
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:natural-interactions:2" %%
## 選單可以 hover 開，但不能只靠 hover
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：下拉選單用 `<button popovertarget>` 宣告式觸發，點擊、觸控、鍵盤都能開，`Esc` 關閉
- 被什麼擋：只在 hover 時開選單，鍵盤和觸控使用者打不開（引用："Menus and dropdowns may open on hover, but never only on hover: they also open on click, tap, and keyboard activation, stay open while the pointer moves onto them, and close with Esc (WCAG 2.1.1, 1.4.13)."）
- 戰報：部分改善——popover 內建點擊、鍵盤與關閉行為；popover 為 Newly，舊瀏覽器要 polyfill（官方宣稱）

經過：和 single-line-overflow 的 `title` 線同一組：只對滑鼠有效的互動。宣告式 popover 讓開關行為由瀏覽器提供，不必自己補鍵盤與觸控。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：Popover：Newly（2025-01-27）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
