---
guide: interactive-content-reveal
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/interactive-content-reveal.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 互動式內容揭露

%% line-start id="mwg:interactive-content-reveal" %%
## 用 `@property` 註冊漸層停點，讓跟著游標的聚光燈平滑開合
- 做法：用 `@property` 把 `--inner-size`、`--outer-size` 註冊成 `<length-percentage>`，`mask-image: radial-gradient(circle at var(--mouse-x) var(--mouse-y), …)` 引用它們，只對尺寸做 `transition`；`pointermove` 只更新位置變數
- 對手：不支援 `@property` 的瀏覽器無法在 `radial-gradient` 裡內插數值，聚光燈只能在開與關之間跳（引用："the movement will jump between on and off states because they cannot interpolate values inside a `radial-gradient`"）
- 退路：失去主要好處——退回未註冊變數的遮罩，聚光燈仍在但開合會跳
- 解鎖：將漸層停點註冊為有型別的屬性後，只需少量座標更新腳本就能平滑開合跟著游標的聚光燈效果

經過：漸層裡的數字預設不能動畫，聚光燈只能瞬間出現。把停點註冊成有型別的屬性，瀏覽器就知道怎麼在兩個大小之間過渡。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Registered custom properties：Newly（2024-07-09）；Masks：Widely
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前漸層裡的尺寸無法過渡 → 現在作品集的「手電筒看底稿」、前後對照圖的圓形放大鏡、產品圖的 X 光效果可以只用一小段座標 JS 做出平滑開合
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:interactive-content-reveal:2" %%
## 聚光燈只當裝飾，不能擋住或藏起內容
- 做法：遮罩層設 `pointer-events: none`；底下的內容預設就完整可見、可用鍵盤到達，聚光燈只是給指標使用者的額外效果
- 對手：拿這個效果遮住或把關必要內容時，只用鍵盤或輔助技術的人拿不到內容；遮罩層也會擋住下面控制項的點擊（引用："Never use this effect to obscure or gate essential content from keyboard-only or assistive technology users."）
- 退路：不需要——底層內容預設完整可見並以 pointer-events: none 讓出互動，所有裝置皆可到達
- 解鎖：（缺）

經過：「移過去才看得到」很有趣，但只有拿滑鼠的人能玩；內容本身要先對所有人敞開。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：無障礙要求：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：減少動態偏好下關掉過渡；放大到 200%／400% 仍可用、每秒閃爍不超過三次
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
