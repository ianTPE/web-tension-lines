---
guide: select-menu-interaction
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/select-menu-interaction.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 下拉選單的互動後驗證

%% line-start id="mwg:select-menu-interaction" %%
## 用 select:user-invalid 讓必選下拉等互動後才標錯
- 做法：`<select required>` 的第一個選項設 `value=""` 並停用，錯誤框線與訊息用 `select:user-invalid` 觸發，成功用 `:user-valid`
- 對手：必選下拉的預設選項是空值時，標準驗證一載入就把欄位標成無效，製造視覺雜訊（引用："standard validation flags the field as invalid immediately if the default option has an empty value. This can create visual noise."）
- 退路：不需要——`:user-invalid` 已 Widely，不必退路
- 解鎖：以前必選下拉一載入就被標準驗證標成無效；現在能用 `:user-invalid` 在使用者動過又沒選、或送出時才標錯

經過：「選擇國家」這類必選下拉，空的預設選項讓它從一開始就是 `:invalid`，表單還沒填就一片紅。改用 `:user-invalid` 後，錯誤只在使用者動過又沒選、或按送出時出現。部分瀏覽器把「打開又關上」也算互動，行動裝置上的 blur 時機也不同，要實機測。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 4 條未拆（與既有線同一個對手，指南文字逐字相同）：`aria-invalid` 起始設 `"false"`（同 `mwg:style-parent-with-has:2`）；錯誤訊息只在無效時掛進 `aria-describedby`（同 `mwg:required-field-feedback:3`）；錯誤改由全頁一個 polite live region 播報（同 `mwg:accessible-error-announcement:3`）；fallback CSS 用 `:is()` 包住 `:user-invalid`（同 `mwg:validate-input-after-interaction:5`）。
