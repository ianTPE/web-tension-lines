---
guide: dark-mode-toggle
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/dark-mode-toggle.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 深色模式切換

%% line-start id="mwg:dark-mode-toggle" %%
## 只改 `<meta name="color-scheme">` 沒用，要用 `:has()` 把它映射回 CSS
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`:root` 維持 `color-scheme: light dark`，再用 `:root:has(> head > meta[name="color-scheme"][content="dark"])`（與 `light`）覆寫成單一配色；切換時只改 `<meta>` 的 content
- 被什麼擋：`<meta>` 只是呈現提示，作者 CSS 裡的 `color-scheme` 會蓋過它，只更新 `<meta>` 等於沒做（引用："updating the `<meta>` alone is a **no-op** — CSS wins."）
- 戰報：勝——`light-dark()`、系統色與原生介面都跟著覆寫走；JS 沒跑時 `<meta>` 維持 `light dark`，照系統偏好（官方宣稱）

經過：按了切換鈕，meta 確實變了，頁面顏色紋風不動。把 meta 接回 color-scheme 屬性，所有顏色一次跟上。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode-toggle:2" %%
## 儲存的配色用緊接在 `<meta>` 後面的同步內嵌腳本套用
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `<meta name="color-scheme">` 後面放一段極小的內嵌 `<script>`（不是 module、不加 defer），從 `localStorage` 讀值寫回 meta
- 被什麼擋：晚一點才套用儲存的偏好，會先閃一下錯的配色（引用："To avoid a flash of the wrong scheme, apply the stored value in an inline script (NOT `type=module`, NOT `defer`) placed immediately after the `<meta>` element"）
- 戰報：勝——第一次繪製就是使用者選的配色（官方宣稱）

經過：選了深色的使用者每次換頁都被白光閃一下。
%% line-end %%

### 細節（不索引）
- 對手組：內容要等JS才成形
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode-toggle:3" %%
## 只在儲存當下比對系統偏好，之後不要因為兩者一致就刪掉儲存值
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：兩態切換的目標是「目前畫面的相反」；目標和系統偏好不同才存，相同就刪除儲存值；之後系統偏好變得和儲存值一樣時保留，不用 `matchMedia()` 自動清除
- 被什麼擋：很多人的系統會依時段自動切換，一致時就刪掉儲存值，使用者永遠無法固定配色；反過來存下與系統相同的值，又會在之後系統變更時悄悄釘死（引用："removing the stored value whenever the two happen to coincide would make it impossible to pin a scheme at all."；"that would invisibly pin the scheme against future system changes."）
- 戰報：勝——使用者可以固定配色，也可以一鍵回到跟隨系統（官方宣稱）

經過：白天把網站固定成深色，傍晚系統自動變深色時偏好被清掉，隔天早上網站又變回淺色。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dark-mode-toggle:4" %%
## 非顏色的分支不要只靠 JS 加的 `.dark` 類別
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：字重、圖片來源等非顏色值，用 `prefers-color-scheme` 媒體查詢搭配 `:root:has(> head > meta[...][content="dark"])` 選擇器分支
- 被什麼擋：JS 沒載入、系統預設又是深色時，只靠 `.dark` 類別的分支就會錯（引用："they will be incorrect if JS doesn't load and the OS default is dark."）
- 戰報：勝——不論 JS 是否執行，分支都和實際配色一致（官方宣稱）

經過：深色系統、腳本被擋：底色是深的，Logo 卻還是給淺色背景用的黑色版。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：用 `display: none` 藏 `<source>` 無效，HTML 媒體只能放兩份元素切換；多數網站不需要常駐的配色切換鈕，放在設定頁即可
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
