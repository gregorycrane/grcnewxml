#!/usr/bin/env python3
"""Compile Bergk/Schroeder's Pindar volume into CTS work-level TEI.

The retained volume transcription remains the diplomatic source.  The four
complete epinician collections are cited by poem and line; the lost works are
compiled separately and cited by Schroeder's printed fragment numbers.  Page
numbers survive only in ``pb`` provenance markers.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


TEI = "http://www.tei-c.org/ns/1.0"
CTS = "http://chs.harvard.edu/xmlns/cts"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"tei": TEI}
ET.register_namespace("", TEI)
ET.register_namespace("ti", CTS)

VERSION = "schroeder1900-grc1"
REVISION_DATE = "2026-11-05"

# Start pages are explicit because several short odes omit the metrical
# preface used to mark the surrounding ode openings.
WORKS = {
    "tlg001": {
        "title": "Olympian Odes", "greek": "Ὀλυμπιονῖκαι",
        "starts": [81, 90, 101, 106, 109, 112, 122, 130, 137, 146, 155, 158, 160, 170, 173],
    },
    "tlg002": {
        "title": "Pythian Odes", "greek": "Πυθιονῖκαι",
        "starts": [175, 184, 193, 201, 222, 231, 236, 239, 246, 256, 262, 268, 271],
    },
    "tlg003": {
        "title": "Nemean Odes", "greek": "Νεμεονῖκαι",
        "starts": [273, 280, 283, 291, 298, 304, 311, 320, 325, 331, 339, 343],
    },
    "tlg004": {
        "title": "Isthmian Odes", "greek": "Ἰσθμιονῖκαι",
        "starts": [345, 351, 355, 357, 363, 368, 374, 378, 385],
    },
}
FRAGMENT_WORK = "plg1p001"
FRAGMENT_START = 389
FRAGMENT_END = 497


def q(name): return f"{{{TEI}}}{name}"
def cq(name): return f"{{{CTS}}}{name}"
def xq(name): return f"{{{XML}}}{name}"


def text(element):
    return " ".join("".join(element.itertext()).split())


def indent(tree):
    if hasattr(ET, "indent"):
        ET.indent(tree, space="  ")


def pages(source):
    root = ET.parse(source).getroot()
    result = {}
    for page in root.findall(".//tei:div[@type='page']", NS):
        result[int(page.get("n"))] = page
    return root, result


def header(source_root, title, citation):
    root = ET.Element(q("teiHeader"))
    file_desc = ET.SubElement(root, q("fileDesc"))
    title_stmt = ET.SubElement(file_desc, q("titleStmt"))
    ET.SubElement(title_stmt, q("title")).text = title
    ET.SubElement(title_stmt, q("author")).text = "Pindar"
    ET.SubElement(title_stmt, q("editor")).text = "Theodor Bergk"
    ET.SubElement(title_stmt, q("editor")).text = "Otto Schroeder"
    resp = ET.SubElement(title_stmt, q("respStmt"))
    ET.SubElement(resp, q("resp")).text = "Diplomatic scan transcription and work-level compilation"
    ET.SubElement(resp, q("name")).text = "DeepSeek, under human review"
    pub = ET.SubElement(file_desc, q("publicationStmt"))
    ET.SubElement(pub, q("p")).text = "Research draft for the Perseus Multitext Viewer."
    source_desc = ET.SubElement(file_desc, q("sourceDesc"))
    bibl = ET.SubElement(source_desc, q("biblStruct"))
    monogr = ET.SubElement(bibl, q("monogr"))
    ET.SubElement(monogr, q("author")).text = "Pindar"
    ET.SubElement(monogr, q("title")).text = "Poetae Lyrici Graeci, Volume I: Pindari carmina"
    ET.SubElement(monogr, q("editor")).text = "Theodor Bergk; revised by Otto Schroeder"
    imprint = ET.SubElement(monogr, q("imprint"))
    ET.SubElement(imprint, q("pubPlace")).text = "Lipsiae"
    ET.SubElement(imprint, q("publisher")).text = "B. G. Teubner"
    ET.SubElement(imprint, q("date")).text = "1900"
    ET.SubElement(source_desc, q("ref"), {"target": "https://hdl.handle.net/2027/oxu1.602378615"}).text = "HathiTrust scan and OCR witness"
    encoding = ET.SubElement(root, q("encodingDesc"))
    refs = ET.SubElement(encoding, q("refsDecl"), {"n": "CTS"})
    if citation == "poem-line":
        outer = ET.SubElement(refs, q("citeStructure"), {"unit": "poem", "match": "//tei:div[@subtype='poem']", "use": "@n"})
        ET.SubElement(outer, q("citeStructure"), {"unit": "line", "match": ".//tei:l", "use": "@n"})
        patterns = [
            ("line", r"(\w+)\.(\w+)", "#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@subtype='poem' and @n='$1']//tei:l[@n='$2'])"),
            ("poem", r"(\w+)", "#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@subtype='poem' and @n='$1'])"),
        ]
    else:
        ET.SubElement(refs, q("citeStructure"), {"unit": "fragment", "match": "//tei:div[@subtype='fragment']", "use": "@n"})
        patterns = [("fragment", r"(.+)", "#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@subtype='fragment' and @n='$1'])")]
    for name, match, replacement in patterns:
        pattern = ET.SubElement(refs, q("cRefPattern"), {"n": name, "matchPattern": match, "replacementPattern": replacement})
        ET.SubElement(pattern, q("p")).text = f"This pointer extracts a printed {name}."
    profile = ET.SubElement(root, q("profileDesc"))
    usage = ET.SubElement(profile, q("langUsage"))
    ET.SubElement(usage, q("language"), {"ident": "grc"}).text = "Greek"
    ET.SubElement(usage, q("language"), {"ident": "la"}).text = "Latin"
    revision = ET.SubElement(root, q("revisionDesc"))
    ET.SubElement(revision, q("change"), {"when": REVISION_DATE}).text = (
        "Compiled from the retained volume TEI; printed pages retained only as provenance."
    )
    return root


def work_tree(source_root, page_map, work, spec):
    urn = f"urn:cts:greekLit:tlg0033.{work}.{VERSION}"
    root = ET.Element(q("TEI"), {xq("id"): f"tlg0033-{work}-{VERSION}"})
    root.append(header(source_root, f"Pindar, {spec['title']}", "poem-line"))
    text_el = ET.SubElement(root, q("text"), {xq("lang"): "grc", xq("base"): urn})
    body = ET.SubElement(text_el, q("body"), {xq("lang"): "grc", "n": urn})
    edition = ET.SubElement(body, q("div"), {"type": "edition", "n": urn, xq("lang"): "grc"})
    ET.SubElement(edition, q("head")).text = spec["greek"]
    starts = spec["starts"]
    for poem_no, (start, end) in enumerate(zip(starts, starts[1:]), 1):
        poem = ET.SubElement(edition, q("div"), {"type": "textpart", "subtype": "poem", "n": str(poem_no)})
        ET.SubElement(poem, q("head")).text = f"{spec['title']} {poem_no}"
        line_no = 0
        for page_no in range(start, end):
            page = page_map.get(page_no)
            if page is None:
                raise ValueError(f"Missing source page {page_no}")
            pb = page.find("tei:pb", NS)
            if pb is not None:
                poem.append(copy.deepcopy(pb))
            for child in page:
                if child.tag == q("pb"):
                    continue
                block = copy.deepcopy(child)
                for line in block.iter(q("l")):
                    line.attrib.pop("n", None)
                    if re.search(r"[\u0370-\u03ff\u1f00-\u1fff]", text(line)):
                        line_no += 1
                        line.set("n", str(line_no))
                poem.append(block)
        if not line_no:
            raise ValueError(f"No Greek verse lines in {work}, poem {poem_no}")
    return ET.ElementTree(root)


def fragment_label(element):
    if element.tag not in {q("p"), q("head")}:
        return None
    value = text(element).strip()
    if not re.match(r"^[*?†‡\s(]*\d", value):
        return None
    # Ignore concordance numbers in parentheses and prose following the
    # marker; retain the primary printed Bergk/Schroeder number or range.
    lead = re.sub(r"\([^)]*\)", "", value)
    marker = re.match(
        r"^[*?†‡\s]*([0-9]+\s*[A-Za-z]?)"
        r"(?:\s*(?:[.—–-]|\.\s*[*?†‡])\s*[*?†‡]*([0-9]+\s*[A-Za-z]?))?",
        lead,
    )
    if not marker:
        return None
    # A long ordinary sentence beginning with a number is not a marker.
    if len(lead) > 32 or re.search(r"[\u0370-\u03ff\u1f00-\u1fff]", lead):
        return None
    nums = [re.sub(r"\s+", "", n).upper() for n in marker.groups() if n]
    return nums[0] if len(nums) == 1 else f"{nums[0]}to{nums[-1]}"


def fragment_tree(source_root, page_map):
    urn = f"urn:cts:greekLit:tlg0033.{FRAGMENT_WORK}.{VERSION}"
    root = ET.Element(q("TEI"), {xq("id"): f"tlg0033-{FRAGMENT_WORK}-{VERSION}"})
    root.append(header(source_root, "Pindar, Fragments", "fragment"))
    text_el = ET.SubElement(root, q("text"), {xq("lang"): "grc", xq("base"): urn})
    body = ET.SubElement(text_el, q("body"), {xq("lang"): "grc", "n": urn})
    edition = ET.SubElement(body, q("div"), {"type": "edition", "n": urn, xq("lang"): "grc"})
    ET.SubElement(edition, q("head")).text = "Pindari fragmenta"
    current = None
    seen = {}
    for page_no in range(FRAGMENT_START, FRAGMENT_END):
        page = page_map[page_no]
        pending_pb = copy.deepcopy(page.find("tei:pb", NS))
        for child in page:
            if child.tag == q("pb"):
                continue
            label = fragment_label(child)
            if label:
                seen[label] = seen.get(label, 0) + 1
                occurrence = seen[label]
                unique = label if occurrence == 1 else f"{label}bis{occurrence - 1}"
                current = ET.SubElement(edition, q("div"), {
                    "type": "textpart", "subtype": "fragment", "n": unique,
                    xq("id"): f"schroeder-frag-{re.sub(r'[^A-Za-z0-9]+', '-', unique)}",
                })
            if current is None:
                continue
            if pending_pb is not None:
                current.append(pending_pb)
                pending_pb = None
            current.append(copy.deepcopy(child))
    fragments = edition.findall("tei:div[@subtype='fragment']", NS)
    if len(fragments) < 200:
        raise ValueError(f"Only {len(fragments)} fragment markers found; expected at least 200")
    return ET.ElementTree(root), [item.get("n") for item in fragments]


def group_metadata(path):
    root = ET.Element(cq("textgroup"), {"urn": "urn:cts:greekLit:tlg0033", "projid": "greekLit:tlg0033"})
    ET.SubElement(root, cq("groupname"), {xq("lang"): "eng"}).text = "Pindar"
    tree = ET.ElementTree(root); indent(tree)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def work_metadata(path, work, title, greek):
    work_urn = f"urn:cts:greekLit:tlg0033.{work}"
    root = ET.Element(cq("work"), {"groupUrn": "urn:cts:greekLit:tlg0033", "urn": work_urn, xq("lang"): "grc"})
    ET.SubElement(root, cq("title"), {xq("lang"): "eng"}).text = title
    edition = ET.SubElement(root, cq("edition"), {"urn": f"{work_urn}.{VERSION}", "workUrn": work_urn, xq("lang"): "grc"})
    ET.SubElement(edition, cq("label"), {xq("lang"): "grc"}).text = greek
    ET.SubElement(edition, cq("description"), {xq("lang"): "eng"}).text = (
        "Pindar. Poetae Lyrici Graeci I. Theodor Bergk, editor; Otto Schroeder, reviser. Leipzig: Teubner, 1900. OCR/AI research draft."
    )
    tree = ET.ElementTree(root); indent(tree)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def install(source, data_dir, audit_path=None):
    source_root, page_map = pages(source)
    target_group = data_dir / "tlg0033"
    target_group.mkdir(parents=True, exist_ok=True)
    group_metadata(target_group / "__cts__.xml")
    audit = {"source": str(source), "version": VERSION, "works": {}}
    for work, spec in WORKS.items():
        folder = target_group / work
        folder.mkdir(parents=True, exist_ok=True)
        tree = work_tree(source_root, page_map, work, spec); indent(tree)
        destination = folder / f"tlg0033.{work}.{VERSION}.xml"
        tree.write(destination, encoding="utf-8", xml_declaration=True)
        work_metadata(folder / "__cts__.xml", work, spec["title"], spec["greek"])
        audit["works"][work] = {"poems": len(spec["starts"]) - 1, "path": str(destination)}
    folder = target_group / FRAGMENT_WORK
    folder.mkdir(parents=True, exist_ok=True)
    tree, labels = fragment_tree(source_root, page_map); indent(tree)
    destination = folder / f"tlg0033.{FRAGMENT_WORK}.{VERSION}.xml"
    tree.write(destination, encoding="utf-8", xml_declaration=True)
    work_metadata(folder / "__cts__.xml", FRAGMENT_WORK, "Fragments", "Fragmenta")
    audit["works"][FRAGMENT_WORK] = {"fragments": len(labels), "first": labels[:5], "last": labels[-5:], "path": str(destination)}
    if audit_path:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return audit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args()
    print(json.dumps(install(args.source, args.data_dir, args.audit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
