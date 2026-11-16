---
guide: overflow-clipping-control
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/overflow-clipping-control.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 控制溢出裁切的位置

%% line-start id="mwg:overflow-clipping-control" %%
## 用 overflow-clip-margin 留出安全距離，不讓 overflow: hidden 切掉子元素的陰影
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在容器上設 `overflow: clip` 加長度值的 `overflow-clip-margin`（例如 `15px`），讓裁切邊界往外推一段，子元素的陰影可以畫出容器外
- 被什麼擋：`overflow: hidden` 一律在 padding box 切齊，子元素明顯的陰影在容器邊界被切斷；舊解法是多包一層 wrapper 再配 padding 與負邊距（引用："Without this, the child's shadow is clipped at the parent's boundary."）
- 戰報：僵持——`overflow-clip-margin` 目前只有 Firefox 148 支援，其他瀏覽器退回 `overflow: hidden`，陰影照樣被切（官方宣稱）

經過：卡片裡的送出按鈕帶一圈發光陰影，容器為了裁掉其他溢出內容設了 `overflow: hidden`，陰影就被切成一刀平的邊。`overflow-clip-margin` 讓裁切線往外留一段，版面幾何不變。但 Chrome、Edge、Safari 都還不支援，實務上仍得靠 fallback。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：overflow-clip-margin：Limited（Supported by: Firefox 148 (Feb 2026). Unsupported in: Chrome, Edge, and Safari.）；overflow: clip 本身 Widely（2022-09-12）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前裁切與「讓效果溢出」只能二選一 → 卡片可以裁掉溢出的內文，同時讓按鈕光暈、浮起陰影、角落徽章畫出邊界一段距離，不必多包 wrapper。目前僅 Firefox 148
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:overflow-clipping-control:2" %%
## 用 overflow-clip-margin: content-box 讓內層圓角自動同心
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在有圓角與 padding 的容器上設 `overflow: clip; overflow-clip-margin: content-box`，讓裁切邊界對齊內容框，內層圖片與頁尾的角被切成同心的內圓角
- 被什麼擋：（缺）只說能省去手算 padding 的 `calc()`、解決「awkward nesting curves」，沒說舊做法的內角在什麼情況下出現什麼樣的錯（引用："solving awkward nesting curves without custom `calc()` logic."）
- 戰報：僵持——`overflow-clip-margin` 只有 Firefox 148 支援，其他瀏覽器退回 `overflow: hidden`，大致在 padding box 裁切（官方宣稱）

經過：圓角卡片裡放滿版圖片與深色頁尾，內層的角和外框的角要同心才好看，以往得自己用外圓角減 padding 算內圓角。裁切邊界對齊 content box 後，瀏覽器直接算出對應的弧度。支援範圍太窄，目前只能當漸進增強。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：overflow-clip-margin：Limited（僅 Firefox 148）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前巢狀圓角要手算 → 卡片、對話框裡的內嵌媒體可以只寫外框圓角，內層自動貼合同心弧度，換 padding 也不用重算。目前僅 Firefox 148
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

未拆：「不要在需要程式捲動或作為 `position: sticky` 定位脈絡的容器上用 `overflow: clip`」是使用限制，不是做法對付的對手。
