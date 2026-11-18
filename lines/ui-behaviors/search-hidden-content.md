---
guide: search-hidden-content
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/search-hidden-content.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 可被搜尋的隱藏內容

%% line-start id="mwg:search-hidden-content" %%
## 用 `<details>` 或 `hidden="until-found"` 藏內容，頁內搜尋仍找得到
- 做法：一般摺疊優先用 `<details>`；控制鈕在 DOM 別處、要完全自訂樣式或不打算再收起時，用 `hidden="until-found"`，並在 `beforematch` 事件裡同步相關狀態（例如設 `aria-expanded="true"`、收起其他面板）
- 對手：用 `display: none` 或 `visibility: hidden` 藏起來的內容，讀屏與「在頁面中尋找」都完全碰不到（引用："they also make that content completely inaccessible to screen readers and browser features like "Find in page"."）
- 退路：保住主要行為——一般摺疊可用廣泛支援的 `<details>`；`until-found` 在 Safari 偵測缺失時展開全部內容維持可搜可讀
- 解鎖：隱藏折疊或自訂面板的內容仍能被「在頁面中尋找」與文字片段連結命中並自動展開同步介面狀態

經過：分頁、自訂手風琴裡的文字 Ctrl+F 找不到，分享出去的文字片段連結也打不開。換成 until-found，搜尋命中時瀏覽器自己展開並觸發 beforematch，讓按鈕狀態跟上。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：<details>：Widely；hidden="until-found"：Limited availability，Supported by: Chrome 102, Edge 102, Firefox 148；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前自訂分頁的內容對搜尋隱形 → 現在設定頁的多個分頁、文件站的分頁式程式碼範例、產品規格的切換面板可以被 Ctrl+F 與文字片段連結直接命中並切到對的分頁。Safari 退回全部展開
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:search-hidden-content:2" %%
## 不要在 `hidden="until-found"` 元素上再設 `display` 或 `visibility`
- 做法：隱藏完全交給 `hidden="until-found"`，不另外寫 `display: none`、`visibility: hidden` 等樣式
- 對手：這些樣式會破壞原生行為，內容永遠從搜尋索引消失（引用："This breaks the native functionality and permanently hides the content from the search index."）
- 退路：保住主要行為——Safari 原本就走展開退路不會受隱藏樣式影響，支援瀏覽器不覆寫即能被搜尋命中
- 解鎖：（缺）

經過：為了保險又加了一行 `display: none`，結果 until-found 等於沒寫。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：hidden="until-found"：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「隱藏或停用把人擋在外面」

%% line-start id="mwg:search-hidden-content:3" %%
## 邊框、內距、背景放在內層 wrapper，不放在 until-found 元素本身
- 做法：把框線、padding、背景套在子層 wrapper
- 對手：直接套在 `hidden="until-found"` 元素上，隱藏時會留下版面位移或視覺殘影（引用："This prevents unintended layout shifts or visual remnants while the element is hidden."）
- 退路：保住主要行為——樣式移至內層 wrapper 在原生隱藏與 Safari 展開退路下都能呈現乾淨版面
- 解鎖：（缺）

經過：收起的面板還留著一條空的邊框和一段高度。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：hidden="until-found"：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:search-hidden-content:4" %%
## 敏感或不相關的資料不要用 `hidden="until-found"` 藏
- 做法：敏感資訊、內部資料 token、不該被搜到的內容不放在 until-found 區塊裡
- 對手：until-found 的內容會被頁內搜尋找到並展開（引用："**DO NOT** use `hidden="until-found"` for sensitive information, internal data tokens, or irrelevant data that should not be exposed via search."）
- 退路：保住主要行為——原本就不將敏感資料放進前端頁面，原生與 Safari 展開退路下皆不會外露
- 解鎖：（缺）

經過：以為藏起來就安全，使用者一搜就把內部欄位翻了出來。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：hidden="until-found"：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：不要拿 `hidden="until-found"` 取代「只給讀屏」的 `.sr-only` 文字
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
