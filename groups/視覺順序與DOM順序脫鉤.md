---
group: 視覺順序與DOM順序脫鉤
group_en: Visual order drifts from DOM order
lines: 4
guides: 4
tags: [對手組]
---

# 視覺順序與DOM順序脫鉤

4 條線，出自 4 份指南。

- 類型：新能力 1、糾錯 3
- 戰報：勝 3、部分改善 1
- 退路：不需要 3、保住主要行為 1

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/ui-behaviors/drag-and-drop#搬真的 DOM 節點，不用 CSS order 假裝重排\|搬真的 DOM 節點，不用 CSS order 假裝重排]] | drag-and-drop | 新能力 | 部分改善 | 用 CSS `order` 或 `flex-direction: *-reverse` 改變畫面順序，DOM 順序沒變，… |
| [[lines/css/css-layout#不用 order、*-reverse、dense 改變互動內容的視覺順序\|不用 order、*-reverse、dense 改變互動內容的視覺順序]] | css-layout | 糾錯 | 勝 | 這些功能只改視覺順序，DOM 仍驅動 Tab，鍵盤焦點與畫面位置對不上 |
| [[lines/forms/forms#不用 CSS 改變表單的視覺順序\|不用 CSS 改變表單的視覺順序]] | forms | 糾錯 | 勝 | 視覺順序被 CSS 改變後，鍵盤仍按 DOM 順序移動，焦點在畫面上亂跳 |
| [[lines/ui-behaviors/spatial-navigation#依每次按鍵當下的實際幾何選下一個焦點，不靠索引或 DOM 順序\|依每次按鍵當下的實際幾何選下一個焦點，不靠索引或 DOM 順序]] | spatial-navigation | 糾錯 | 勝 | 不對稱或會換行的版面用索引對應會選錯；隱藏元素位於原點的零尺寸矩形變成意外的上、左目標 |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/版面意外溢出或位移|版面意外溢出或位移]]（2）
- [[groups/互動中畫面抖動|互動中畫面抖動]]（1）
- [[groups/封裝邊界切斷關聯|封裝邊界切斷關聯]]（1）
- [[groups/平台慣用操作沒有作用|平台慣用操作沒有作用]]（1）
- [[groups/播報時機或可靠度出錯|播報時機或可靠度出錯]]（1）
- [[groups/播報過量|播報過量]]（1）
- [[groups/敏感資料外露|敏感資料外露]]（1）
- [[groups/浮層遮住說明|浮層遮住說明]]（1）
- [[groups/版面依賴錯的量測|版面依賴錯的量測]]（1）
- [[groups/版面擠壓破壞可讀性|版面擠壓破壞可讀性]]（1）
- [[groups/用錯原生控制項|用錯原生控制項]]（1）
- [[groups/自動填入失效|自動填入失效]]（1）

← [[groups/對手組總覽|對手組總覽]]
