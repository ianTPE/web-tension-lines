---
guide: brand-consistent-forms
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/brand-consistent-forms.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 品牌一致的表單控制項

%% line-start id="mwg:brand-consistent-forms" %%
## 用 accent-color 一行換品牌色，不必重做勾選框與單選鈕
- 做法：在 `body` 或表單容器設 `accent-color: var(--brand-color)`，讓 checkbox、radio、range、progress 套上品牌色；搭配 `color-scheme` 支援深色模式
- 對手：從零自製控制項費時，而且很容易出現可及性問題或漏掉狀態，例如勾選框的 indeterminate 狀態（引用："Building custom controls is time-consuming and can easily lead to accessibility issues or missing states (like the indeterminate state for checkboxes)."）
- 退路：失去主要好處——退回視覺隱藏原生 input 再自繪勾選框與滑桿，失去一行換色就保住原生狀態的好處
- 解鎖：以前原生勾選框只有瀏覽器的顏色，要品牌色就得整個自製；現在一行 `accent-color` 就能讓原生控制項換上品牌色

經過：設計稿上的勾選框是品牌紫，原生控制項只有瀏覽器預設的藍，以往只能把原生 input 藏起來、用偽元素重畫，順手就漏了 indeterminate 或焦點樣式。`accent-color` 讓原生控制項自己換色。指南仍要求為不支援的瀏覽器保留重畫的那一套。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：accent-color：Limited（指南原句："Browser support for accent-color: Limited availability. Supported by: Chrome 93 (Aug 2021), Edge 93 (Sep 2021), Firefox 92 (Sep 2021), and Safari 26.2 (Dec 2025)."——標 Limited 卻列出四大瀏覽器，待人工確認，暫照指南）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前品牌色的勾選框、滑桿、進度條等於重寫一套控制項 → 問卷、設定頁可以直接用原生控制項，一行 CSS 換成品牌色，indeterminate、鍵盤操作、焦點都由瀏覽器處理。只作用於 checkbox、radio、range、progress
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:brand-consistent-forms:2" %%
## accent-color 自己挑對比夠的顏色，不要信任瀏覽器自動反色
- 做法：選與背景至少 3:1 對比的品牌色，並在深色模式改用較亮的色值，搭配 `color-scheme: light dark`
- 對手：Safari（WebKit bug 244233）與 Android Chrome（Chromium bug 343503163）可能沒有把勾號反色，顏色與背景對比不足時控制項變得看不見或難以辨識（引用："can fail to invert checkmark colors, leading to invisible or hard-to-see controls when using colors that lack sufficient contrast against the background"）
- 退路：保住主要行為——不支援時退回瀏覽器預設外觀，控制項照常看得見，只是沒有品牌色
- 解鎖：（缺）

經過：淺色模式下選了淡黃當品牌色，瀏覽器理論上會自動挑對比色畫勾號，但有些實作沒做到，勾選與否幾乎看不出來。指南的做法是不要賭瀏覽器，一開始就挑對比夠的顏色。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：accent-color：Limited（同上，指南標示存疑）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

未拆：「不要以為 `accent-color` 對所有表單元素都有效，目前只作用於 checkbox、radio、range、progress」是適用範圍說明，不是對手。
