---
guide: apply-webgl-shaders
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/apply-webgl-shaders.md
first_seen: 2026-11-16（v1.0.0，回溯拆出；上游自 v0.0.177 起就有這份指南）
license: CC-BY-4.0（上游指南）
---

# 把 WebGL shader 套用到 HTML 內容

%% line-start id="mwg:apply-webgl-shaders" %%
## shader 直接套在可互動的 HTML 上
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把 `drawable` 的 HTML 元素用 `texElementSubImage2D()` 上傳成 WebGL 貼圖，套 fragment／vertex shader，再用 `canvas.updateElementGeometry()` 讓點擊位置和畫出來的像素對齊
- 被什麼擋：（缺）只說套了 shader 之後仍保有原生的可及性、文字選取與 DOM 事件，沒說以前的做法是什麼、壞在哪（引用："This enables applying high-performance fragment and vertex shaders natively to fully interactive UI components, such as buttons, input fields, and rich text, while retaining native accessibility, text selection, and DOM event handling."）
- 戰報：僵持——指南宣稱按鈕、輸入框、rich text 套上 shader 後仍可互動；但只有 Chrome 157 起支援，其他瀏覽器的 fallback 是把 HTML 用 CSS 疊在 canvas 上（也就沒有 shader 效果），或用 `three-html-render` polyfill（官方宣稱）

經過：波紋扭曲、光照、調色這類效果只能作用在貼圖上，而貼圖不是元素。新 API 讓真元素的繪製結果成為貼圖，同時元素本身留在 DOM 裡接收輸入。指南沒有描述舊做法，所以對手判缺。貼圖要先用 `texImage2D()` 配置、尺寸變了才重配，元素還沒繪製過時 `captureElementImage()` 會丟例外，這些都得自己處理。
%% line-end %%

### 細節（不索引）
- 對手組：canvas裡手寫互動
- 支援狀態：HTML-in-Canvas：Limited（Chrome 157 起，2026-11-03 進穩定版；Firefox、Safari 不支援）。指南的 fallback 段落仍寫 "HTML-in-canvas is not natively supported by any major browser yet."，已過時，照 PROMPT.md「已驗證的支援資料偏差」判
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：按下去會起漣漪的真按鈕、帶玻璃折射或 CRT 掃描線的真輸入框：效果是 GPU shader，但仍然可以打字、選字、被螢幕閱讀器讀到。目前僅 Chrome 157 起
- 現成 demo：[webgpu-jelly-slider](https://wicg.github.io/html-in-canvas/Examples/webgpu-jelly-slider/)（果凍效果的滑桿；用的是 WebGPU `drawElementImageToTexture()`，不是這份指南的 WebGL 路徑）、[webGL](https://wicg.github.io/html-in-canvas/Examples/webGL.html)（WebGL 貼圖，沒有自訂 shader 效果）（WICG 範例，尚未自己實測）
- 規格來源：https://github.com/WICG/html-in-canvas （四槽只依上游指南判定，這裡僅供追蹤）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出（使用者指定 HTML-in-Canvas 的四份指南；不在每週差異內）；2026-11-16 支援狀態由「無瀏覽器支援」更正為 Limited（Chrome 157 已於 2026-11-03 進穩定版，指南 fallback 段落過時）
