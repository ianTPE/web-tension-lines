---
guide: dynamic-sort
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/dynamic-sort.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 使用者觸發的動態排序

%% line-start id="mwg:dynamic-sort" %%
## 搬既有節點排序，不用 innerHTML 重建
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：使用者改變排序時，用 `moveBefore()` 把既有節點搬到新順序，並可包進 view transition 做動畫
- 被什麼擋：用 `innerHTML` 或整批重新 render 產生新節點，焦點、項目內捲動位置、圖片狀態全部丟失，view transition 也對不上（引用："Recreating nodes with `innerHTML` or a re-render that replaces them discards focus, scroll position inside items, and image state, and it breaks view transitions, which match old and new elements by identity."）
- 戰報：部分改善——搬節點本身就擋掉焦點與捲動流失；`moveBefore()` 在 Safari 不支援，fallback `append()` 順序相同但 iframe/動畫/內部焦點可能流失；view transitions 為 Newly（官方宣稱）

經過：排序後整個清單重畫是最常見的寫法，代價是使用者剛點的按鈕失焦、卡片內捲到一半的內容回到頂端。指南把排序改成「搬家」而不是「重蓋」，並讓動畫成為可有可無的加強。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：moveBefore()：Limited（Safari 不支援）；View transitions：Newly（2025-10-14）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：排序或篩選後清單用 view transition 動畫「走」到新位置，項目內的捲動、焦點、播放狀態都還在。適合項目本身很重的清單（內嵌預覽、影片卡片）
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:dynamic-sort:2" %%
## 排序結果只播報一次
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用一個 `role="status"` 區域在排序後播報一次結果，焦點留在觸發排序的控制項
- 被什麼擋：把 `aria-live` 放在清單上，每個被搬動的項目都被唸一次（引用："DO NOT put `aria-live` on the list, which would announce every moved item."）
- 戰報：勝——使用者做了一次動作，只聽到一次播報（官方宣稱）

經過：重排會搬動很多節點，但使用者只做了一個動作。清單掛 `aria-live` 時，螢幕閱讀器會把每次節點移動都當成更新來唸。改成單一狀態區播報一次即可。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：ARIA live regions：Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
