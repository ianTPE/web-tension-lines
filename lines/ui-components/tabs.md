---
guide: tabs
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/tabs.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 分頁介面（Tabs）

%% line-start id="mwg:tabs" %%
## 用 focusgroup 取代手寫 roving tabindex
- 做法：在 tablist 上用 `focusgroup`，自動得到正確角色與方向鍵移動
- 對手：（缺）只說要取代手動實作 roving tabindex 或 activedescendant，沒說手寫版在哪個情境出錯（引用："Instead of manually implementing a roving tabindex or ARIA activedescendant pattern to meet the focus management requirement of the ARIA `tablist` role, we can use `focusgroup`"）
- 退路：保住主要行為——不支援時載入 `@microsoft/focusgroup-polyfill`，保留 tablist 角色與方向鍵移動
- 解鎖：不必手寫 roving tabindex 或 activedescendant，`focusgroup` 會自動設定 tablist 與 tab 角色

經過：分頁的鍵盤模型（只有一個 Tab 停點，方向鍵切換）一向要自己寫。新屬性讓瀏覽器代勞，但對手只被描述成「要手動實作」，屬於工作量而不是可觀察的失敗。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：focusgroup：Limited（Chrome/Edge 150；Firefox、Safari 不支援）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：一組元素「只有一個 Tab 停點、方向鍵在裡面移動」可以用一個屬性宣告，不必手寫 roving tabindex。鍵盤優先的介面（格狀選單、看板）門檻大降；目前僅 Chromium
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:tabs:2" %%
## 選中底線用偽元素邊框，強制色彩下不消失
- 做法：用偽元素上的 border 畫選中分頁的底線，並以 `aria-selected` 為樣式依據
- 對手：用 `box-shadow` 或背景畫底線，強制色彩模式把兩者都移除，選中狀態完全沒有指示（引用："DO NOT use `box-shadow` or a background: forced colors mode removes both, leaving no indicator."）
- 退路：不需要——偽元素 border 與 `aria-selected` 已 Widely，不必退路
- 解鎖：（缺）

經過：高對比模式使用者看到的分頁是一排一模一樣的按鈕。指南也要求不能只用顏色區分選中（WCAG 1.4.1），且樣式綁 `aria-selected`，讓視覺與無障礙狀態不會不一致。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：—
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:tabs:3" %%
## 分頁不換行，放不下時捲動或收進選單
- 做法：分頁保持單列，放不下時用水平捲動加淡出提示、或收進「More」選單
- 對手：分頁換成多列，Tab 順序與選中的分頁都難以追蹤（引用："DO NOT wrap them onto multiple rows: wrapped rows make the tab order and the selected tab hard to follow."）
- 退路：保住主要行為——不支援捲動動畫時改用陰影或 IntersectionObserver 提示，不支援 `interpolate-size` 時立即縮放，分頁仍可單列捲動
- 解鎖：捲動驅動動畫可讓分頁列邊緣淡出隨捲動位置增減，內容放得下時自動消失

經過：分頁太多時直覺是讓它換行，但換行後選中的分頁可能跑到第二列，視覺上的「目前位置」消失。指南給三種策略並交代各自的 fallback。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：Scroll-driven animations：Newly（2026-10-27）；hidden="until-found"：Limited；interpolate-size：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：捲動容器的邊緣淡出可以跟捲動位置連動、到底就消失，純 CSS。很多分頁、很多標籤的列可以不換行也不讓人迷路
- 變更紀錄：2026-11-11（v1.0.0）首次拆出；2026-11-18 改為槽 v2
