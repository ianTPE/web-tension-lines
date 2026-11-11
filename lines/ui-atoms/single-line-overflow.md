---
guide: single-line-overflow
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/single-line-overflow.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 單行文字溢出

%% line-start id="mwg:single-line-overflow" %%
## 用 CSS 視覺截斷取代在 script 裡砍字串
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：單行標籤（分頁、表格格、檔名）過長時，用 `text-overflow: ellipsis` 或 mask 淡出只在畫面上截斷，全文留在 DOM
- 被什麼擋：在 script 裡把字串切短後，螢幕閱讀器、頁內搜尋、複製拿到的都是殘缺文字（引用："Screen readers announce the full text, find-in-page matches it, and copying copies it. This is why the string must never be cut in script."）
- 戰報：勝——截斷只發生在繪製層，輔助技術、搜尋、複製都還拿得到全文；省略號與 mask 都是 Widely available（官方宣稱）

經過：常見寫法是在渲染前把字串截到 N 個字再加「…」，結果全文從 DOM 消失。指南要求截斷只做在視覺上；要保留副檔名這類尾巴時，在 markup 裡分段包起來，而不是切字元。另一個坑是用單一漸層當 mask：它會連焦點外框一起遮掉（"it also hides the element's focus outline"）。
%% line-end %%

### 細節（不索引）
- 對手組：截字傷可及性
- 支援狀態：Masks：Widely（2023-12-07）；Container queries (size)：Widely（2023-02-14）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出

%% line-start id="mwg:single-line-overflow:2" %%
## 讓被截斷的全文對鍵盤與觸控也找得到
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `:hover` 與 `:focus-visible` 觸發文字捲動顯示，並以 scroll-driven animations 控制淡出與提示
- 被什麼擋：只靠 `title` 屬性顯示全文，鍵盤和觸控使用者都碰不到（引用："DO NOT rely on `title` alone: it is unreachable from the keyboard and on touch."）
- 戰報：部分改善——鍵盤可經由 focus 看到全文；但觸控仍沒有 hover/focus，指南改要求另開一條路（選中的項目不截斷、打開詳情）；scroll-driven animations 才剛 Newly available（官方宣稱）

經過：`title` 是最省事的做法，但只對滑鼠有效。新做法在 hover 和 focus 時讓文字在框內捲動，淡出寬度跟著捲動縮小，捲到底時尾端可讀。原文也承認 "Hover and focus reveal nothing on touch"，所以觸控這一側的對手沒有被新功能擋掉，而是靠介面設計繞開。不支援 scroll-driven animations 時，淡出與提示都不出現，文字被切掉且沒有任何跡象，要用 `ResizeObserver` 補。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：Scroll-driven animations：Newly（2026-10-27）；Container style queries：Newly（2026-05-19）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 上游 issue 候選：無
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
