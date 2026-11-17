---
guide: scroll-snap-state-sync
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/scroll-snap-state-sync.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 捲動吸附狀態同步

%% line-start id="mwg:scroll-snap-state-sync" %%
## 用 `scrollsnapchange` 在捲動停到新段落時同步目錄高亮
- 做法：容器設 `scroll-snap-type`、段落標題設 `scroll-snap-align: start`，監聽 `scrollsnapchange`，以 `event.snapTargetBlock` 更新側欄目錄的作用中連結
- 對手：指南只說以前要寫複雜的 scroll 監聽、手算捲動偏移與 IntersectionObserver，沒說這些做法在哪個時刻出錯（引用："traditionally required complex scroll event listeners, manual calculations of scroll offsets, and intersection observers."）
- 退路：保住主要行為——偵測不支援時改用 IntersectionObserver 追蹤頂端標題，只差在捲動途中就會更新狀態
- 解鎖：在捲動容器停到新吸附目標時自動同步側欄目錄或頁碼高亮，不必寫複雜的偏移計算或觀察器

經過：長文配側欄目錄，讀到哪一節目錄就亮哪一節，以前得自己算。吸附事件把「停在哪」直接交給你，但跨瀏覽器仍得留一份觀察器版本。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll snap events：Limited availability，Supported by: Chrome 129, Edge 129；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「現在停在哪一段」要自己算偏移 → 現在投影片式文件、分章節的說明頁、直式短影音列表可以在停下時同步頁碼、目錄或播放狀態。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-snap-state-sync:2" %%
## 吸附事件只同步畫面，作用中狀態要另外用 `aria-current` 告訴輔助技術
- 做法：目錄連結作用中時設 `aria-current="true"` 或 `"location"`，並把目錄包在有名稱的 `<nav>` 裡
- 對手：捲動吸附事件讓畫面同步，但不會自動把這些資訊暴露給程式（引用："it does not automatically expose that information programmatically."）
- 退路：不需要——aria-current 與導覽地標屬既有語意屬性，不論走原生事件或觀察器退路皆可同步標註
- 解鎖：（缺）

經過：視覺上目錄亮了第三節，讀屏使用者聽到的每個連結都一樣，不知道自己在哪。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：aria-current：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-snap-state-sync:3" %%
## 段落比畫面長時小心 `mandatory` 吸附
- 做法：長文的段落吸附用 `scroll-snap-type: y proximity`，不要隨手用 `mandatory`
- 對手：`mandatory` 會讓吸附點之間、比畫面還長的內容讀不到（引用："it can cause content in-between snap-points to become inaccessible when longer than the screen."）
- 退路：不需要——Scroll snap 已廣泛支援，一律改用 y proximity 即可在所有瀏覽器防止跳過長段落
- 解鎖：（缺）

經過：一節內容比螢幕長，往下捲就被硬拉到下一節的標題，中間那半段永遠看不到。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Scroll snap：Baseline Widely available（2020-01-15 起）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：目錄跳轉的目標標題加 `tabindex="-1"`，捲動容器要可聚焦並有名稱與角色
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
