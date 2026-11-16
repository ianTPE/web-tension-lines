---
guide: conditional-async-dependencies
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/conditional-async-dependencies.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 條件式非同步相依

%% line-start id="mwg:conditional-async-dependencies" %%
## 用 top-level await 只在缺功能時載入 polyfill，並讓下游模組等它載完
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在一個獨立模組裡做功能偵測（例如檢查 `'popover' in HTMLElement.prototype`），缺的時候 `await import()` polyfill；入口模組靜態 import 這個模組後才使用該功能
- 被什麼擋：缺——指南只說這樣能把條件載入封裝在單一模組、讓下游在相依載完前不執行，沒說舊做法在哪個時刻出問題
- 戰報：部分改善——top-level await 2026-09-14 起才算 Baseline（Safari 27 修正模組載入器）；Safari 15–26.6 只要照單一入口的寫法就能安全使用（官方宣稱）

經過：polyfill 或大型次要函式庫只有不支援的瀏覽器需要，用 top-level await 包成一個模組，支援的瀏覽器不必下載，不支援的瀏覽器在使用前一定已經載完。指南沒有描述不用這個模式時壞在哪裡。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：Top-level await：Newly available（2026-09-14）。Supported by: Chrome 89, Edge 89, Firefox 89, Safari 27
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：用到 popover、anchor positioning 這類新功能的小工具，可以只替舊瀏覽器載 polyfill，新瀏覽器零額外下載，而且主程式不必到處寫「等 polyfill 好了再跑」的回呼
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:conditional-async-dependencies:2" %%
## top-level await 只擋住匯入它的父模組，不擋兄弟 import
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：從單一入口匯入含 top-level await 的模組；入口要委派給其他應用模組時，用 `await import('./polyfill.js'); await import('./app.js');` 串起來，不寫成兩個並列的靜態 import，也不讓多個兄弟模組同時匯入它
- 被什麼擋：並列的靜態 import 會讓 `app.js` 在 polyfill 載完前就執行；Safari 15–26.6 在多個模組同時匯入含 top-level await 的模組時直接失敗（引用："top-level `await` only suspends the parent module that imports it—not sibling static imports—so `./app.js` will evaluate concurrently in all browsers before the polyfill finishes loading."）
- 戰報：部分改善——照單一入口或串接動態 import 的寫法，`app.js` 一定在 polyfill 之後才取得與執行，Safari 舊版的錯誤也不會觸發（官方宣稱）

經過：直覺寫法是入口檔裡兩行 import，看起來有順序，實際上兄弟模組照樣並行求值，`showPopover()` 在 polyfill 還沒到時就被呼叫。改成串接動態 import，順序才真的被保證。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Top-level await：Newly available（同上）；Safari 15–26.6 的並行匯入錯誤於 Safari 27 修正
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
