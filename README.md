# web-tension-lines

**繁體中文** · [English](README.en.md)

**線上瀏覽：https://iantpe.github.io/web-tension-lines/**（可搜尋、可篩選、可展開）

每週檢查 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) 的新指南，用張力句四槽（誰在做／動作＋對象／被什麼擋／戰報）拆成問題線。拆出來的不是功能清單，而是「哪個新做法擋掉了哪個老問題」，再從「擋掉之後什麼變得做得到」去想新應用。

## 什麼是「問題線」

一條問題線用四個槽記下一個問題的形狀：

| 槽 | 問的是 | 例子（`dynamic-sort` 指南） |
|---|---|---|
| 誰在做 | 行動者 | 開發者 |
| 動作＋對象 | 用什麼做法處理什麼 | 排序時用 `moveBefore()` 搬動既有節點 |
| 被什麼擋 | 舊做法具體在哪個時刻出事 | 用 `innerHTML` 重建清單，焦點、捲動位置、圖片狀態全部丟失 |
| 戰報 | 換了做法之後，同一個問題退了多少 | 部分改善：焦點保住了，但 Safari 不支援 `moveBefore()` |

重點在第三、四槽。「被什麼擋」要指得出一個看得到的現象，「效能不好」「寫起來麻煩」這種只有標籤的不算。「戰報」要回答**同一個**問題有沒有退，「很方便」「比較現代」不算。指南沒寫到的槽就判「缺」，不替它補。

這樣拆的好處是：好幾份指南擋的如果是同一個對手（例如都在處理「隱藏方式把鍵盤使用者擋在外面」），在 `ledger.csv` 按「對手組」一篩就看得到。

四槽來自 [ctxfst](https://github.com/ctxfst) 的張力句四槽教練，原始定義見 [skill-line-coach/references/four-slot-coach.md](https://github.com/ctxfst/skill-line-coach/blob/main/references/four-slot-coach.md)。原本是寫筆記時用的教練規則，這裡把它拿來拆別人寫的功能指南；調整過的地方（例如「誰在做」固定為開發者、戰報依瀏覽器支援度分級）寫在 [PROMPT.md](PROMPT.md)。

## 結構

| 路徑 | 內容 |
|---|---|
| `lines/<分類>/<guide-id>.md` | 一份指南一個檔，裡面一到三條問題線。每條線包在 `%% line-start id="…" %%` 和 `%% line-end %%` 之間（Obsidian 的註解語法，畫面上看不到），格式照 [CtxFST 規格](https://github.com/ctxfst/skill-line-coach/blob/main/references/ctxfst-spec.md)，可直接用 skill-line-coach 的 `shape_layer.py` 逐條建索引；標記外的「細節」是給人看的補充 |
| `ledger.csv` | 累積表，一條線一列；按「對手組」篩選可以看到哪些老問題被反覆對付 |
| `weekly/<日期>.md` | 每期週記：這週的對手、僵持中的線、**本週靈感**（用新能力組出的應用點子與小 demo） |
| `docs/index.html` | 一頁看完所有線：可搜尋（Ctrl+F 也找得到摺起來的內容）、按類型和戰報篩選、按對手組或指南分組。由 `scripts/build_page.py` 產生，每週自動重建 |
| `wants.md` | 你自己「想做但卡住的事」。有寫東西時，週記會多一節「對到你的清單」，列出剛好擋掉這些問題的新功能 |
| `PROMPT.md` | 每週自動任務的完整指示 |
| `scripts/weekly.sh` | 抓上游、算差異、叫 `claude -p` 跑 PROMPT.md |
| `state.json` | 上次處理到的上游 commit |

## 判讀

- **戰報**：`勝`（Widely available，對手消失）、`部分改善`（Newly 或 fallback 會失去部分好處）、`僵持`（Limited 或沒有瀏覽器支援）、`缺`（指南沒說改善了什麼）。
- **證據**：一律 `宣稱`，因為戰報來自官方指南。自己在瀏覽器實測過的，手動改成 `實測`。
- **類型**：`新能力`（新平台功能讓某件事變得可行）或 `糾錯`（糾正常見錯誤，用的是早就能用的功能）。找靈感時只看新能力。
- **解鎖**：新能力的線才有，一句話寫「以前卡在哪 → 現在能做出什麼」。這是發想，不是指南原文。
- **槽3 = 缺**：指南推薦了新做法，卻沒說舊做法具體壞在哪。

## 排程

使用者 crontab，每週三 09:00（上游多在週一、週二發版）：

```
0 9 * * 3 /path/to/web-tension-lines/scripts/weekly.sh
```

上游沒有新 commit 就直接結束，不呼叫 claude。有拆出新線時，腳本會自動 commit 並 push 到 `origin main`。執行紀錄在 `logs/<日期>.log`（不進 git）。手動跑一次：`scripts/weekly.sh`。

## 授權

上游指南為 CC-BY 4.0。這裡的引文與摘要若要公開發表，請標註來源：GoogleChrome/modern-web-guidance。
