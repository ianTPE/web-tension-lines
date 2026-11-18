---
group: 內容要等JS才成形
group_en: Content takes shape only after JS runs
lines: 7
guides: 7
tags: [對手組]
---

# 內容要等JS才成形

7 條線，出自 7 份指南。

- 類型：新能力 5、糾錯 2
- 戰報：勝 2、部分改善 4、僵持 1
- 退路：不需要 2、保住主要行為 4、失去主要好處 1

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/performance/flicker-free-client-side-ab-testing#用 blocking="render" 讓實驗腳本在第一次繪製前跑完，取代整頁隱藏的防閃爍片段\|用 blocking="render" 讓實驗腳本在第一次繪製前跑完，取代整頁隱藏的防閃爍片段]] | flicker-free-client-side-ab-testing | 新能力 | 僵持 | 實驗腳本後改 DOM，先看到原版再閃成變體；防閃爍片段整頁 opacity: 0，犧牲漸進渲染、讓人誤點看不見的內容 |
| [[lines/performance/out-of-order-html-streaming#用 `streamHTML()` 把 fetch 回應直接串流進 DOM，不等整包 JSON\|用 `streamHTML()` 把 fetch 回應直接串流進 DOM，不等整包 JSON]] | out-of-order-html-streaming | 新能力 | 部分改善 | 指南只說可取代等整包 JSON 回來再手動建 DOM，沒說那樣做在哪個時刻出問題 |
| [[lines/ui-atoms/pull-to-reveal#用 `scroll-initial-target` 讓搜尋列一載入就藏在上方\|用 `scroll-initial-target` 讓搜尋列一載入就藏在上方]] | pull-to-reveal | 新能力 | 部分改善 | 指南只說 scrollIntoView() 與網址片段有限制、不好做，沒說在哪個時刻出問題 |
| [[lines/ui-behaviors/scroll-target-on-load#用 `scroll-initial-target: nearest` 讓清單一開就停在指定項目\|用 `scroll-initial-target: nearest` 讓清單一開就停在指定項目]] | scroll-target-on-load | 新能力 | 部分改善 | 指南只說 scrollIntoView() 與網址片段有限制、不好做，沒說在哪個時刻出問題 |
| [[lines/ui-behaviors/swipe-to-reveal#左側面板用 `scroll-initial-target` 讓列一開始停在內容欄\|左側面板用 `scroll-initial-target` 讓列一開始停在內容欄]] | swipe-to-reveal | 新能力 | 部分改善 | 不支援的瀏覽器從捲動位置 0 開始，左側面板一開始就露在外面 |
| [[lines/ui-components/dark-mode-toggle#儲存的配色用緊接在 `<meta>` 後面的同步內嵌腳本套用\|儲存的配色用緊接在 `<meta>` 後面的同步內嵌腳本套用]] | dark-mode-toggle | 糾錯 | 勝 | 晚一點才套用儲存的偏好，先閃一下錯的配色 |
| [[lines/html/prerendering-custom-elements#用 Declarative Shadow DOM 從伺服器送出 shadow tree，擋掉等 JS 才有樣式的閃爍\|用 Declarative Shadow DOM 從伺服器送出 shadow tree，擋掉等 JS 才有樣式的閃爍]] | prerendering-custom-elements | 糾錯 | 勝 | shadow tree 靠腳本建立時，元件在 JS 執行前沒有結構也沒有樣式，出現未樣式化內容的閃爍（FOUC）；樣式若… |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/只改外觀沒改語意或焦點|只改外觀沒改語意或焦點]]（2）
- [[groups/只能 hover 才看得到|只能 hover 才看得到]]（2）
- [[groups/版面意外溢出或位移|版面意外溢出或位移]]（2）
- [[groups/重建DOM丟狀態|重建DOM丟狀態]]（2）
- [[groups/不認得的語法讓整條規則失效|不認得的語法讓整條規則失效]]（1）
- [[groups/主題配色對不上|主題配色對不上]]（1）
- [[groups/優化用過頭反傷|優化用過頭反傷]]（1）
- [[groups/原生捲動手勢不合用途|原生捲動手勢不合用途]]（1）
- [[groups/層疊覆蓋不符意圖|層疊覆蓋不符意圖]]（1）
- [[groups/忽略使用者設定|忽略使用者設定]]（1）
- [[groups/播報時機或可靠度出錯|播報時機或可靠度出錯]]（1）
- [[groups/播報過量|播報過量]]（1）

← [[groups/對手組總覽|對手組總覽]]
