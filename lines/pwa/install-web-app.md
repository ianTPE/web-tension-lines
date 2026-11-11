---
guide: install-web-app
category: pwa
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/pwa/install-web-app.md
first_seen: 2026-11-11（v1.0.0）
license: CC-BY-4.0（上游指南）
---

# 安裝網頁應用

%% line-start id="mwg:install-web-app" %%
## 用 <install> / navigator.install() 取代只能裝自己的 beforeinstallprompt
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 HTML `<install>` 元素或 `navigator.install()` 在頁面內提供明確的安裝入口，而且可以安裝別的 app（例如 app 目錄）
- 被什麼擋：現有的 `beforeinstallprompt` 只能安裝目前這個 app，無法替目錄裡的其他 app 提供安裝（引用："Unlike `navigator.install()`, this event cannot install a different app."）
- 戰報：僵持——兩個新入口都還沒有任何主要瀏覽器支援，實務上仍得靠 `beforeinstallprompt` 或瀏覽器自己的安裝 UI（官方宣稱）

經過：指南把安裝流程收斂到瀏覽器控制的同意介面，網站不能偷偷安裝。新入口讓 app 目錄也能一鍵安裝別的 app，但原文直說 "<install> is not natively supported by any major browser yet"，`navigator.install()` 也一樣。在支援出現前，替代方案只有舊事件，而舊事件正好做不到跨 app 安裝。
%% line-end %%

### 細節（不索引）
- 對手組：安裝入口受限
- 支援狀態：`<install>`：not natively supported by any major browser yet；`navigator.install()`：同；Web app manifest：Limited（Firefox 不支援）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：一個頁面可以替「別的」web app 提供安裝按鈕，自建 app 目錄或工具集合頁就能一鍵安裝每個小工具。目前沒有瀏覽器支援，只能先追蹤
- 變更紀錄：2026-11-11（v1.0.0）首次拆出
