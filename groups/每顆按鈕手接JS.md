---
group: 每顆按鈕手接JS
group_en: Wiring JS to every button
lines: 4
guides: 4
tags: [對手組]
---

# 每顆按鈕手接JS

4 條線，出自 4 份指南。

- 類型：新能力 4
- 戰報：部分改善 4
- 退路：保住主要行為 4

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/user-experience/content-first-noise-reduction#次要介面收進 `popover` 與抽屜，不放常駐工具列或自寫 JS 浮層\|次要介面收進 `popover` 與抽屜，不放常駐工具列或自寫 JS 浮層]] | content-first-noise-reduction | 新能力 | 部分改善 | 指南只說用 popover 取代常駐工具列與自寫 JS 浮層，沒說那些做法在哪個時刻出錯 |
| [[lines/ui-components/copy-button#用 Invoker Commands 宣告複製目標\|用 Invoker Commands 宣告複製目標]] | copy-button | 新能力 | 部分改善 | 指南只說要取代 "per-button JavaScript wiring"，沒有指出舊寫法具體在哪個時刻出問題 |
| [[lines/ui-behaviors/custom-button-actions#用 `command="--自訂指令"` 宣告按鈕要對誰做什麼\|用 `command="--自訂指令"` 宣告按鈕要對誰做什麼]] | custom-button-actions | 新能力 | 部分改善 | 指南只說能減少手動事件監聽、讓介面與實作脫鉤，沒說手接監聽在哪個時刻出問題 |
| [[lines/ui-behaviors/declarative-dialog-popover-control#用 `command="show-modal"`、`toggle-popover` 從 HTML 開關對話框\|用 `command="show-modal"`、`toggle-popover` 從 HTML 開關對話框]] | declarative-dialog-popover-control | 新能力 | 部分改善 | 指南只說可移除脆弱的樣板程式、HTML 解析完就能互動，沒說手寫監聽器在哪個時刻出問題 |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/隱藏或停用把人擋在外面|隱藏或停用把人擋在外面]]（3）
- [[groups/不認得的語法讓整條規則失效|不認得的語法讓整條規則失效]]（1）
- [[groups/事件不冒泡收不到|事件不冒泡收不到]]（1）
- [[groups/兩套機制重複作用|兩套機制重複作用]]（1）
- [[groups/捲動連動效果靠JS監聽|捲動連動效果靠JS監聽]]（1）
- [[groups/沒防護不支援的瀏覽器|沒防護不支援的瀏覽器]]（1）
- [[groups/焦點或狀態指示消失|焦點或狀態指示消失]]（1）

← [[groups/對手組總覽|對手組總覽]]
