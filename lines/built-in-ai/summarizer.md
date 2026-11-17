---
guide: summarizer
category: built-in-ai
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/built-in-ai/summarizer.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 摘要器（Summarizer API）

%% line-start id="mwg:summarizer" %%
## 用 Summarizer 在本機產生摘要，不把文章送上雲端
- 做法：以相同的 options 呼叫 `Summarizer.availability()` 與 `Summarizer.create()`（type：key-points／tldr／teaser／headline），用 `summarize()` 或 `summarizeStreaming()` 摘要長文
- 對手：改由遠端服務代為處理時，請求會被轉到雲端，本機隱私保證完全失效，還會產生伺服器端 API 費用（引用："This completely nullifies the on-device privacy guarantees of the native Built-in AI APIs and will incur server-side API usage costs."）
- 退路：失去主要好處——退回雲端 API 或停用按鈕，內容又離開裝置，隱私保證與費用的問題回來
- 解鎖：以前要摘要就得把文章送上雲端；現在瀏覽器用內建模型在本機處理，資料不離開裝置，也沒有 API 帳單

經過：指南說摘要「完全在裝置上進行」，資料不送 Google。對手出現在 fallback 段的警告：polyfill 可能把請求轉給雲端模型。所以在 Firefox、Safari 上，要嘛付費且交出資料，要嘛停用摘要按鈕。
%% line-end %%

### 細節（不索引）
- 對手組：得送雲端或載大型函式庫
- 支援狀態：Summarizer：Limited（Chrome 138、Edge 138；Firefox、Safari 不支援）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：私人文件（日記、會議紀錄、郵件）可以在頁面裡直接產生 TL;DR 或重點條列，內容不離開裝置，也沒有 API 帳單；例如長週記頂端自動加一段「本週三句話」。目前僅 Chrome／Edge 138 桌面版
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
