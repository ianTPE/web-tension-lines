---
group: 重建DOM丟狀態
group_en: Rebuilding the DOM loses state
lines: 10
guides: 10
tags: [對手組]
---

# 重建DOM丟狀態

10 條線，出自 10 份指南。

- 類型：新能力 5、糾錯 5
- 戰報：勝 3、部分改善 4、僵持 3
- 退路：不需要 3、保住主要行為 3、失去主要好處 3、沒說 1

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/html/custom-elements#用 connectedMoveCallback 接住 moveBefore() 的搬移，擋掉搬一次就重來\|用 connectedMoveCallback 接住 moveBefore() 的搬移，擋掉搬一次就重來]] | custom-elements | 新能力 | 僵持 | 一般搬動會先 `disconnectedCallback` 再 `connectedCallback`，昂貴或看得出來的… |
| [[lines/ui-behaviors/dynamic-sort#搬既有節點排序，不用 innerHTML 重建\|搬既有節點排序，不用 innerHTML 重建]] | dynamic-sort | 新能力 | 部分改善 | 用 `innerHTML` 或整批重新 render 產生新節點，焦點、項目內捲動位置、圖片狀態全部丟失，view tr… |
| [[lines/ui-behaviors/highlight-text-ranges#用 CSS Custom Highlight API 標示文字，不動 DOM\|用 CSS Custom Highlight API 標示文字，不動 DOM]] | highlight-text-ranges | 新能力 | 部分改善 | 把符合的文字包進 <mark> 會改動 DOM，可能弄掉事件監聽器、弄壞文件結構 |
| [[lines/ui-behaviors/move-dom-element-without-losing-state#用 `moveBefore()` 搬元素，iframe 不重載、焦點不丟\|用 `moveBefore()` 搬元素，iframe 不重載、焦點不丟]] | move-dom-element-without-losing-state | 新能力 | 僵持 | 傳統搬法先移除再插入：iframe 重新載入、CSS 動畫重頭開始、輸入欄位失去焦點 |
| [[lines/ui-behaviors/persistent-top-layer-ui#用 `moveBefore()` 搬動開著的對話框、popover、全螢幕元素而不關閉\|用 `moveBefore()` 搬動開著的對話框、popover、全螢幕元素而不關閉]] | persistent-top-layer-ui | 新能力 | 僵持 | 傳統搬法先移除再插入，開著的模態、popover 與全螢幕元素突然關閉 |
| [[lines/built-in-ai/language-model#AI 改寫保留版本、比較與復原，不覆蓋唯一草稿\|AI 改寫保留版本、比較與復原，不覆蓋唯一草稿]] | language-model | 糾錯 | 部分改善 | 直接覆蓋會讓使用者失去原本草稿或較好的上一版，無法回頭 |
| [[lines/performance/out-of-order-html-streaming#佔位被替換時，焦點不能跟著消失\|佔位被替換時，焦點不能跟著消失]] | out-of-order-html-streaming | 糾錯 | 勝 | 佔位裡有目前焦點的元素時，被替換後焦點遺失 |
| [[lines/html/prerendering-custom-elements#hydrate 時沿用伺服器的 shadow root，不要重新渲染\|hydrate 時沿用伺服器的 shadow root，不要重新渲染]] | prerendering-custom-elements | 糾錯 | 勝 | 升級時重新渲染 shadow tree，會丟掉伺服器送來的 DOM 並造成閃爍 |
| [[lines/ui-behaviors/scoped-component-transitions#`match-element` 要搬動既有節點，不能用 `innerHTML` 重建\|`match-element` 要搬動既有節點，不能用 `innerHTML` 重建]] | scoped-component-transitions | 糾錯 | 部分改善 | match-element 依節點身分配對，用 innerHTML 重建的新節點對不上舊節點 |
| [[lines/ui-behaviors/sortable-table#排序時搬 <tr>，不重建 tbody\|排序時搬 <tr>，不重建 tbody]] | sortable-table | 糾錯 | 勝 | 排序時用 `innerHTML` 或重新 render 重建 `<tbody>`，焦點與列內狀態丟失、view tran… |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/播報過量|播報過量]]（3）
- [[groups/生命週期假設錯|生命週期假設錯]]（3）
- [[groups/內容要等JS才成形|內容要等JS才成形]]（2）
- [[groups/載入優先序錯置|載入優先序錯置]]（2）
- [[groups/不可信內容當HTML解析|不可信內容當HTML解析]]（1）
- [[groups/主執行緒被重活卡住|主執行緒被重活卡住]]（1）
- [[groups/優化用過頭反傷|優化用過頭反傷]]（1）
- [[groups/只改外觀沒改語意或焦點|只改外觀沒改語意或焦點]]（1）
- [[groups/得送雲端或載大型函式庫|得送雲端或載大型函式庫]]（1）
- [[groups/快取策略錯置|快取策略錯置]]（1）
- [[groups/手寫焦點管理|手寫焦點管理]]（1）
- [[groups/播報時機或可靠度出錯|播報時機或可靠度出錯]]（1）

← [[groups/對手組總覽|對手組總覽]]
