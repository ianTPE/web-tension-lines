# 每週任務：把 modern-web-guidance 的新指南拆成問題線

你在 repo 根目錄（目前工作目錄）執行；下面所有路徑都是相對於這裡，不要讀寫這個目錄以外的地方。`scripts/weekly.sh` 已經把上游 `GoogleChrome/modern-web-guidance` 抓到 `.cache/upstream`，並把本週差異寫進 `.cache/diff.txt`（`git diff --name-status <上次 commit> <這次 commit> -- skills/modern-web-guidance/guides`）。環境變數 `MWG_FROM`、`MWG_TO`、`MWG_RELEASE` 給出兩個 commit 與版本名。

上游指南路徑：`.cache/upstream/skills/modern-web-guidance/guides/<分類>/<guide-id>.md`

## 範圍

- `A`（新增）：每份都拆，寫成問題線。
- `M`（修改）：先看 `git -C .cache/upstream diff $MWG_FROM $MWG_TO -- <檔案>`。
  - 本 repo 已有 `lines/<分類>/<guide-id>.md`：只在**對手、戰報或支援狀態**變了時改那條線，並在線尾的「變更紀錄」記一行。
  - 沒有線檔、且這次改動是新增整段做法（新增 ≥40 行 prose，不算程式碼）：當成新增處理。
  - 其他（措辭、程式碼範例、連結）：不拆，只在週記列出檔名。
- `D`／`R`（刪除、改名）：在線檔頂端加 `> 上游已刪除／改名為 …（日期）`，不刪檔；ledger 對應列的「狀態」改成 `上游已刪除` 或 `改名`。
- 一次超過 20 份要拆時，只拆前 20 份（依路徑排序），其餘在週記列為「待拆」，下週優先處理。

## 四槽

四槽原始定義見 https://github.com/ctxfst/skill-line-coach/blob/main/references/four-slot-coach.md ；以下是套用到功能指南時的版本。這些是別人寫的功能指南，不是自己的筆記；這裡一律把它們當成「解決問題」的文字來拆：有人用某個做法對付某個問題。

1. **誰在做**：固定為「開發者（或寫程式的代理）」，指南若指定角色（例如「內容作者」「擴充功能開發者」）就照指南。
2. **動作＋對象**：用哪個平台功能／做法，處理哪個介面或行為。寫出功能名（`moveBefore()`、`focusgroup`、`<details name>`）。
3. **被什麼擋**：舊做法或常見錯誤的**具體**後果，要能指到一個可觀察的現象，並引用指南原文（英文原句，短引）。
   - 「臃腫的 JS」「體驗不好」「不夠現代」這類只有標籤、指不到現象的，判**缺**。
   - 指南只有做法、沒說舊做法哪裡壞，判**缺**。不要替指南補對手。
4. **戰報**：換成新做法後，同一個對手退了多少。只能寫指南宣稱的內容，並依支援狀態分類：
   - `勝`：功能已 Baseline Widely available，對手直接消失。
   - `部分改善`：Newly available，或 fallback 能保住主要行為但失去部分好處。
   - `僵持`：Limited availability／沒有任何主要瀏覽器支援，實務上仍得用舊做法。
   - `缺`：指南沒說新做法對那個對手有什麼影響。

指南完全沒有瀏覽器支援資料時（工具鏈、WebAssembly 建置這類），支援狀態寫 `不適用`，戰報只看指南宣稱：說對手消失為 `勝`，說改善但有代價或限制為 `部分改善`，沒說改善了什麼為 `缺`。不要自行補外部支援資料，也不要發明其他分類。

**已驗證的支援資料偏差**（照這裡判，不照指南原文）：

- **Anchor positioning**：指南寫 "Supported by: Safari 27 … Unsupported in: Chrome, Edge, and Firefox"，那是 web-features 整個群組的狀態，只因 `position-visibility: anchor-valid / anchor-visible` 兩個值而拖累。若該線沒用到 `position-visibility`，支援狀態記 `Newly`（核心屬性 2026-01-13 起 Baseline），並在細節註明「群組狀態誤導，見 `lines/ui-components/app-menus.md`」。（2026-11-12 驗證，web-features 3.45.0）

每條線的戰報都是**官方宣稱**，在 ledger 的「證據」欄寫 `宣稱`。只有使用者自己實測過的才改成 `實測`（自動任務永遠不寫 `實測`）。

一份指南可能有兩條以上的問題線（對手不同就分開）。超過三條時，只寫前三條（依指南出現順序），在線檔尾註明「另有 N 條未拆」。

## 輸出

### 1. 線檔 `lines/<分類>/<guide-id>.md`

格式照 CtxFST（https://github.com/ctxfst/skill-line-coach/blob/main/references/ctxfst-spec.md ）：四槽與一段短敘述放在 `%% line-start %%`／`%% line-end %%` 標記內，細節放標記外；程式只擷取標記內的文字。標記內約 300–900 字。

```markdown
---
guide: <guide-id>
category: <分類>
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/<分類>/<guide-id>.md
first_seen: <YYYY-MM-DD>（<版本>）
license: CC-BY-4.0（上游指南）
---

# <指南標題中譯>

%% line-start id="mwg:<guide-id>" %%
## <一句話：用 X 擋掉 Y>
- 誰在做：…
- 動作＋對象：…
- 被什麼擋：…（引用："…"）
- 戰報：<勝／部分改善／僵持／缺>——…（官方宣稱）

經過：兩到四句，說清楚舊做法在哪個時刻出事、新做法怎麼避開、還剩什麼沒解決。
%% line-end %%

### 細節（不索引）
- 對手組：<見 ledger 的對手組>
- 支援狀態：<功能>：<Baseline 狀態／Supported by 原句>
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有或缺／戰報 有或缺
- 類型：新能力／糾錯（見下）
- 解鎖（發想，非指南原文）：<只有新能力才寫>
- 變更紀錄：<YYYY-MM-DD>（<版本>）首次拆出
```

第二條線的 id 用 `mwg:<guide-id>:2`。

### 2. 累積表 `ledger.csv`

每條線一列，追加，不重寫舊列（修改時改該列）。欄位固定：

`日期,版本,guide_id,line_id,功能,對手組,對手,戰報,支援狀態,證據,槽3,類型,解鎖,狀態`

- `對手組`：先用 `ledger.csv` 已有的組名；真的對不上才新增，並在週記說明為什麼新開一組。
- `支援狀態`：取該線關鍵功能的最低狀態：`Widely`／`Newly`／`Limited`／`無瀏覽器支援`／`不適用`。
- `類型`、`解鎖`：見第 4 節；糾錯的 `解鎖` 留空。
- `狀態`：`有效`、`上游已刪除`、`改名`。
- 欄位內有逗號時用雙引號包起來。

### 3. 週記 `weekly/<YYYY-MM-DD>.md`

```markdown
# <YYYY-MM-DD> 週記：modern-web-guidance <版本>

- 上游範圍：<from>..<to>，新增 N、修改 N、刪除 N
- 本週拆出：N 條線（N 份指南）

## 這週的對手
按對手組列，每組一行：組名——哪幾條線，一句話說這組的共同形狀。
標出**重複出現**的對手（跨週累計 ≥3 條線的組，查 ledger）。

## 僵持中的線
戰報為「僵持」的線，各一行：功能、卡在哪個瀏覽器。

## 本週靈感
本週新能力 N 條。用新能力組出 3～5 個應用點子（本週新能力太少時，可以和 ledger 裡舊的新能力組合），每個點子包含：
- 一句話：做出來的東西是什麼、誰會用
- 用到：哪幾條線（line_id）與功能
- 限制：支援度，以及退回 fallback 時會失去什麼
- 小 demo：一個一個晚上做得完的最小版本
沒有新能力就寫「本週無新能力」，不要硬湊。

## 糾錯備忘
本週糾錯類的對手組，一行列完。

## 未拆
修改但未拆的檔名，一行一個；「待拆」清單。
```

### 4. 類型與解鎖

這個 repo 的目的是**靈感**：從新功能想到新應用。所以每條線要分類：

- `新能力`：關鍵功能是平台新增的（Newly、Limited、無支援，或指南明說是新 API），而且它讓某件以前做不到或代價很高的事變得可行。
- `糾錯`：用的是早已 Widely 的做法，只是糾正常見錯誤。對做東西有用，但不產生新應用。

新能力要寫 `解鎖`：一到兩句，說「以前卡在哪 → 現在能做什麼樣的東西」。
- 必須從該線的戰報推得出來；支援受限時寫出來（例如「目前僅 Chromium」）。
- 這是發想，放在線標記外的細節裡，不放進四槽，也不寫成指南的宣稱。
- 寫成具體的東西（「可重排的即時儀表板」），不要寫成形容詞（「更流暢的體驗」）。

### 5. 結束

最後更新 `state.json` 的 `last_commit`、`last_release`、`last_run`。`scripts/weekly.sh` 會在你結束後檢查這一步。

結束時的總結用繁體中文寫，它會留在 `logs/` 給使用者看。

## 邊界

- 四槽只根據上游指南原文判斷；每個對手與戰報都要能指回原句。發想只出現在「解鎖」與「本週靈感」，並標明是發想。
- 不替指南補它沒寫的對手或成效；不為湊齊四槽牽強加料。
- 不改動上游檔案、不開 issue、不推送任何東西（commit 與 push 由腳本負責）。
- 不修改 `PROMPT.md`、`README.md`、`scripts/`。
