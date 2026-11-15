#!/usr/bin/env python3
"""
test_tools.py — tw-translate 自我測試（離線、只用標準函式庫）。

    python scripts/test_tools.py        # 全過 exit 0

涵蓋：po.py validate 當關卡（有錯回 1）、extract、lookup 單字邊界、search、
兩份 CSV 的出處／可信度欄、待補清單、SKILL.md 的數字（check_numbers）、連結、速查表、
TAIWAN_VS_CHINA.md 的依據、evals 題目的答案真的在詞彙表裡。
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
SKILL_MD = ROOT / "SKILL.md"
TRUST = {"實測", "官方文件", "推論", "站內風格"}
DATE = re.compile(r"^20\d\d-\d\d-\d\d$")


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)


def rows(name: str) -> list[dict]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def wp_current() -> set[tuple[str, str]]:
    g = rows("glossary.csv")
    latest = max(r["retrieved_on"] for r in g)
    return {(r["en"].strip().lower(), r["zh-tw"].strip()) for r in g if r["retrieved_on"] == latest}


def write_po(tmp: str, name: str, body: str) -> str:
    p = Path(tmp) / name
    p.write_text('msgid ""\nmsgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"\n\n' + body, encoding="utf-8")
    return str(p)


class TestPoValidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_error_returns_1(self):
        po = write_po(self.tmp, "bad.po", 'msgid "Save %s"\nmsgstr "儲存"\n\nmsgid "Delete"\nmsgstr ""\n')
        r = run("scripts/po.py", "validate", po)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("錯誤 2", r.stdout)

    def test_error_returns_1_json(self):
        po = write_po(self.tmp, "bad.po", 'msgid "Save %s"\nmsgstr "儲存"\n')
        r = run("scripts/po.py", "validate", po, "--format", "json")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["counts"]["error"], 1)

    def test_clean_returns_0(self):
        po = write_po(self.tmp, "ok.po", 'msgid "Save %s"\nmsgstr "儲存 %s"\n')
        r = run("scripts/po.py", "validate", po)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_warning_only_returns_0(self):
        po = write_po(self.tmp, "warn.po", 'msgid "Plugin"\nmsgstr "插件"\n')
        r = run("scripts/po.py", "validate", po, "--format", "json")
        self.assertEqual(r.returncode, 0)
        codes = [i["code"] for i in json.loads(r.stdout)["issues"]]
        self.assertIn("china-term", codes)

    def test_missing_file_returns_1(self):
        self.assertEqual(run("scripts/po.py", "validate", str(Path(self.tmp) / "nope.po")).returncode, 1)


class TestPoExtract(unittest.TestCase):
    def test_extract_untranslated(self):
        tmp = tempfile.mkdtemp()
        po = write_po(tmp, "x.pot", 'msgid "Save"\nmsgstr ""\n\nmsgid "Delete"\nmsgstr "刪除"\n')
        r = run("scripts/po.py", "extract", po, "--format", "json")
        self.assertEqual(r.returncode, 0)
        ids = [i["msgid"] for i in json.loads(r.stdout)["items"]]
        self.assertEqual(ids, ["Save"])


class TestLookup(unittest.TestCase):
    def test_word_boundary(self):
        r = run("scripts/lookup.py", "Enable debug mode", "--format", "json")
        en = {t["en"].lower() for t in json.loads(r.stdout)["terms"]}
        self.assertIn("debug", en)
        self.assertNotIn("bug", en)

    def test_phrase_hit(self):
        r = run("scripts/lookup.py", "Set a featured image", "--format", "json")
        hits = {(t["en"].lower(), t["zh"]) for t in json.loads(r.stdout)["terms"]}
        self.assertIn(("featured image", "精選圖片"), hits)


class TestSearch(unittest.TestCase):
    def top(self, *args):
        r = run("scripts/search.py", *args, "--format", "json")
        self.assertEqual(r.returncode, 0, r.stdout)
        return json.loads(r.stdout) if r.stdout.lstrip().startswith("[") else []

    def test_block_pattern(self):
        self.assertEqual(self.top("block pattern")[0]["zh"], "區塊版面配置")

    def test_sidebar_zixunlan(self):
        self.assertEqual(self.top("sidebar", "--source", "wp", "--domain", "en")[0]["zh"], "資訊欄")

    def test_fanhuaji(self):
        self.assertEqual(self.top("設置", "--source", "fanhuaji")[0]["zh"], "設定")

    def test_absent_term_not_matched_exactly(self):
        hits = self.top("dark pattern", "--source", "wp", "--domain", "en")
        self.assertFalse(any(h["en"].lower() == "dark pattern" for h in hits))


class TestData(unittest.TestCase):
    def test_glossary_provenance(self):
        g = rows("glossary.csv")
        self.assertEqual(list(g[0])[:4], ["en", "zh-tw", "pos", "description"])
        for r in g:
            self.assertTrue(r["doc_url"].startswith("https://"), r)
            self.assertRegex(r["retrieved_on"], DATE)
            self.assertIn(r["trust"], TRUST, r)

    def test_glossary_current_rows_from_glotpress(self):
        g = rows("glossary.csv")
        latest = max(r["retrieved_on"] for r in g)
        for r in g:
            if r["retrieved_on"] == latest:
                self.assertIn("translate.wordpress.org", r["doc_url"])

    def test_terms_provenance(self):
        for r in rows("taiwan-terms.csv"):
            self.assertIn(r["trust"], TRUST, r)
            self.assertRegex(r["measured_on"][:10], DATE)
            if r["trust"] == "實測":
                self.assertEqual(r["fanhuaji_out"], r["tw"], r)
            if r["trust"] == "官方文件":
                self.assertTrue(r["doc_url"].startswith("https://"), r)

    def test_pending(self):
        p = rows("pending.csv")
        self.assertEqual(list(p[0]), ["date", "question", "why_not_found", "asked_by", "status"])
        for r in p:
            self.assertRegex(r["date"], DATE)
            self.assertTrue(r["question"] and r["why_not_found"] and r["asked_by"], r)


class TestSkillMd(unittest.TestCase):
    text = SKILL_MD.read_text(encoding="utf-8")

    def test_numbers(self):
        r = run("scripts/check_numbers.py")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_check_numbers_catches_drift(self):
        sys.path.insert(0, str(HERE))
        import check_numbers
        tmp = Path(tempfile.mkdtemp()) / "SKILL.md"
        tmp.write_text(self.text.replace("135 列", "136 列"), encoding="utf-8")
        problems, _ = check_numbers.check(tmp)
        self.assertTrue(any("terms" in p for p in problems), problems)
        tmp.write_text(self.text + "\n共 42 個\n", encoding="utf-8")
        problems, _ = check_numbers.check(tmp)
        self.assertTrue(any("42" in p for p in problems), problems)

    def test_headings(self):
        heads = re.findall(r"^## (.+)$", self.text, re.M)
        self.assertEqual(heads, ["資料出處", "用法", "路由", "使用", "驗證", "維護"])

    def test_iron_rule_first_in_routing(self):
        routing = self.text.split("## 路由", 1)[1].lstrip()
        self.assertTrue(routing.startswith("> **鐵則：先查再答"), routing[:40])
        self.assertIn("data/pending.csv", routing.split("\n\n", 1)[0])

    def test_local_paths_exist(self):
        for p in set(re.findall(r"`((?:data|references|scripts|tools|evals)/[\w./-]+\.(?:csv|md|py|json))", self.text)):
            self.assertTrue((ROOT / p).exists(), p)
        for p in ("EXAMPLES.md",):
            self.assertTrue((ROOT / p).exists(), p)

    def test_quick_table_in_glossary(self):
        sec = self.text.split("### 常用詞速查", 1)[1].split("\n\n", 2)[1]
        wp = wp_current()
        pairs = []
        for line in sec.splitlines()[2:]:
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            pairs += [(c[0], c[1]), (c[2], c[3])]
        self.assertGreaterEqual(len(pairs), 10)
        for en, zh in pairs:
            self.assertIn((en.lower(), zh), wp, f"{en} → {zh} 不在現行詞彙表")


class TestTaiwanVsChina(unittest.TestCase):
    def test_rows_have_basis(self):
        text = (ROOT / "references" / "TAIWAN_VS_CHINA.md").read_text(encoding="utf-8")
        terms = {r["cn"]: r for r in rows("taiwan-terms.csv")}
        wp = wp_current()
        n = 0
        for line in text.splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) != 4 or c[0] in ("中國大陸",) or set(c[0]) <= set("-"):
                continue
            cn, tw, en, basis = c
            n += 1
            self.assertIn(basis, TRUST, line)
            if basis == "官方文件" and not (cn in terms and terms[cn]["tw"] == tw):
                self.assertIn((en.lower(), tw), wp, line)
            if cn in terms and terms[cn]["tw"] == tw:
                self.assertEqual(basis, terms[cn]["trust"], line)
        self.assertGreater(n, 30)


class TestEvals(unittest.TestCase):
    def test_cases_sourced(self):
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))["cases"]
        active = [c for c in cases if not c.get("retired")]
        self.assertGreaterEqual(len(active), 10)
        wp = wp_current()
        all_en = {en for en, _ in wp}
        for c in cases:
            if c.get("absent"):
                self.assertNotIn(c["term"].lower(), all_en, c["id"])
                continue
            self.assertIn((c["term"].lower(), c["expect"]), wp, c["id"])
            self.assertTrue(all(any(re.search(p, c["expect"]) for p in g) for g in c["must"]), c["id"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=2)
