---
guide: prerendering-custom-elements
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/prerendering-custom-elements.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 預先渲染自訂元素

%% line-start id="mwg:prerendering-custom-elements" %%
## 用 Declarative Shadow DOM 從伺服器送出 shadow tree，擋掉等 JS 才有樣式的閃爍
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：宿主的第一個子節點放 `<template shadowrootmode="open">`，元件 CSS 寫在模板內的 `<style>` 或 `<link>`，解析器直接掛上 shadow root
- 被什麼擋：shadow tree 靠腳本建立時，元件在 JS 執行前沒有結構也沒有樣式，出現未樣式化內容的閃爍（FOUC）；樣式若放在另外由腳本載入的樣式表，第一次繪製也一樣沒樣式（引用："DSD renders correctly on first paint only if styles ship inside the declarative template."）
- 戰報：勝——DSD 已 Widely，元件在任何 JS 執行前就有結構與樣式，伺服器渲染與串流都適用（官方宣稱）

經過：卡片元件的外框、間距都寫在 shadow 裡，頁面先出現一堆沒排版的文字，等元件腳本跑完才突然成形。DSD 讓解析器直接長出 shadow root，樣式隨模板送達，第一次繪製就是完成的樣子。
%% line-end %%

### 細節（不索引）
- 對手組：內容要等JS才成形
- 支援狀態：Declarative shadow DOM：Widely（2024-02-20）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:prerendering-custom-elements:2" %%
## hydrate 時沿用伺服器的 shadow root，不要重新渲染
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：constructor 先檢查 `this.shadowRoot`，已存在就沿用，只在沒有時才 `attachShadow()`；行為直接掛在現有標記上
- 被什麼擋：升級時重新渲染 shadow tree，會丟掉伺服器送來的 DOM 並造成閃爍（引用："do NOT re-render; that would discard the server's DOM and flash."）
- 戰報：勝——把伺服器標記當成權威、原地接上事件，畫面不重繪（官方宣稱）

經過：元件類別照客戶端渲染的習慣，在 constructor 裡無條件建 shadow root 並塞模板，伺服器辛苦送來的內容被整個換掉，畫面閃一下。改成「有就用、沒有才建」就沒事。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：Declarative shadow DOM：Widely（2024-02-20）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 1 個糾錯提醒未拆：`shadowrootmode` 用 `open` 而非 `closed`，讓腳本與工具拿得到 `this.shadowRoot`（同 `mwg:web-components:2` 的對手）。
