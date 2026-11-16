---
guide: lazy-load-video-and-audio
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/lazy-load-video-and-audio.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 延遲載入影片與音訊

%% line-start id="mwg:lazy-load-video-and-audio" %%
## 用 <video>／<audio> 的 loading="lazy" 把海報圖與 metadata 請求延到接近視窗時
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：對首屏以下的 `<video>`、`<audio>` 加 `loading="lazy"`，搭配 `preload="none"`（要使用者按播放）或 `preload="metadata"`（進入視窗後自動帶出長度與首格）；`autoplay` 也會等到接近視窗才下載與播放
- 被什麼擋：即使設了 `preload="metadata"` 或 `preload="none"`，瀏覽器仍立刻抓 `poster` 圖，`preload="metadata"` 還會對頁面上每個播放器發出範圍請求（引用："Even when `preload="metadata"` or `preload="none"` is set on a `<video>`, the browser eagerly fetches its `poster` image immediately, and `preload="metadata"` still initiates range requests for media headers across every player on the page."）
- 戰報：部分改善——支援的瀏覽器把海報圖、preload 與 autoplay 全部延到接近視窗；不支援時屬性被忽略，搭配 `preload="none"`／`metadata` 仍不會預先下載整個媒體檔，但海報圖與 metadata 照樣立即抓，要完全延後得自己用 `IntersectionObserver`（官方宣稱）

經過：教學頁放了二十支影片，就算都設 `preload="none"`，一載入還是先抓二十張海報圖。`loading="lazy"` 讓媒體元素也能像圖片一樣等捲近了才發請求。目前只有 Chromium。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：Lazy-loading media：Limited availability。Supported by: Chrome 150, Edge 150；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：一頁塞滿影片的課程目錄、Podcast 全集列表、產品示範牆可以只寫 HTML，不必自己寫 IntersectionObserver 換 `data-src`，首屏也不會被幾十張海報圖拖住。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:lazy-load-video-and-audio:2" %%
## 延遲載入的 video 要寫寬高、audio 要有 controls，否則永遠不載入
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<video loading="lazy">` 一律寫整數的 `width`、`height`；`<audio loading="lazy">` 一律加 `controls`
- 被什麼擋：沒有 `controls` 的音訊元素沒有可見的盒子，碰不到視窗，永遠不載入也不自動播放；沒寫尺寸的影片預設 300×150，可能碰不到視窗而永遠不載入，或載入時造成版面位移（引用："an `<audio loading="lazy">` element without `controls` cannot visibly intersect the viewport and will never load or autoplay."）
- 戰報：部分改善——有尺寸與 controls，元素才有實際的版面盒子可以觸發載入，也不會在載入時撐開版面（官方宣稱）

經過：背景音樂用沒有 controls 的 audio 加 lazy，或影片只靠 CSS 設尺寸，延遲載入的判斷根本不成立，媒體就靜靜地一直不出現。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Lazy-loading media：Limited availability（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:lazy-load-video-and-audio:3" %%
## window 的 load 事件不等延遲載入的媒體
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：不用 `window` 的 `load` 事件判斷延遲載入的 `<video>`／`<audio>` 是否已載入
- 被什麼擋：`load` 事件只看急載的媒體，延遲載入的媒體就算一開始就在視窗內也不算（引用："The `load` event fires based only on eager-loaded media, even if a `loading="lazy"` media element is initially inside the visual viewport."）
- 戰報：缺——指南只說不要依賴 `load`，沒說該改用什麼判斷

經過：原本等 `load` 之後才初始化播放器或量版面的程式，加上 lazy 後時機就不對了，因為 `load` 觸發時媒體可能還沒開始抓。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Lazy-loading media：Limited availability（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:lazy-load-video-and-audio:4" %%
## 首屏與 LCP 影片不要加 loading="lazy"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：首屏的英雄影片省略 `loading` 屬性（預設急載），只對首屏以下的媒體加 `loading="lazy"`
- 被什麼擋：對首屏或 LCP 影片加 `loading="lazy"`，海報圖與影片資料的抓取都被延後（引用："DO NOT apply `loading="lazy"` to above-the-fold or Largest Contentful Paint (LCP) `<video>` elements, as it delays fetching both the `poster` image and video data."）
- 戰報：部分改善——首屏影片照常急載，海報圖與初始媒體立即開始下載（官方宣稱）

經過：一次替所有 `<video>` 加上 lazy，最先被看到的那支英雄影片也得等瀏覽器判斷距離後才抓海報圖，LCP 被拖慢。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Lazy-loading media：Limited availability（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（自動播放前尊重 `prefers-reduced-motion`；停用 JavaScript 時瀏覽器不延遲載入媒體，屬行為說明）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
