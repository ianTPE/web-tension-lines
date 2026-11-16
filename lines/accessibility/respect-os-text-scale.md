---
guide: respect-os-text-scale
category: accessibility
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/accessibility/respect-os-text-scale.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 尊重作業系統的文字縮放

%% line-start id="mwg:respect-os-text-scale" %%
## 用 meta text-scale 讓頁面跟著系統字級放大
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `<head>` 放 `<meta name="text-scale" content="scale">`，字級、間距用 `rem`／`em`，行高用無單位值
- 被什麼擋：使用者在 iOS／Android 設定了大字級，行動瀏覽器預設不理會，頁面字級不變（引用："By default, mobile browsers ignore these OS-level accessibility settings to prevent legacy, fixed-pixel websites from breaking visually."）
- 戰報：僵持——只有 Chrome／Edge 146 支援；Firefox、Safari 退回預設字級，使用者只能手動縮放或雙指放大（官方宣稱）

經過：瀏覽器為了保護用固定 px 排版的老網站，選擇忽略系統字級。meta 是頁面主動宣告「我的版面撐得住」，瀏覽器才把系統比例套到 `1rem`。宣告之後還不能自己改 `:root` 的 `font-size`，也不能再用 `env(preferred-text-scale)` 手動乘一次，否則會擋掉或重複縮放。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：<meta name="text-scale">：Limited（Chrome 146、Edge 146；Firefox、Safari 不支援）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：網頁可以像原生 app 一樣直接吃到手機的系統字級（Dynamic Type），長輩或低視力使用者不必每個網站各自調整。文件、閱讀類網頁最受益；目前僅 Chrome／Edge 146 起
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:respect-os-text-scale:2" %%
## 流體字級要帶 rem 成分，不能只用 vw
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：流體字級寫成 `clamp(2rem, 1.25rem + 2vw, 4rem)`，讓字級同時有字型相對與視窗相對的部分
- 被什麼擋：只用 `font-size: 5vw`，字級不會完整回應使用者的文字縮放（引用："The font size does not respond fully to user text scaling"）
- 戰報：勝——混入 `rem` 成分後，系統字級與瀏覽器縮放都會影響字級（官方宣稱）

經過：純 vw 字級只跟視窗寬度走，使用者把字放大，標題卻不動。指南也給了經驗法則：最大字級不超過最小的 2.5 倍，並要測 200% 文字放大與 320 CSS px 寬的重排。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：—（指南只給 meta text-scale 的支援資料；`clamp()`／`rem` 未給）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:respect-os-text-scale:3" %%
## 開了 text-scale 就不要在 html 上寫死 font-size
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：根字級交給瀏覽器，不在 `:root`／`html` 宣告任何 `font-size`（絕對、相對、計算值都不行）
- 被什麼擋：在 `html` 寫 `font-size: 16px`，可能讓瀏覽器無法套用文字縮放（引用："This can prevent the browser from applying text scaling"）
- 戰報：僵持——根字級交給瀏覽器才能讓系統比例生效，但這只在支援 meta text-scale 的 Chrome／Edge 146 起有意義（官方宣稱）

經過：很多 reset 或設計系統習慣在 `html` 先釘一個 16px 當基準，這一行就把 opt-in 抵銷了。指南把它列為 DO NOT，並另外警告不要和 `env(preferred-text-scale)` 疊用造成雙重縮放。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：<meta name="text-scale">：Limited（Chrome 146、Edge 146）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯（新功能的使用條件，不產生新應用）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

`env(preferred-text-scale)` 與 meta 同時使用的雙重縮放已併入第一、三條，不另拆重複線。
