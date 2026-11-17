---
guide: cross-document-transitions
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/cross-document-transitions.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 跨文件轉場

%% line-start id="mwg:cross-document-transitions" %%
## 用 `@view-transition` 讓多頁網站換頁也有轉場
- 做法：兩頁共用的樣式表在 `prefers-reduced-motion: no-preference` 裡寫 `@view-transition { navigation: auto; }`，再用 `::view-transition-old(root)`／`::view-transition-new(root)` 自訂滑出滑入
- 對手：指南只說能做出平順、像 app 的換頁轉場，沒說一般換頁在哪個時刻出問題（引用："create smooth, app-like transitions between different pages of a Multi-Page Application (MPA)"）
- 退路：保住主要行為——不支援跨文件轉場的瀏覽器退回標準即時換頁，網站核心導覽功能不受影響
- 解鎖：純多頁網站不必改成 SPA，加上 CSS 就能做出像應用程式般可自訂的平滑換頁轉場

經過：多頁網站換頁一直是整頁閃一下。現在兩頁各宣告一行就有轉場，不支援的瀏覽器照常換頁，沒有退路要寫。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：View transitions：Newly（2025-10-14）；Cross-document view transitions：Limited availability，Supported by: Chrome 126, Edge 126, Safari 18.2；Unsupported in: Firefox
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前要換頁有動畫就得改成 SPA → 現在純靜態產生的網站（文件站、作品集、週記站）加兩行 CSS 就有換頁轉場。Firefox 退回一般換頁
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:cross-document-transitions:2" %%
## 用轉場類型讓「返回」和「前進」方向相反
- 做法：頁面固定方向時在 `@view-transition` 寫 `types: previous`；要依來源決定時，在 `pagereveal` 裡用 `navigation.activation` 算出類型並 `e.viewTransition.types.add()`，再用 `:active-view-transition-type()` 套不同動畫
- 對手：所有換頁都用同一個效果時，回到首頁也和前往聯絡頁一樣從右邊進來，方向說不通（引用："When navigating back to the home page, it wouldn't make sense to have the same effect."）
- 退路：保住主要行為——缺 Navigation API 時改用其他判斷或預設類型，不支援跨文件轉場則退回一般換頁
- 解鎖：多頁網站能依導覽來源與前進後退方向切換不同轉場動畫，讓返回與前進有合理方向

經過：滑動轉場一做出來就會發現回上一頁也是「往前滑」。類型讓同一組頁面依導覽關係選動畫。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Cross-document view transitions：Limited；Navigation API：Newly（2026-01-13）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前多頁網站的轉場分不出方向 → 現在分步驟教學、相簿的上一張／下一張、系列文章可以各自往正確方向滑。Firefox 退回一般換頁
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
