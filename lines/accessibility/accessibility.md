---
guide: accessibility
category: accessibility
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/accessibility/accessibility.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 無障礙程式設計準則

%% line-start id="mwg:accessibility" %%
## 每頁只放一個 h1，讓讀屏找得到主標題
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：頁面主標題只用一個 `<h1>`，其餘標題依層級用 `<h2>`–`<h6>`（對話框內的主標題例外）
- 被什麼擋：一頁放了好幾個 `<h1>`，螢幕閱讀器使用者分不出哪一個才是主標題（引用："Having more than one `<h1>` element on a page makes it difficult for screen reader users to identify the actual main heading."）
- 戰報：勝——只留一個 `<h1>` 就沒有歧義；這是純標記規則，指南沒有給支援資料（官方宣稱）

經過：讀屏使用者常靠標題清單或「跳到 h1」快速定位，多個 h1 讓這個入口失效。指南把 `<dialog>`／`role="dialog"` 裡的 h1 列為例外，因為對話框是獨立視窗。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:accessibility:2" %%
## 需要當標題的展開鈕，不要把 heading 塞進 summary
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：標題要兼當展開觸發時，改用 heading 包住 button 的 ARIA 手風琴／disclosure，不用 `<details>`／`<summary>`
- 被什麼擋：部分瀏覽器把 `<summary>` 當按鈕暴露，連帶拿掉子元素的所有角色，裡面的標題就消失了（引用："Some browsers still expose this element as a button, which removes all roles from its children including headings."）
- 戰報：勝——heading 包住 button 時，標題留在無障礙樹裡（官方宣稱）

經過：和 accordion、navbar 指南是同一個對手：`summary` 的角色在各家實作不一致。這份通用準則沒有點名哪個讀屏，只說「some browsers」。
%% line-end %%

### 細節（不索引）
- 對手組：原生元素角色實作不一致
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:accessibility:3" %%
## 清單標記只給真正的清單
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`<ul>`／`<ol>` 只用在重複、連續的項目；段落文字不要包成清單
- 被什麼擋：把分開的段落標成清單，讀屏每次都唸出清單資訊，使用者聽到混亂又多餘的內容（引用："screen readers will announce list information when they encounter lists, therefore leading to a screen reader hearing potentially confusing and redundant information about the related content."）
- 戰報：勝——不是清單就不會被唸成清單（官方宣稱）

經過：清單標記會讓讀屏先報「清單，N 項」，所以用錯地方就變成噪音。同一節還提到核取方塊與單選鈕本身就會報數量，再包一層清單會重複播報。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:accessibility:4" %%
## 視覺版面不要用 table，資料表也要控制複雜度
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：視覺排版用 Grid／Flexbox；真正的資料表用 `<table>`、`<caption>`、`scope`，跨欄列與巢狀表過多時拆成小表
- 被什麼擋：排版用 table 會讓讀屏播報多餘結構並影響閱讀與焦點順序；過複雜表格則讓使用者迷失（引用："Screen readers will announce redundant information about the layout, which may be confusing for screen reader users"）
- 戰報：勝——CSS 負責版面，語意表格只描述資料且容易導覽（官方宣稱）

經過：表格語意會改變讀屏的移動方式，不只是外觀不同。需要合併儲存格、巢狀與展開列時，也要評估是否該拆成幾個較簡單的表。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:5" %%
## 重複導覽前提供 skip link，但不要堆一堆
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：主要重複內容前放一個或少量 skip links，目標用 `tabindex="-1"`；只有一個首頁連結的共用區不必加
- 被什麼擋：沒有 skip link 時鍵盤使用者每頁都要走過重複導覽；太多 skip links 又增加 Tab 停靠點，造成挫折（引用："Multiple unnecessary skip links add to the number of Tab stops to a page, which causes frustration for people who use the keyboard alone for navigation."）
- 戰報：勝——主要重複區可一跳越過，額外 Tab 次數維持少量（官方宣稱）

經過：skip link 的目標要能被程式聚焦，放大鏡才會跟過去。目標前若還有重要內容，也要避免被一併跳掉。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:6" %%
## 用原生 button，不用 div role="button" 自己補行為
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：按鈕用 `<button>`，必填用 `required`，只有 HTML 沒有對應功能時才補 ARIA
- 被什麼擋：`<div role="button">` 只有角色外觀，鍵盤與啟動行為都要自己重建；原生元素已內建（引用："Native HTML elements and attributes already have the correct role and behavior, including keyboard support, built-in by default."）
- 戰報：勝——角色、鍵盤與啟動由平台提供，不必額外 JavaScript（官方宣稱）

經過：ARIA 不會自動帶來行為。`<button>` 已有 role，`required` 已表達 aria-required，不要再寫一份重複屬性。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:7" %%
## 互動 ARIA 角色不要蓋掉結構元素的角色
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：清單中的按鈕寫成 `<li><span role="button">…</span></li>`，不把 `<li>` 本身改成 button
- 被什麼擋：把互動角色放到 `<li>` 等結構元素上會破壞清單語意（引用："Use `<li><span role="button">Button in a list</span></li>`, not `<li role="button">Button in a list</li>`, to avoid breaking the container list semantics."）
- 戰報：勝——外層仍是清單項目，內層才承擔按鈕角色（官方宣稱）

經過：結構與互動要分層表達；tree view 這類本來就定義角色相容的 pattern 是例外。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:8" %%
## 要讓使用者找到停用原因時用 aria-disabled，不用 disabled
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：工具列按鈕或連結需要可聚焦時用 `aria-disabled="true"` 並在 JS 擋下啟動；真的要移出 Tab 才用 `disabled`
- 被什麼擋：`disabled` 會把元素完全移出焦點順序，`tabindex="0"` 也救不回，使用者無法靠近了解它已停用（引用："`disabled` removes the element from the focus order entirely (and `tabindex="0"` won't bring it back)"）
- 戰報：勝——使用者能聚焦並聽到停用狀態，實際啟動仍被阻止（官方宣稱）

經過：aria-disabled 只負責播報，不會自己停用事件；兩種 disabled 的焦點行為要明確選擇。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:9" %%
## 互動元素不要用 role="presentation" 拿掉語意
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：互動元素保留按鈕、連結等原生角色，不用 `role="presentation"`／`none`
- 被什麼擋：元素仍會被讀屏碰到，角色與狀態卻被剝掉，使用者聽到內容卻不知道它能做什麼（引用："The element will still be exposed to assistive technologies and announced by screen readers, but its role and any state information will not be"）
- 戰報：勝——可操作的元素同時保有角色與狀態（官方宣稱）

經過：presentation 不是隱藏元素，只是拿掉語意；可聚焦元素因此更容易讓人困惑。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:10" %%
## label 用 for／id 明確連到控制項
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：`<label for>` 對上控制項 `id`，不只依賴把 input 包在 label 裡
- 被什麼擋：部分語音辨識等輔助技術即使接受包覆寫法，仍要求明確 for／id 關係；明確關聯也提供較大的點擊目標（引用："some assistive technologies, particularly voice recognition software, require the `for`/`id` relationship to be explicitly set"）
- 戰報：勝——標籤可啟動對應控制項，語音與其他輔助技術也能辨識（官方宣稱）

經過：可見文字放附近不代表程式一定知道它屬於誰。原生 naming mechanism 先於 aria-label。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:11" %%
## 不用 title 當控制項名稱
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：名稱用 `<label>`、可見文字或適當 ARIA；`title` 只保留給 iframe 這類標準用途
- 被什麼擋：`title` 只在滑鼠 hover 顯示，任何瀏覽器都無法用鍵盤取得（引用："The value of this attribute is only displayed on mouse hover, and cannot be displayed or otherwise accessed using the keyboard in any browser."）
- 戰報：勝——控制項名稱不依賴滑鼠，鍵盤與讀屏也能取得（官方宣稱）

經過：圖示按鈕只放 title，鍵盤聚焦時不會出現那個提示，可及名稱也不可靠。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:12" %%
## placeholder 只當提示，不當標籤
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：欄位保留可見 `<label>`，placeholder 只放範例或補充提示
- 被什麼擋：輸入一開始 placeholder 就消失，使用者失去欄位用途線索；其低對比也難以辨讀（引用："it disappears as soon as the user enters text into the field, meaning that there is no longer a visual cue as to what the field represents."）
- 戰報：勝——輸入前後都有持續可見、可程式關聯的標籤（官方宣稱）

經過：使用者填到一半回頭看欄位，不能只剩自己輸入的值來猜這格是什麼。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:13" %%
## 同樣是 Edit 的按鈕用可及名稱分出對象
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：用視覺隱藏文字、`aria-label` 或 `aria-labelledby` 補成「Edit name」「Edit address」，並保留可見的 Edit 文字
- 被什麼擋：讀屏只聽到一排「Edit, button」，不知道每個按鈕會修改什麼（引用："screen reader users may only hear "Edit, button"."）
- 戰報：勝——不同效果的控制在名稱上可分，語音也能指定目標（官方宣稱）

經過：周圍版面給視覺使用者的線索，不一定會跟著控制項一起被讀出。不同目的地的同名連結也一樣要補年份等差異。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:14" %%
## 標籤保持精簡，說明與狀態不要重複塞進去
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：額外指示與錯誤用 `aria-describedby`；ARIA 已提供的狀態與元素角色不寫進 label
- 被什麼擋：冗長標籤讓讀屏使用者困惑；重複狀態或角色會唸出「Primary navigation, navigation」這類贅詞（引用："Verbose labels confuse and frustrate people who use screen readers."）
- 戰報：勝——先聽到簡短名稱與控制項類型，再決定是否聽額外描述（官方宣稱）

經過：required、expanded、checked 等狀態交給原生屬性或 ARIA，不要再寫「必填的…按鈕按鈕」。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:15" %%
## 頁面與局部語言變化都用 lang 標正確
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：`<html>` 設主要語言，外語詞句的父元素另設對應 `lang`
- 被什麼擋：lang 與實際內容不符時，讀屏與文字轉語音會唸成無法理解的內容（引用："This causes screen readers and other text-to-speech software to announce the content in a non-understandable manner."）
- 戰報：勝——每段文字都用正確的語音規則播報（官方宣稱）

經過：英文頁面夾一句德文時，整頁語言不必改，但那句德文要標 `lang="de"`。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:16" %%
## 每頁給獨特且前置重點的 title，SPA 換頁也更新
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：`<title>` 寫成「Page Topic | Site Name」，不同頁不重複；SPA 路由或完成狀態改變時同步更新
- 被什麼擋：空白、重複或含糊的 title 讓多分頁無法分辨，必須進頁讀內容才知道自己在哪（引用："In such cases, pages are indistinguishable without reviewing the actual page content itself."）
- 戰報：勝——瀏覽器分頁與讀屏開場都能指出目前頁面用途（官方宣稱）

經過：聯絡表單送出成功後，title 也應從 Contact Us 變成 Thank you，而不是一直停在上一個狀態。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:17" %%
## iframe 不要關捲動，放大後才到得了全部內容
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：保留 iframe 捲動，不用 `scrolling="no"` 或 `overflow: hidden`，並給描述性 `title`
- 被什麼擋：使用者放大頁面或文字後，溢出內容需要捲動才能到達，關掉就被困住（引用："Users who zoom in or enlarge text need to scroll to reach content that overflows."）
- 戰報：勝——放大後仍能捲到 iframe 的全部內容（官方宣稱）

經過：巢入的表單或地圖在小框裡溢出時，不能為了外觀整齊把多出的部分藏死。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:18" %%
## 不用正數 tabindex，焦點順序交給 DOM
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：移除 `tabindex="1"` 等正數；原生控制項不加多餘 `tabindex="0"`，靜態與隱藏內容不放進 Tab
- 被什麼擋：正數 tabindex 會強造一套與頁面預期順序無關的 Tab 路徑（引用："doing so imposes a tab order on the page that bears no resemblance to the intended or expected tab order."）
- 戰報：勝——焦點依 DOM 與原生行為前進，和閱讀順序一致（官方宣稱）

經過：為了讓某顆按鈕先被走到而設正數，結果所有原生控制項都被排到它後面，整頁順序失控。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:19" %%
## 自訂手勢不要用 touch-action: none 鎖死整塊捲動
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只限制手勢真正需要的軸，水平滑動用 `pan-y`、垂直滑動用 `pan-x`；繪圖 canvas 才考慮 `none`
- 被什麼擋：`touch-action: none` 會停用元素上的頁面捲動，使用者在該區域無法正常上下頁（引用："This disables page scrolling through the element."）
- 戰報：勝——自訂手勢運作時，另一軸的原生捲動仍保留（官方宣稱）

經過：橫向卡片滑動不該連整頁垂直捲動都鎖掉。限制範圍愈小，副作用愈少。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:20" %%
## 圖片與 SVG 的替代文字依用途提供或留空
- 誰在做：內容作者與開發者（或寫程式的代理）
- 動作＋對象：有意義圖片寫功能導向 `alt`，非裝飾 SVG 用 `role="img"` 加 `<title>`／`aria-label`；裝飾圖片用 `alt=""`、裝飾 SVG 用 `aria-hidden="true"`
- 被什麼擋：缺少替代文字時讀屏以圖名等內容代替；裝飾圖沒隱藏則會多唸無關內容（引用："Do apply `alt=""` to decorative visuals: This prevents screen readers from announcing them."）
- 戰報：勝——有意義內容被正確描述，純裝飾不再造成噪音（官方宣稱）

經過：搜尋按鈕的放大鏡寫「Search」而不是「Magnifying glass」。分隔線與純裝飾 icon 則不必進入播報。
%% line-end %%

### 細節（不索引）
- 對手組：重複內容干擾輔助技術
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:21" %%
## live region 控制數量與時機，inert 內容不要送播報
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：全頁各用一個 polite／assertive 區域，頻繁更新 debounce、碰撞時稍延遲；對話框或區塊 inert 時先協調播報狀態
- 被什麼擋：太多或高頻 live regions 會變成讀屏 spam；訊息送進 inert DOM 則可能不播，或從使用者到不了的地方播出（引用："queued or debounced messages will be unannounced — or announced from DOM the user can't reach."）
- 戰報：勝——重要更新能被聽到，不重複、不互相覆蓋，也不從失效區域發出（官方宣稱）

經過：Loading 這類過場通常用 progress，而不是反覆播報。assertive 只留給資料遺失、逾時等必須立即打斷的情況。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:accessibility:22" %%
## 模態用原生 dialog.showModal()，自訂覆層才裝 inert 與焦點
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：模態用 `<dialog>` 加 `.showModal()`；不能用時才給外部內容 `inert`、覆層 `role="dialog"` 並移入焦點
- 被什麼擋：（缺）指南只說手寫焦點陷阱、外部隱藏、頂層與遮罩容易出錯，沒指出單一失敗案例（引用："all of which are error prone and require heavy JavaScript event tracking to maintain."）
- 戰報：勝——原生模態讓外部內容不可聚焦、不在無障礙樹，不必再寫 focus trap（官方宣稱）

經過：原生 dialog 不必額外攔 Tab；仍可到瀏覽器 chrome。自訂覆層不能把 overlay 放在被設 inert 的祖先裡。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

另有 7 個糾錯提醒未拆：地標與標題層級的一般原則、可見文字須包含在可及名稱中、焦點框的高對比退路、最小點擊目標、音影片字幕與逐字稿、複雜圖表的長描述、自動與人工測試；這些多為常識性檢查或指南未指出具體後果。
