---
guide: visually-stable-mixed-fonts
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/visually-stable-mixed-fonts.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 視覺穩定的混排字型

%% line-start id="mwg:visually-stable-mixed-fonts" %%
## 混排字型時用 `font-size-adjust` 以 x 高度對齊大小，不再只看 `font-size`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在混用字型的容器（行內程式碼、換主題字型的區塊）設 `font-size-adjust: from-font`，子元素換字型時自動對齊外層字型的 x 高度；要對齊的字型不是祖先時（例如另一套主題），直接寫首選字型的比例數值，如 `font-size-adjust: 0.51`
- 被什麼擋：不同字型的 x 高度不同，同樣的 `font-size` 下一種看起來明顯比另一種小或大，可讀性變差並造成版面位移（引用："differences in "x-height" (the height of lowercase letters) can make one font appear much smaller or larger than the other font. This can lead to poor legibility and layout shifts."）
- 戰報：部分改善——各字型的小寫字看起來一樣大；font-size-adjust 為 Newly，不支援時以原本的 `font-size` 顯示，要用 `@supports not (font-size-adjust: from-font)` 補上手調的 `font-size`／`line-height`，或挑 x 高度相近的字型（官方宣稱）

經過：段落裡夾一段 `<code>`，等寬字型的小寫字明顯比內文矮一截，看起來像註腳。改成依 x 高度對齊後，程式碼和內文並排也一樣大。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：font-size-adjust：Baseline Newly available（2024-07-25 起），Supported by: Chrome 127, Edge 127, Firefox 118, Safari 17
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前混排字型只能挑 x 高度相近的組合或逐個手調字級 → 現在技術文件的行內程式碼、可切換字型的電子書閱讀器、多主題的部落格可以自由搭配字型，切換主題字型時版面也不跳
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
