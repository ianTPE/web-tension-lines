---
group: 不可信內容當HTML解析
group_en: Untrusted content parsed as HTML
lines: 5
guides: 4
tags: [對手組]
---

# 不可信內容當HTML解析

5 條線，出自 4 份指南。

- 類型：新能力 2、糾錯 3
- 戰報：勝 2、部分改善 3
- 退路：不需要 2、保住主要行為 2、失去主要好處 1

## 線

| 線 | 指南 | 類型 | 戰報 | 對手 |
|---|---|---|---|---|
| [[lines/security/sanitize-untrusted-html#用原生 `setHTML()` 一步完成解析、清理與插入\|用原生 `setHTML()` 一步完成解析、清理與插入]] | sanitize-untrusted-html | 新能力 | 部分改善 | 使用者產生的 HTML 裡的 script 標籤與 on* 屬性在進入 DOM 時就會執行 |
| [[lines/security/trusted-types#用 Trusted Types 讓危險 sink 只收政策產生的物件\|用 Trusted Types 讓危險 sink 只收政策產生的物件]] | trusted-types | 新能力 | 部分改善 | DOM sink 預設接受原始字串，含不可信來源惡意腳本的字串會被執行 |
| [[lines/built-in-ai/language-model#模型輸出一律用 textContent，不塞進 innerHTML\|模型輸出一律用 textContent，不塞進 innerHTML]] | language-model | 糾錯 | 勝 | 模型輸出可能夾帶注入的標記，直接設 `innerHTML` 會變成 XSS |
| [[lines/security/sanitize-untrusted-html#清理後直接搬節點，不要序列化成字串再塞回 `innerHTML`\|清理後直接搬節點，不要序列化成字串再塞回 `innerHTML`]] | sanitize-untrusted-html | 糾錯 | 部分改善 | 清理後序列化成字串再用 innerHTML 重新解析，可能重新引入突變型 XSS |
| [[lines/security/security#不讓不可信字串進危險 sink，並用 Trusted Types 在執行期把關\|不讓不可信字串進危險 sink，並用 Trusted Types 在執行期把關]] | security | 糾錯 | 勝 | 不可信輸入經 innerHTML、setHTMLUnsafe 寫進 DOM 形成 DOM XSS；pass-throug… |

## 常一起出現的組

同一份指南裡也出現的其他對手組（括號內是共同的指南數）。

- [[groups/合法連線被安全規則擋下|合法連線被安全規則擋下]]（2）
- [[groups/敏感資料外露|敏感資料外露]]（2）
- [[groups/防線形同虛設|防線形同虛設]]（2）
- [[groups/主執行緒被重活卡住|主執行緒被重活卡住]]（1）
- [[groups/優化用過頭反傷|優化用過頭反傷]]（1）
- [[groups/參數或格式用錯就丟例外|參數或格式用錯就丟例外]]（1）
- [[groups/得送雲端或載大型函式庫|得送雲端或載大型函式庫]]（1）
- [[groups/快取策略錯置|快取策略錯置]]（1）
- [[groups/手寫焦點管理|手寫焦點管理]]（1）
- [[groups/播報過量|播報過量]]（1）
- [[groups/新屬性的隱藏前提|新屬性的隱藏前提]]（1）
- [[groups/權限請求不看時機|權限請求不看時機]]（1）

← [[groups/對手組總覽|對手組總覽]]
