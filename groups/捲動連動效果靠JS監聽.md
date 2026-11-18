---
group: 捲動連動效果靠JS監聽
group_en: Scroll-linked effects rely on JS listeners
lines: 15
guides: 15
tags: [對手組]
---

# 捲動連動效果靠JS監聽

15 條線，出自 15 份指南。

- 類型：新能力 15
- 戰報：勝 1、部分改善 13、僵持 1
- 退路：不需要 1、保住主要行為 10、失去主要好處 4

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/ui-atoms/carousel-slide-effects#用 `view()` 時間軸讓投影片隨捲動位置縮放、淡出\|用 `view()` 時間軸讓投影片隨捲動位置縮放、淡出]] | carousel-slide-effects | 新能力 | 部分改善 | 指南只說原生實作比 scroll 監聽加 Web Animations 的退路更有效率，沒說舊做法在哪個時刻出問題 |
| [[lines/ui-behaviors/carousel-snap-highlights#用 `scroll-state(snapped)` 查詢標亮吸附到位的項目\|用 `scroll-state(snapped)` 查詢標亮吸附到位的項目]] | carousel-snap-highlights | 新能力 | 僵持 | 指南只說不必依賴 IntersectionObserver 或 scroll 監聽器，沒說那些做法在哪個時刻出問題 |
| [[lines/user-experience/content-first-noise-reduction#用 `scroll-state(scrolled)` 在往下捲時藏起頂端列，往上捲立刻回來\|用 `scroll-state(scrolled)` 在往下捲時藏起頂端列，往上捲立刻回來]] | content-first-noise-reduction | 新能力 | 部分改善 | 指南只說頂端列在閱讀時應讓開且不需腳本，沒說常駐列或腳本做法在哪個時刻出錯 |
| [[lines/ui-behaviors/motion#非必要的捲動連動效果用捲動驅動動畫\|非必要的捲動連動效果用捲動驅動動畫]] | motion | 新能力 | 勝 | 總覽指南只說用它取代 JS 監聽器，沒說監聽器在哪個時刻出問題 |
| [[lines/ui-behaviors/parallax-scroll-effects#用 `view-timeline` 加 `sibling-index()` 做多層視差\|用 `view-timeline` 加 `sibling-index()` 做多層視差]] | parallax-scroll-effects | 新能力 | 部分改善 | 指南只說原生實作比 scroll 監聽或 IntersectionObserver 退路更有效率，沒說退路在哪個時刻出問… |
| [[lines/ui-behaviors/scroll-entry-exit-effects#用 `view()` 加 `animation-range: entry, exit` 做進場與離場效果\|用 `view()` 加 `animation-range: entry, exit` 做進場與離場效果]] | scroll-entry-exit-effects | 新能力 | 部分改善 | 指南只說原生實作比 IntersectionObserver 退路效能好，沒說舊做法在哪個時刻出問題 |
| [[lines/ui-atoms/scroll-position-aware-elements#用 `scroll-state(scrollable: top)` 只在往下捲之後顯示「回到頂端」\|用 `scroll-state(scrollable: top)` 只在往下捲之後顯示「回到頂端」]] | scroll-position-aware-elements | 新能力 | 部分改善 | 指南只說不必依賴 JS 的 scroll 監聽器或 observer，沒說那些做法在哪個時刻出問題 |
| [[lines/ui-atoms/scroll-progress-indicator#用 `scroll()` 時間軸做閱讀進度條\|用 `scroll()` 時間軸做閱讀進度條]] | scroll-progress-indicator | 新能力 | 部分改善 | 指南只說原生實作比 scroll 監聽器的退路更有效率，沒說舊做法在哪個時刻出問題 |
| [[lines/ui-behaviors/scroll-snap-state-sync#用 `scrollsnapchange` 在捲動停到新段落時同步目錄高亮\|用 `scrollsnapchange` 在捲動停到新段落時同步目錄高亮]] | scroll-snap-state-sync | 新能力 | 部分改善 | 指南只說以前要 scroll 監聽、手算偏移與 IntersectionObserver，沒說這些做法在哪個時刻出錯 |
| [[lines/ui-atoms/scrollability-affordance-hints#用 scroll-state 查詢與捲動驅動的遮罩提示「還有內容」\|用 scroll-state 查詢與捲動驅動的遮罩提示「還有內容」]] | scrollability-affordance-hints | 新能力 | 部分改善 | 指南只說兩種提示都不需要 scroll 監聽器與額外元素，沒說那些做法在哪個時刻出問題 |
| [[lines/ui-components/scrollspy#用 `scroll-target-group` 與 `:target-current` 讓目錄自己標出目前章節\|用 `scroll-target-group` 與 `:target-current` 讓目錄自己標出目前章節]] | scrollspy | 新能力 | 部分改善 | 指南只說傳統做法需要 JS 與 IntersectionObserver，沒說那種做法在哪個時刻出錯 |
| [[lines/ui-behaviors/scrollytelling#用具名 `view-timeline` 加 `timeline-scope`，讓一組段落驅動另一組元素的動畫\|用具名 `view-timeline` 加 `timeline-scope`，讓一組段落驅動另一組元素的動畫]] | scrollytelling | 新能力 | 部分改善 | 指南只說可以不靠 JavaScript、動畫跟著捲動位置走，沒說舊做法在哪個時刻出問題 |
| [[lines/ui-atoms/shrinking-header-on-scroll#用 `scroll(block root)` 加 `animation-range` 讓標頭隨捲動縮小\|用 `scroll(block root)` 加 `animation-range` 讓標頭隨捲動縮小]] | shrinking-header-on-scroll | 新能力 | 部分改善 | 指南只說原生實作比 scroll 監聽器的退路更有效率，沒說舊做法在哪個時刻出問題 |
| [[lines/ui-components/stack-drill-down#視差、變暗與陰影用 `view(inline)` 時間軸跟著手指走，不用 `scroll` 監聽\|視差、變暗與陰影用 `view(inline)` 時間軸跟著手指走，不用 `scroll` 監聽]] | stack-drill-down | 新能力 | 部分改善 | JS scroll 監聽跑在主執行緒，手勢中明顯掉幀 |
| [[lines/ui-atoms/state-aware-sticky-headers#用 `scroll-state(stuck: top)` 讓 sticky 標頭黏住時換樣式\|用 `scroll-state(stuck: top)` 讓 sticky 標頭黏住時換樣式]] | state-aware-sticky-headers | 新能力 | 部分改善 | 傳統做法用 JS scroll 監聽器，指南只說可能造成效能問題，沒指出具體現象 |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/隱藏或停用把人擋在外面|隱藏或停用把人擋在外面]]（8）
- [[groups/簡寫或屬性連動重設|簡寫或屬性連動重設]]（7）
- [[groups/焦點或狀態指示消失|焦點或狀態指示消失]]（6）
- [[groups/功能偵測不可靠|功能偵測不可靠]]（3）
- [[groups/互動中畫面抖動|互動中畫面抖動]]（2）
- [[groups/尺寸動畫只能跳變|尺寸動畫只能跳變]]（2）
- [[groups/忽略使用者設定|忽略使用者設定]]（2）
- [[groups/沒防護不支援的瀏覽器|沒防護不支援的瀏覽器]]（2）
- [[groups/語意結構失真|語意結構失真]]（2）
- [[groups/不認得的語法讓整條規則失效|不認得的語法讓整條規則失效]]（1）
- [[groups/動作被意外觸發|動作被意外觸發]]（1）
- [[groups/只改外觀沒改語意或焦點|只改外觀沒改語意或焦點]]（1）

← [[groups/對手組總覽|對手組總覽]]
