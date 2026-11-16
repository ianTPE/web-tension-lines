---
guide: language-model
category: built-in-ai
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/built-in-ai/language-model.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 語言模型（Prompt API）

%% line-start id="mwg:language-model" %%
## 用 Prompt API 在瀏覽器內跑 Gemini Nano
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `LanguageModel.availability()` 檢查，由使用者手勢觸發 `LanguageModel.create()` 下載模型，再用 `prompt()`／`promptStreaming()` 處理文字、圖片、音訊輸入
- 被什麼擋：（缺）只列出本機執行的好處（隱私、降低伺服器成本、可離線），沒說舊做法在哪個時刻出問題（引用："This built-in AI approach ensures user privacy, reduces server costs, and enables offline functionality."）
- 戰報：僵持——只有 Chrome 148 支援；Edge、Firefox、Safari 要退回伺服器／雲端 API，或用 Transformers.js 這類本機端點（官方宣稱）

經過：指南涵蓋 session 管理（`clone()`、`initialPrompts`、`destroy()`）、多模態輸入與 JSON Schema 結構化輸出。對手只以「好處」的反面出現，沒有可觀察的失敗。硬體門檻高（22 GB 空間、16 GB RAM），下載要使用者手勢並顯示進度。
%% line-end %%

### 細節（不索引）
- 對手組：得送雲端或載大型函式庫
- 支援狀態：LanguageModel：Limited（Chrome 148；Edge、Firefox、Safari 不支援）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：不經伺服器就能在頁面裡做分類、改寫、看圖回答，例如筆記 app 在本機替每篇日記打標籤、把截圖內容轉成文字，資料不離開裝置，離線也能用。目前僅 Chrome 148 桌面版，且有硬體門檻
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:language-model:2" %%
## 模型輸出一律用 textContent，不塞進 innerHTML
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把模型回應寫進 `textContent`；需要有限的 HTML 時，對**完整**輸出跑 Sanitizer API 或 DOMPurify
- 被什麼擋：模型輸出不可信，可能夾帶注入的標記，直接設 `innerHTML` 會變成 XSS（引用："Model output is untrusted and can contain injected markup. Always use `textContent` or a sanitizer."）
- 戰報：勝——當純文字寫入就不會被解析成標記（官方宣稱）

經過：串流時的常見寫法是每來一塊就 `innerHTML +=`，指南說這樣又慢又容易被注入，而且惡意碼可能被拆在兩塊之間，所以要清理合併後的完整輸出，不是逐塊清理。
%% line-end %%

### 細節（不索引）
- 對手組：不可信內容當HTML解析
- 支援狀態：—（textContent 指南未給支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:language-model:3" %%
## 串流輸出時設 aria-busy，讓讀屏唸完整回應而不是每一塊
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：輸出容器是從頁面載入就存在的 polite live region，串流期間設 `aria-busy="true"`，結束後設回 `false`；串流中不移動焦點
- 被什麼擋：沒有 `aria-busy` 時，live region 會把每個串流片段都唸出來（引用："so assistive technologies announce the complete response rather than each chunk"）
- 戰報：勝——輔助科技等串流結束才播報完整回應（官方宣稱）

經過：打字機效果對視覺使用者是回饋，對讀屏使用者卻是斷斷續續的碎片。輸出語言和頁面不同時，還必須在輸出元素設 `lang`，讀屏才會用對的發音。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：—（aria-busy／live region 指南未給支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有約 12 條未拆，例如：只靠「只輸出 JSON」的指示，模型會夾帶閒聊讓 parser 壞掉（`responseConstraint`）；用 `maxLength` 限制長度，模型改用外語或 emoji 壓縮造成亂碼；等使用者按「Generate」才建立 session 的冷啟動延遲；同一 session 做不相干任務，舊脈絡干擾新任務。
