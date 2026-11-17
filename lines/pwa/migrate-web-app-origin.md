---
guide: migrate-web-app-origin
category: pwa
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/pwa/migrate-web-app-origin.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 遷移已安裝 web app 的來源

%% line-start id="mwg:migrate-web-app-origin" %%
## 用 manifest 的 `migrate_from`／`migrate_to` 搬家，不再要使用者解除安裝再重裝
- 做法：新站 manifest 宣告 `migrate_from`（可設 `behavior: "force"`），舊站在 `/.well-known/web-app-origin-association` 授權 `allow_migration`，舊站 manifest 可加 `migrate_to` 主動通知；新舊來源必須同站（同 eTLD+1）
- 對手：換來源時得要使用者手動解除安裝舊 app、再安裝新 app，失去工作列捷徑、通知權限等系統整合（引用："This process usually causes the loss of OS-level integration, such as taskbar shortcuts and notification permissions."）
- 退路：失去主要好處——退回舊站提示使用者到新站，失去自動遷移與設定保留
- 解鎖：已安裝 PWA 可在同站的新舊來源間遷移，不必手動解除再重裝

經過：產品換網域，已安裝的使用者得自己移除再重裝，捷徑沒了、圖示沒了。新舊兩端互相確認後，瀏覽器幫忙換殼；只是 localStorage、IndexedDB 與權限仍綁在舊來源，要另外搬。
%% line-end %%

### 細節（不索引）
- 對手組：遷移時遺失使用者狀態
- 支援狀態：Web app origin migration：Limited availability。Supported by: Chrome 149, Edge 149。Unsupported in: Firefox and Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：個人工具站可以從 `tools.example.com/foo` 拆成獨立子網域、或把幾個小 PWA 合併，已安裝的使用者點一下「更新」就跟過去，不必寫公告教人重裝。目前僅 Chromium，資料仍要自己搬
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
