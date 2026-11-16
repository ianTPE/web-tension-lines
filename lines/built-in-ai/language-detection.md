---
guide: language-detection
category: built-in-ai
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/built-in-ai/language-detection.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 語言偵測

%% line-start id="mwg:language-detection" %%
## 在瀏覽器裡用 LanguageDetector 判斷文字語言
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：先用 `LanguageDetector.availability()` 檢查，再由使用者手勢觸發 `LanguageDetector.create()`，用 `detect()` 取得依信心分數排序的語言清單
- 被什麼擋：（缺）只說可以減少對大型外部函式庫或昂貴伺服器呼叫的依賴，沒說舊做法在哪個時刻出問題（引用："it enhances user privacy and reduces the need for heavy external libraries or costly server-side calls."）
- 戰報：僵持——只有 Chrome 138、Edge 148 支援；其他瀏覽器得退回伺服器或雲端 API，或停用偵測功能（官方宣稱）

經過：用途包括翻譯前判斷來源語言、替內容加正確的 `lang`。指南強調偵測在本機進行，資料不會送到 Google 或第三方，但沒有描述舊做法的具體失敗。模型下載要使用者手勢、需要 22 GB 空間與 16 GB RAM，很短的字句準確度也會大幅下降。
%% line-end %%

### 細節（不索引）
- 對手組：得送雲端或載大型函式庫
- 支援狀態：Language detector：Limited（Chrome 138、Edge 148；Firefox、Safari 不支援）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：使用者貼進來的文字可以在本機判斷語言，自動替留言、筆記段落補上正確的 `lang`，讓讀屏用對的發音唸，也不用把內容送去伺服器。目前僅 Chrome／Edge 桌面版，且有硬體門檻
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
