# web-tension-lines

每週檢查 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) 的新指南，用張力句四槽（誰在做／動作＋對象／被什麼擋／戰報）拆成問題線。拆出來的不是功能清單，而是「哪個新做法擋掉了哪個老問題」。

四槽定義來自 `fieldline-lab/meta/知識庫設計/張力句訓練器：四槽檢查、結構寫作應用設計.md`，套用到功能指南時的調整寫在 [PROMPT.md](PROMPT.md)。

## 結構

| 路徑 | 內容 |
|---|---|
| `lines/<分類>/<guide-id>.md` | 一份指南一個檔，裡面一到三條問題線，CtxFST 格式（`%% line-start %%`），可直接給 `shape_layer.py` 建索引 |
| `ledger.csv` | 累積表，一條線一列；按「對手組」篩選可以看到哪些老問題被反覆對付 |
| `weekly/<日期>.md` | 每期週記：這週的對手、僵持中的線、上游 issue 候選 |
| `PROMPT.md` | 每週自動任務的完整指示 |
| `scripts/weekly.sh` | 抓上游、算差異、叫 `claude -p` 跑 PROMPT.md |
| `state.json` | 上次處理到的上游 commit |

## 判讀

- **戰報**：`勝`（Widely available，對手消失）、`部分改善`（Newly 或 fallback 會失去部分好處）、`僵持`（Limited 或沒有瀏覽器支援）、`缺`（指南沒說改善了什麼）。
- **證據**：一律 `宣稱`，因為戰報來自官方指南。自己在瀏覽器實測過的，手動改成 `實測`。
- **槽3 = 缺**：指南推薦了新做法，卻沒說舊做法具體壞在哪。這些通常就是值得回報上游的地方。

## 排程

使用者 crontab，每週三 09:00（上游多在週一、週二發版）：

```
0 9 * * 3 /home/iand03/GitHub/web-tension-lines/scripts/weekly.sh
```

上游沒有新 commit 就直接結束，不呼叫 claude。有拆出新線時，腳本會自動 commit 並 push 到 `origin main`。執行紀錄在 `logs/<日期>.log`（不進 git）。手動跑一次：`scripts/weekly.sh`。

## 授權

上游指南為 CC-BY 4.0。這裡的引文與摘要若要公開發表，請標註來源：GoogleChrome/modern-web-guidance。
