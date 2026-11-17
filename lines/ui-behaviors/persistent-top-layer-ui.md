---
guide: persistent-top-layer-ui
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/persistent-top-layer-ui.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 持續開著的頂層介面

%% line-start id="mwg:persistent-top-layer-ui" %%
## 用 `moveBefore()` 搬動開著的對話框、popover、全螢幕元素而不關閉
- 做法：`newParent.moveBefore(dialogElement, null)` 搬動開啟中的 `<dialog>`、popover 或全螢幕元素；不支援時退回 `insertBefore()`，事先記下是否開著，搬完再 `showModal()`／`showPopover()`
- 對手：傳統搬法隱含先移除再插入，開著的模態、popover 與全螢幕元素會突然關閉（引用："This removal resets the state, causing open modals, popovers, and fullscreen elements to close abruptly."）
- 退路：失去主要好處——Safari 退回 insertBefore() 會先關閉頂層介面，對話框與 popover 須手動重開且全螢幕無法恢復
- 解鎖：不用中斷或關閉開著的對話框、popover 或全螢幕元素，就能原子搬動它們在 DOM 中的父層位置

經過：框架重新安排版面時把開著的對話框換了個父層，使用者眼前的視窗就消失了。原子搬移讓頂層狀態跟著元素走。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：moveBefore()：Limited availability，Supported by: Chrome 133, Edge 133, Firefox 144；Unsupported in: Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前開著的頂層元素不能換位置 → 現在全螢幕播放中的影片、開著的對話框可以在版面重組（側欄收合、分頁拆窗）時被搬到新容器而不關閉。Safari 仍會關閉
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
