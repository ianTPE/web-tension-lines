# web-tension-lines

**繁體中文** · [English](README.en.md)

**[線上瀏覽](https://iantpe.github.io/web-tension-lines/)**（可搜尋、可篩選、可展開；[英文版](https://iantpe.github.io/web-tension-lines/en/)、[週記](https://iantpe.github.io/web-tension-lines/weekly/)、[demo](https://iantpe.github.io/web-tension-lines/demos/ledger-chart/)、[靈感](https://iantpe.github.io/web-tension-lines/ideas/)、[對手組關係圖（英文）](https://iantpe.github.io/web-tension-lines/en/graph/)）

每週檢查 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) 的新指南，用張力句四槽（做法／對手／退路／解鎖）拆成問題線。拆出來的不是功能清單，而是「哪個新做法擋掉了哪個老問題、退回時怎麼辦」，再從「解鎖」與「發想」去想新應用。

## 什麼是「問題線」

一條問題線用四個槽記下一個問題的形狀：

| 槽 | 問的是 | 例子（`dynamic-sort` 指南） |
|---|---|---|
| 做法 | 用什麼做法處理什麼 | 排序時用 `moveBefore()` 把既有節點搬到新順序 |
| 對手 | 舊做法具體在哪個時刻出事 | 用 `innerHTML` 重建清單，焦點、捲動位置、圖片狀態全部丟失 |
| 退路 | 不支援時怎麼退、失去什麼 | 保住主要行為——Safari 缺 `moveBefore()` 改用 `append()`，順序正確但項目內焦點與狀態會重設 |
| 解鎖 | 從指南原文來看現在做得到什麼 | 不用重建 DOM 就能把既有項目直接搬到新順序，保住項目內焦點、iframe 與動畫狀態 |

重點在對手、退路與解鎖。「對手」要指得出一個看得到的現象，「效能不好」「寫起來麻煩」這種只有標籤的不算。「退路」四選一並寫出退回後失去什麼。「解鎖」必須能指回指南原文；指南沒寫到的對手或解鎖就記「缺」，不替它補。

這樣拆的好處是：好幾份指南擋的如果是同一個對手（例如都在處理「隱藏方式把鍵盤使用者擋在外面」），在 `ledger.csv` 按「對手組」一篩就看得到。

四槽來自 [ctxfst](https://github.com/ctxfst) 的張力句四槽教練，原始定義見 [skill-line-coach/references/four-slot-coach.md](https://github.com/ctxfst/skill-line-coach/blob/main/references/four-slot-coach.md)。原本是寫筆記時用的教練規則，這裡把它拿來拆別人寫的功能指南；遷移到槽 v2 的調整（包括退路分類、由規則推出戰報）寫在 [PROMPT.md](PROMPT.md)。

## 結構

| 路徑 | 內容 |
|---|---|
| `lines/<分類>/<guide-id>.md` | 一份指南一個檔，裡面一到三條問題線。每條線包在 `%% line-start id="…" %%` 和 `%% line-end %%` 之間（Obsidian 的註解語法，畫面上看不到），格式照 [CtxFST 規格](https://github.com/ctxfst/skill-line-coach/blob/main/references/ctxfst-spec.md)，可直接用 skill-line-coach 的 `shape_layer.py` 逐條建索引；標記外的「細節」是給人看的補充 |
| `ledger.csv` | 累積表，一條線一列；按「對手組」篩選可以看到哪些老問題被反覆對付 |
| `weekly/<日期>.md` | 每期週記：這週的對手、僵持中的線、**本週靈感**（用新能力組出的應用點子與小 demo） |
| `docs/index.html`、`docs/en/index.html` | 一頁看完所有線（中文版、英文版）：可搜尋（Ctrl+F 也找得到摺起來的內容）、按類型和戰報篩選、按對手組或指南分組。由 `scripts/build_page.py` 產生，每週自動重建 |
| `docs/ideas/`、`docs/en/ideas/` | 靈感頁：只列新能力的線，依「現在能不能用」分成今天就能用、漸進增強、只在支援的瀏覽器有效、先追蹤，可依主題篩選。由 `scripts/build_ideas.py` 每週重建 |
| `docs/en/graph/` | 對手組關係圖（英文網頁）：每個對手組一個圓，出現在同一份指南就連線，點進去看該組的線。由 `scripts/build_graph.py` 每週重建 |
| `docs/weekly/` | 週記的網頁版：目錄頁加每篇一頁，週記裡的 `mwg:…` 可以點，會跳到主頁並展開那條線。由 `scripts/build_weekly.py` 產生 |
| `docs/demos/` | 用新能力做的模組 demo。目前有 `ledger-chart/`：用 HTML-in-Canvas 畫的對手組戰報圖，標籤是真 DOM，可搜尋、可匯出（僅 Chrome 157 起，其他瀏覽器走 fallback）。資料由 `scripts/build_demo.py` 從 `ledger.csv` 產生 |
| `groups/` | 每個對手組一頁的 Obsidian 索引（加一頁 `對手組總覽`）：列出該組的線、常一起出現的組。用 Obsidian 開這個 repo、打開關係圖，就看得到哪些對手常在同一份指南出現。由 `scripts/build_groups.py` 每週重建 |
| `docs/demos/` 底下其餘 | 可以直接在瀏覽器試的新能力小範例（錯開進場、滑動底線、捲動進出場、手風琴、自動對比文字、宣告式按鈕、預覽卡、深淺色 token），每頁先檢查支援度、不支援時示範退路。總覽在 `docs/demos/index.html`，手寫，不由腳本產生 |
| `i18n/en.json` | 英文版網頁用的譯文。線檔維持中文，每週任務會替新線補上譯文；缺譯時英文頁退回顯示中文 |
| `wants.md` | 你自己「想做但卡住的事」。有寫東西時，週記會多一節「對到你的清單」，列出剛好擋掉這些問題的新功能 |
| `.agents/skills/web-tension-lines/` | 顧問型 Agent Skill：從開發者描述的阻礙檢索相關線，回報新做法、戰報、限制與原文 |
| `PROMPT.md` | 每週自動任務的完整指示 |
| `scripts/weekly.sh` | 抓上游、算差異、叫 `claude -p` 跑 PROMPT.md |
| `state.json` | 上次處理到的上游 commit |

## 判讀

- **退路**：瀏覽器不支援時怎麼退、失去什麼，四選一加一句說明：`不需要`（`Widely` 或 `不適用`）、`保住主要行為`、`失去主要好處`、`沒說`。
- **戰報**：不直接判，由 `支援狀態` 與 `退路` 規則推出：`勝`（`Widely` 或 `不適用`）、`部分改善`（`Newly` 或退路為 `保住主要行為`）、`僵持`（其餘）。不再有 `缺`。
- **證據**：一律 `宣稱`，因為資料來自官方指南。自己在瀏覽器實測過的，手動改成 `實測`。
- **類型**：`新能力`（新平台功能讓某件事變得可行）或 `糾錯`（糾正常見錯誤，用的是早就能用的功能）。找靈感時只看新能力。
- **解鎖**：來自指南原文的具體可達成能力，能指回原句；沒有就寫 `（缺）`。
- **發想（非指南原文）**：新能力的線才有的延伸應用點子，「以前卡在哪 → 現在能做出什麼」，不是指南原文。
- **對手有無 = 缺**：指南推薦了新做法，卻沒說舊做法具體壞在哪。

## Agent Skill

Kimi Code 會自動發現專案內的 `.agents/skills/web-tension-lines/SKILL.md`。可手動呼叫：

```text
/skill:web-tension-lines 以前不敢做可拖曳的儀表板，因為圖表一搬就重新載入
```

skill 會用症狀與對手檢索一到三條相關線，附上戰報、支援限制、證據狀態與上游指南；不會自動改碼或開 issues。其他支援 Agent Skills 的工具可把同一目錄複製或連結到自己的 skills 掃描目錄。

也可不透過代理直接檢索，只需要 Python 3，沒有第三方依賴：

```bash
python3 .agents/skills/web-tension-lines/scripts/search.py --kind 新能力 --limit 3 "拖曳 圖表 重新載入"
python3 .agents/skills/web-tension-lines/scripts/search.py --id mwg:move-dom-element-without-losing-state --json
```

查詢同時比對中英文；加 `--lang en` 可輸出英文。詳細選項見 `--help`。

## 排程

使用者 crontab，每週三 09:00（上游多在週一、週二發版）：

```
0 9 * * 3 /path/to/web-tension-lines/scripts/weekly.sh
```

上游沒有新 commit 就直接結束，不呼叫 claude。有拆出新線時，腳本會自動 commit 並 push 到 `origin main`。執行紀錄在 `logs/<日期>.log`（不進 git）。手動跑一次：`scripts/weekly.sh`。

## 授權

上游指南為 CC-BY 4.0。這裡的引文與摘要若要公開發表，請標註來源：GoogleChrome/modern-web-guidance。
