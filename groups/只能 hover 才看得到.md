---
group: 只能 hover 才看得到
group_en: Only reachable by hover
lines: 9
guides: 9
tags: [對手組]
---

# 只能 hover 才看得到

9 條線，出自 9 份指南。

- 類型：新能力 4、糾錯 5
- 戰報：勝 5、部分改善 4
- 退路：不需要 5、保住主要行為 4

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/ui-components/hovercard#用 `interestfor` 讓連結在 hover 與聚焦時都叫出預覽卡\|用 `interestfor` 讓連結在 hover 與聚焦時都叫出預覽卡]] | hovercard | 新能力 | 部分改善 | 指南只說能確保 hover 與聚焦都出現，沒說舊做法哪裡壞 |
| [[lines/ui-behaviors/interest-triggered-action-previews#用 `interestfor` 在按下之前預覽動作效果\|用 `interestfor` 在按下之前預覽動作效果]] | interest-triggered-action-previews | 新能力 | 部分改善 | 指南只說讓使用者在確定前預覽動作會有幫助，沒說舊做法在哪個時刻出問題 |
| [[lines/user-experience/natural-interactions#選單可以 hover 開，但不能只靠 hover\|選單可以 hover 開，但不能只靠 hover]] | natural-interactions | 新能力 | 部分改善 | 只在 hover 時開選單，鍵盤和觸控使用者打不開 |
| [[lines/ui-atoms/single-line-overflow#讓被截斷的全文對鍵盤與觸控也找得到\|讓被截斷的全文對鍵盤與觸控也找得到]] | single-line-overflow | 新能力 | 部分改善 | 只靠 `title` 屬性顯示全文，鍵盤和觸控使用者都碰不到 |
| [[lines/accessibility/accessibility#不用 title 當控制項名稱\|不用 title 當控制項名稱]] | accessibility | 糾錯 | 勝 | `title` 只在滑鼠 hover 顯示，任何瀏覽器都無法用鍵盤取得 |
| [[lines/html/html#不要用 title 屬性做提示\|不要用 title 屬性做提示]] | html | 糾錯 | 勝 | `title` 產生的提示無法用鍵盤取得 |
| [[lines/ui-atoms/pull-to-reveal#每個下拉動作都要有一顆可見的按鈕\|每個下拉動作都要有一顆可見的按鈕]] | pull-to-reveal | 糾錯 | 勝 | 只能靠下拉手勢叫出的功能，不符合 WCAG 2.5.1 路徑型手勢要求 |
| [[lines/ui-behaviors/swipe-to-remove#每個滑動動作都要有可見按鈕當替代\|每個滑動動作都要有可見按鈕當替代]] | swipe-to-remove | 糾錯 | 勝 | 只能滑動的功能無法用鍵盤、單擊或讀屏完成，違反 WCAG 2.5.1 |
| [[lines/ui-behaviors/swipe-to-reveal#滑開才看得到的動作，要有觸發按鈕可以打開\|滑開才看得到的動作，要有觸發按鈕可以打開]] | swipe-to-reveal | 糾錯 | 勝 | 只能靠滑動取得的功能，違反 WCAG 2.5.1 |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/原生捲動手勢不合用途|原生捲動手勢不合用途]]（3）
- [[groups/播報時機或可靠度出錯|播報時機或可靠度出錯]]（3）
- [[groups/播報過量|播報過量]]（3）
- [[groups/焦點或狀態指示消失|焦點或狀態指示消失]]（3）
- [[groups/自製控制項丟掉原生行為|自製控制項丟掉原生行為]]（3）
- [[groups/隱藏或停用把人擋在外面|隱藏或停用把人擋在外面]]（3）
- [[groups/不認得的語法讓整條規則失效|不認得的語法讓整條規則失效]]（2）
- [[groups/內容要等JS才成形|內容要等JS才成形]]（2）
- [[groups/手寫焦點管理|手寫焦點管理]]（2）
- [[groups/生命週期假設錯|生命週期假設錯]]（2）
- [[groups/語意結構失真|語意結構失真]]（2）
- [[groups/事件不冒泡收不到|事件不冒泡收不到]]（1）

← [[groups/對手組總覽|對手組總覽]]
