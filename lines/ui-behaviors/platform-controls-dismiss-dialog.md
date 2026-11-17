---
guide: platform-controls-dismiss-dialog
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/platform-controls-dismiss-dialog.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用平台控制關閉對話框

%% line-start id="mwg:platform-controls-dismiss-dialog" %%
## 模態 `<dialog>` 回應返回鍵與返回手勢
- 做法：模態對話框用 `showModal()` 或 `command="show-modal"` 開啟；不寫 `closedby` 時即等同 `closerequest`，要點背景也關閉時才設 `closedby="any"`
- 對手：`<dialog>` 剛推出時只能用 Esc 關閉，行動裝置的返回鍵或返回手勢關不掉；自己實作返回手勢關閉也沒有好方法（引用："it could be dismissed with the <kbd>Esc</kbd> key, but not other platform controls such as a back button/gesture on mobile … There is no good way to implement close requests from mobile back button/gestures"）
- 退路：失去主要好處——Safari 無法回應行動裝置返回鍵與手勢且無可靠退路，僅剩 Esc 與關閉鈕可關閉對話框
- 解鎖：已經用 showModal() 開啟的模態對話框不必額外寫手勢程式，就能回應行動裝置返回鍵與輔助技術關閉手勢

經過：手機使用者習慣按返回關掉彈窗，網頁的對話框以前不吃這套，按下去反而離開整頁。現在關閉請求涵蓋平台的各種關閉方式。
%% line-end %%

### 細節（不索引）
- 對手組：平台慣用操作沒有作用
- 支援狀態：<dialog closedby>：Limited availability，Supported by: Chrome 134, Edge 134, Firefox 141；Unsupported in: Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前網頁彈窗擋不住手機返回鍵 → 現在行動版的篩選面板、圖片檢視、確認框可以像原生 app 一樣按返回就關、不離開頁面。Safari 尚未支援
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
