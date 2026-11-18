---
group: 用JS補樣式狀態
group_en: JS patches in styling state
lines: 6
guides: 6
tags: [對手組]
---

# 用JS補樣式狀態

6 條線，出自 6 份指南。

- 類型：新能力 3、糾錯 3
- 戰報：勝 3、部分改善 3
- 退路：不需要 3、保住主要行為 3

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/ui-behaviors/dynamic-sibling-animations#用 `sibling-index()` 讓清單項目依序錯開進場\|用 `sibling-index()` 讓清單項目依序錯開進場]] | dynamic-sibling-animations | 新能力 | 部分改善 | 指南只描述錯開動畫的效果，沒說逐個 nth-child 或 JS 設延遲在哪個時刻出問題 |
| [[lines/css/dynamic-sibling-styling#用 sibling-index() 與 sibling-count() 讓每個項目自己算樣式\|用 sibling-index() 與 sibling-count() 讓每個項目自己算樣式]] | dynamic-sibling-styling | 新能力 | 部分改善 | 只說過去要寫複雜的 `:nth-child` 迴圈或用 JS 注入行內樣式，沒說那樣做在哪個時刻出錯 |
| [[lines/forms/slider#用 progress() 與 attr() 在 CSS 裡算出滑桿的填色比例\|用 progress() 與 attr() 在 CSS 裡算出滑桿的填色比例]] | slider | 新能力 | 部分改善 | WebKit／Blink 沒有對應「已填部分」的偽元素，要讓軌道已填和未填兩段不同色，只能自己同步數值 |
| [[lines/css/child-state-based-styling#用 :has() 讓容器反應子元素狀態，不用 JS 切 class\|用 :has() 讓容器反應子元素狀態，不用 JS 切 class]] | child-state-based-styling | 糾錯 | 勝 | 只說不再需要 JS 在父元素切換修飾 class，沒說手寫切換在哪個時刻出錯 |
| [[lines/css/content-based-styling#用 :has() 依有沒有某個子元素切換版面\|用 :has() 依有沒有某個子元素切換版面]] | content-based-styling | 糾錯 | 勝 | 只說過去要用 JS 或模板條件注入修飾 class，沒說那樣做在哪個時刻出錯 |
| [[lines/css/style-parent-with-has#用 :has(:user-invalid) 標示含錯誤欄位的整個區塊\|用 :has(:user-invalid) 標示含錯誤欄位的整個區塊]] | style-parent-with-has | 糾錯 | 勝 | 只說過去要靠 JS 在父元素上切換 class，沒說手寫切換在哪個時刻出錯 |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/不認得的語法讓整條規則失效|不認得的語法讓整條規則失效]]（1）
- [[groups/播報時機或可靠度出錯|播報時機或可靠度出錯]]（1）

← [[groups/對手組總覽|對手組總覽]]
