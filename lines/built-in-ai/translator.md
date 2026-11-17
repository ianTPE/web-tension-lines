---
guide: translator
category: built-in-ai
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/built-in-ai/translator.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 翻譯器（Translator API）

%% line-start id="mwg:translator" %%
## 用 Translator 在本機翻譯，不把文字送上雲端
- 做法：以相同的 `sourceLanguage`／`targetLanguage` 呼叫 `Translator.availability()` 與 `Translator.create()`，由使用者手勢觸發語言包下載，用 `translate()` 或 `translateStreaming()` 翻譯
- 對手：改由遠端服務處理時，本機隱私保證完全失效，也常產生伺服器端 API 費用（引用："Remote processing completely nullifies the on-device privacy guarantees of the native Built-in AI APIs and will often incur server-side API usage costs."）
- 退路：失去主要好處——退回雲端 API 或停用按鈕，文字又離開裝置，隱私保證與費用的問題回來
- 解鎖：以前翻譯要把文字送上雲端；現在瀏覽器用內建模型在本機翻，資料不離開裝置，也沒有每字計費

經過：指南把用途限定在「短暫內容」：聊天訊息、使用者輸入這類不值得送雲端的文字。模型下載後翻譯不連網。語言包按語言對下載，`availability()` 會回報 available／downloadable／downloading／unavailable 四種狀態，unavailable 時就得走 fallback。
%% line-end %%

### 細節（不索引）
- 對手組：得送雲端或載大型函式庫
- 支援狀態：Translator：Limited（Chrome 138、Edge 148；Firefox、Safari 不支援；僅桌面版）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：聊天室、留言區可以逐則「就地翻譯」，訊息不經第三方翻譯服務，也沒有每字計費；配合語言偵測可以做到不用選來源語言。目前僅 Chrome／Edge 桌面版
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
