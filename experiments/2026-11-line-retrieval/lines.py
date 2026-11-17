"""讀出所有線與它們的各種「抽法」表示，供檢索實驗使用。"""
import csv, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
UP = ROOT / ".cache/upstream/skills/modern-web-guidance/guides"
LINE_RE = re.compile(r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%', re.S)
SLOT_RE = re.compile(r"^- (誰在做|動作＋對象|被什麼擋|戰報)：(.+)$", re.M)
QUOTE_RE = re.compile(r'（?引用：[「"](.+?)[」"]）?\s*$')


def strip_quote(s):
    return QUOTE_RE.sub("", s).strip()


def load():
    ledger = {r["line_id"]: r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8", newline=""))}
    out = []
    for p in sorted((ROOT / "lines").glob("*/*.md")):
        text = p.read_text(encoding="utf-8")
        for lid, body in LINE_RE.findall(text):
            if lid not in ledger or ledger[lid]["狀態"] != "有效":
                continue
            title = re.search(r"^## (.+)$", body, re.M).group(1).strip()
            slots = dict(SLOT_RE.findall(body))
            story = re.search(r"^經過：(.+)$", body, re.M)
            blocker = slots.get("被什麼擋", "")
            q = re.search(r'引用：[「"](.+?)[」"]）?\s*$', blocker)
            out.append(dict(
                id=lid, guide=f"{p.parent.name}/{p.stem}", title=title,
                action=slots.get("動作＋對象", ""), blocker=strip_quote(blocker),
                quote=q.group(1) if q else "", outcome=slots.get("戰報", ""),
                story=story.group(1).strip() if story else "",
                group=ledger[lid]["對手組"], kind=ledger[lid]["類型"],
                unlock=ledger[lid]["解鎖"], block=body.strip(),
            ))
    return out


def guide_text(guide):
    return (UP / f"{guide}.md").read_text(encoding="utf-8")


if __name__ == "__main__":
    L = load()
    import collections
    print(len(L), "lines,", len({l["guide"] for l in L}), "guides,", len({l["group"] for l in L}), "groups")
    print("with quote:", sum(bool(l["quote"]) for l in L))
    print(collections.Counter(len(l["block"]) // 200 * 200 for l in L).most_common(6))
