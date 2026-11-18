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
- 做法：用 `LanguageModel.availability()` 檢查，由使用者手勢觸發 `LanguageModel.create()` 下載模型，再用 `prompt()`／`promptStreaming()` 處理文字、圖片、音訊輸入
- 對手：（缺）只列出本機執行的好處（隱私、降低伺服器成本、可離線），沒說舊做法在哪個時刻出問題（引用："This built-in AI approach ensures user privacy, reduces server costs, and enables offline functionality."）
- 退路：保住主要行為——退回雲端 API 或 Transformers.js，失去內建模型部署便利
- 解鎖：以前要在瀏覽器裡做推論只能自己載模型或呼叫雲端；現在 `LanguageModel` 能在裝置上跑，文字、圖片、音訊都能餵進去，離線也能用

經過：指南涵蓋 session 管理（`clone()`、`initialPrompts`、`destroy()`）、多模態輸入與 JSON Schema 結構化輸出。對手只以「好處」的反面出現，沒有可觀察的失敗。硬體門檻高（22 GB 空間、16 GB RAM），下載要使用者手勢並顯示進度。
%% line-end %%

### 細節（不索引）
- 對手組：得送雲端或載大型函式庫
- 支援狀態：LanguageModel：Limited（Chrome 148；Edge、Firefox、Safari 不支援）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：不經伺服器就能在頁面裡做分類、改寫、看圖回答，例如筆記 app 在本機替每篇日記打標籤、把截圖內容轉成文字，資料不離開裝置，離線也能用。目前僅 Chrome 148 桌面版，且有硬體門檻
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」

%% line-start id="mwg:language-model:2" %%
## 模型輸出一律用 textContent，不塞進 innerHTML
- 做法：把模型回應寫進 `textContent`；需要有限的 HTML 時，對**完整**輸出跑 Sanitizer API 或 DOMPurify
- 對手：模型輸出不可信，可能夾帶注入的標記，直接設 `innerHTML` 會變成 XSS（引用："Model output is untrusted and can contain injected markup. Always use `textContent` or a sanitizer."）
- 退路：不需要——`textContent` 與清理器是既有機制，不必退路
- 解鎖：（缺）

經過：串流時的常見寫法是每來一塊就 `innerHTML +=`，指南說這樣又慢又容易被注入，而且惡意碼可能被拆在兩塊之間，所以要清理合併後的完整輸出，不是逐塊清理。
%% line-end %%

### 細節（不索引）
- 對手組：不可信內容當HTML解析
- 支援狀態：—（textContent 指南未給支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:3" %%
## 串流輸出時設 aria-busy，讓讀屏唸完整回應而不是每一塊
- 做法：輸出容器是從頁面載入就存在的 polite live region，串流期間設 `aria-busy="true"`，結束後設回 `false`；串流中不移動焦點
- 對手：沒有 `aria-busy` 時，live region 會把每個串流片段都唸出來（引用："so assistive technologies announce the complete response rather than each chunk"）
- 退路：不需要——`aria-busy` 與 live region 是既有 ARIA 機制，不必退路
- 解鎖：（缺）

經過：打字機效果對視覺使用者是回饋，對讀屏使用者卻是斷斷續續的碎片。輸出語言和頁面不同時，還必須在輸出元素設 `lang`，讀屏才會用對的發音。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：—（aria-busy／live region 指南未給支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:4" %%
## 需要下載模型時由使用者手勢呼叫 create()
- 做法：`availability()` 為 downloadable／downloading 時，在按鈕等事件處理中呼叫 `LanguageModel.create()`，不要在頁面載入時呼叫
- 對手：下載模型的 `create()` 需要使用者手勢，頁面載入時呼叫會以 `NotAllowedError` 拒絕（引用："Call it from an event listener, not on page load, or it rejects with a `NotAllowedError`."）
- 退路：保住主要行為——退回雲端或替代本機模型，不再觸發內建模型下載手勢錯誤
- 解鎖：（缺）

經過：模型已可用時能直接建 session；需要下載時則要由使用者明確啟動，並先檢查裝置是否 unavailable。
%% line-end %%

### 細節（不索引）
- 對手組：權限請求不看時機
- 支援狀態：LanguageModel：Limited（Chrome 148）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」

%% line-start id="mwg:language-model:5" %%
## 模型下載顯示可及進度與完成狀態
- 做法：用有名字的 `<progress>` 顯示 `downloadprogress`，完成時更新 polite live region，不只寫 console
- 對手：大型模型下載沒有可見進度時，UI 看起來像凍結（引用："Inform the user while the model downloads so the UI doesn't appear frozen."）
- 退路：失去主要好處——退回雲端 API 時沒有本機模型可下載，進度條這段無從做起
- 解鎖：（缺）

經過：下載需要 22 GB 空間，等待不該只剩一顆沒有反應的按鈕。進度條要有可及名稱，完成訊息也要能被讀屏聽到。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：LanguageModel：Limited
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:6" %%
## 下載或停止鈕消失前把焦點移到合理目標
- 做法：下載鈕在聚焦狀態被隱藏時，焦點移到帶 `tabindex="-1"` 的狀態文字；停止生成鈕隱藏時移回原本啟動控制項
- 對手：目前聚焦的按鈕被隱藏後，鍵盤使用者失去所在位置（引用："If the button that starts the download is hidden while it has focus, move focus to the download's status text"）
- 退路：沒說——指南未交代不支援時怎麼辦
- 解鎖：（缺）

經過：下載開始或生成結束常會改變可用按鈕，不能只是刪掉目前焦點元素。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：LanguageModel：Limited
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「沒說」

%% line-start id="mwg:language-model:7" %%
## 輸出語言不同時在輸出元素設 lang
- 做法：模型輸出元素依 `expectedOutputs` 的語言設 `lang`，不沿用頁面預設語言
- 對手：輸出語言和頁面不同時，讀屏會用錯誤語言規則發音（引用："If the output language differs from the page language, set `lang` on the output element to the language declared in `expectedOutputs`, so screen readers pronounce it correctly"）
- 退路：保住主要行為——退回雲端 API 後輸出語言一樣要標 `lang`，這條規則照舊成立
- 解鎖：（缺）

經過：中文頁面叫模型輸出英文、日文或西班牙文時，每一段都要把語言標起來。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:8" %%
## 監看 context 用量，避免舊訊息被靜默丟棄
- 做法：用 `contextUsage`／`contextWindow` 監看 token，必要時開新 session 或只保留所需脈絡
- 對手：session 超過 token 上限時，最舊的訊息（system prompt 除外）會被丟掉，後續回答失去早期依據（引用："If the window overflows, the oldest messages (except the system prompt) are dropped."）
- 退路：失去主要好處——退回雲端 API 時沒有本機 session 的 token 視窗可監看
- 解鎖：（缺）

經過：長對話不是無限記憶。重要資訊要在溢出前整理，不能假設模型永遠記得第一輪內容。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：LanguageModel：Limited
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:9" %%
## 對話歷史存 localStorage 前先處理個資風險
- 做法：用 `initialPrompts` 還原歷史前，評估是否該持久化、去除個資或改用其他儲存方式
- 對手：`localStorage` 未加密且持久，對話中的個人資料會留在裝置上（引用："`localStorage` is unencrypted and persistent. Stored conversation history may include user PII"）
- 退路：保住主要行為——退回雲端 API 後對話歷史一樣會留在瀏覽器儲存，個資風險照舊
- 解鎖：（缺）

經過：本機模型不代表資料保存就沒有風險。還原 session 的便利性要和歷史內容的敏感度一起判斷。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:10" %%
## 用 responseConstraint 的 JSON Schema 擋掉閒聊與解析失敗
- 做法：把 JSON Schema 以 plain object 傳給 `responseConstraint`，需要時用 `prefix: true` 引導開頭
- 對手：只叫模型「只輸出 JSON」仍可能夾帶開場白，讓 parser 壞掉，還得補複雜後處理（引用："Models might include conversational filler that breaks your parser."）
- 退路：失去主要好處——退回雲端 API 時沒有本機的結構化輸出限制可用，得自己寫容錯解析
- 解鎖：以前要模型輸出可解析的 JSON，只能在提示詞裡求它配合再寫容錯解析器；現在直接給 JSON Schema 限制回應形狀

經過：分類、欄位抽取這類功能需要的是資料，不是聊天文字。schema 直接限制回應形狀，不要先 JSON.stringify schema。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：LanguageModel：Limited
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：情緒分類、表單自動填入、資料抽取可直接接 `JSON.parse()` 進入應用程式流程，不必再寫容錯解析器。目前僅 Chrome 148
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:11" %%
## 使用者意圖明確時先暖機，initialPrompts 在建立時給齊
- 做法：使用者進入 AI 工作區或和周圍 UI 互動時先建立 session；`initialPrompts` 準備好再一次傳入 `create()`
- 對手：等按下 Generate 才載入模型會有冷啟動延遲；system instructions 放到第一次 prompt 也要在最後一刻才處理，增加延遲（引用："This leads to a cold start delay, because the model must first load into memory and prepare its execution pipeline."）
- 退路：保住主要行為——退回替代模型，仍可在意圖明確時提前準備請求與指示
- 解鎖：（缺）

經過：暖機不是頁面一載入就下載模型，而是意圖已明確時提前準備。`initialPrompts` 只能在建立時設定，不能暖機後才補。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」

%% line-start id="mwg:language-model:12" %%
## 不相干任務從乾淨 base session clone，不共用舊脈絡
- 做法：base session 只放 system instructions，新任務用 `clone()` 分支；不要重用含無關歷史的 session 或 clone
- 對手：同一 session 的先前互動會干擾目前任務，clone 也會繼承所有無關歷史（引用："Both patterns can cause unrelated previous context to interfere with your current task."）
- 退路：保住主要行為——退回替代模型的乾淨請求，不帶入無關任務歷史
- 解鎖：（缺）

經過：昨天翻譯用的 session 今天拿來分類，舊語言與指令可能影響結果。乾淨基底既省初始化，也避免串味。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」

%% line-start id="mwg:language-model:13" %%
## 用完的 session 明確 destroy() 釋放裝置記憶體
- 做法：clone 任務完成就 destroy，不再需要新 clone 時也 destroy base session
- 對手：多個大型 session 同時保留會持續占用記憶體；垃圾回收比明確釋放來得慢（引用："Each session consumes memory, which creates unnecessary resource usage and might become a problem."）
- 退路：保住主要行為——退回雲端模型或明確關閉替代本機工作，釋放不再需要資源
- 解鎖：（缺）

經過：session 與 clone 是裝置上的大型資源，不只是普通 JS 物件。保留 base 的唯一理由是之後還要分支。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」

%% line-start id="mwg:language-model:14" %%
## 只送任務所需輸入，避免大資料讓本機模型像壞掉
- 做法：移除無關 metadata、HTML 與大清單，大資料改成短摘要加少量相關項目
- 對手：輸入越大延遲越明顯，在許多裝置上會讓 AI 功能看起來像沒有回應（引用："Latency grows significantly with input size, which can make the AI feature seem broken on many devices."）
- 退路：保住主要行為——退回雲端 API 後輸入太大一樣拖慢回應，只送必要輸入這條照舊
- 解鎖：（缺）

經過：整份文件與所有欄位都丟進去，不一定比精選內容更有效。輸入設計也是本機推論的效能設計。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:15" %%
## 不用 maxLength 逼模型縮短，生成後由程式截斷
- 做法：讓模型自然生成，再由 client-side 邏輯依 UI 需要截斷，不在 structured output schema 寫嚴格字元上限
- 對手：超過上限時模型可能改用外語或 emoji 高密度壓縮，輸出變成無意義內容（引用："the model might switch to high-density tokens like foreign languages or emoji to compress meaning, resulting in nonsensical output."）
- 退路：保住主要行為——退回雲端 API 後一樣可能壓縮成高密度詞元，截斷規則照舊
- 解鎖：（缺）

經過：125 字元限制不是單純截斷指令，模型會自己想辦法塞進去，結果可能更短卻不可讀。
%% line-end %%

### 細節（不索引）
- 對手組：優化用過頭反傷
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「優化用過頭反傷」

%% line-start id="mwg:language-model:16" %%
## AI 改寫保留版本、比較與復原，不覆蓋唯一草稿
- 做法：提供 stepper／歷史、快速 undo 與版本比較，使用者能回到先前草稿或喜歡的 AI 結果
- 對手：直接覆蓋會讓使用者失去原本草稿或較好的上一版，無法回頭（引用："Don't: Overwrite the user's previous draft, or an AI result they might have liked without a way to go back, revert, or compare versions."）
- 退路：保住主要行為——退回雲端 API 後改寫一樣不能直接蓋掉唯一草稿
- 解鎖：（缺）

經過：生成式修改不是一次取代文件，而是增加一個候選版本。使用者能探索結果而不用擔心失去原作。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:language-model:17" %%
## 重複輸入用本機快取，不重新跑相同推論
- 做法：以 `sessionStorage`／`IndexedDB` 快取正規化輸入或圖片 hash，設合理 TTL，必要時背景更新並允許手動重跑
- 對手：使用者在相同搜尋或資料間來回時重跑推論，浪費本機運算並拖慢回應（引用："Don't: Re-run the same inference for a repeated search query or identical data input where variability isn't desirable"）
- 退路：保住主要行為——退回雲端 API 後重複輸入一樣在燒錢與拖慢回應，快取照舊要加
- 解鎖：（缺）

經過：輸入先 trim、英文小寫正規化以提高命中，圖片則用 hash。快取不是永久真理，TTL 與手動刷新都要留。
%% line-end %%

### 細節（不索引）
- 對手組：快取策略錯置
- 支援狀態：LanguageModel：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
