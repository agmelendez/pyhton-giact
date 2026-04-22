"""Sincroniza teoría y supuestos de laboratorios cualitativos (01-11)
from metodos_cualitativos_marino_costeros_actualizado.md hacia cases.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

MD_PATH = Path("metodos_cualitativos_marino_costeros_actualizado.md")
CASES_PATH = Path("cases.json")

SECTION_RE = re.compile(
    r"## Laboratorio (\d{2}) — (.*?)\n### Teoría\n(.*?)\n\n### Supuestos\n(.*?)(?=\n\n## Laboratorio|\Z)",
    re.S,
)


def parse_md_sections(markdown: str) -> dict[str, tuple[str, str, str]]:
    sections: dict[str, tuple[str, str, str]] = {}
    for num, title, theory, assumptions in SECTION_RE.findall(markdown):
        theory_paragraphs = [p.strip() for p in theory.strip().split("\n\n") if p.strip()]
        assumptions_items = [
            line[2:].strip() for line in assumptions.splitlines() if line.strip().startswith("- ")
        ]

        theory_html = f"<h4>Laboratorio {num} · {title}</h4>" + "".join(
            f"<p>{paragraph}</p>" for paragraph in theory_paragraphs
        )
        assumptions_html = "<ul>" + "".join(f"<li>{item}</li>" for item in assumptions_items) + "</ul>"
        sections[num] = (title, theory_html, assumptions_html)
    return sections


def sync_cases(sections: dict[str, tuple[str, str, str]], cases_doc: dict) -> int:
    updated = 0
    for case in cases_doc.get("cases", []):
        match = re.match(r"cuali-(\d{2})-", case.get("id", ""))
        if not match:
            continue

        lab_num = match.group(1)
        if lab_num not in sections:
            continue

        _, theory_html, assumptions_html = sections[lab_num]
        if case.get("theory") != theory_html:
            case["theory"] = theory_html
            updated += 1
        if case.get("assumptions") != assumptions_html:
            case["assumptions"] = assumptions_html
            updated += 1
    return updated


def main() -> None:
    md_text = MD_PATH.read_text(encoding="utf-8")
    sections = parse_md_sections(md_text)

    if len(sections) != 11:
        raise ValueError(f"Se esperaban 11 laboratorios en el Markdown y se encontraron {len(sections)}")

    cases_doc = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    updates = sync_cases(sections, cases_doc)
    CASES_PATH.write_text(json.dumps(cases_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Laboratorios detectados en MD: {len(sections)}")
    print(f"Campos actualizados en cases.json: {updates}")


if __name__ == "__main__":
    main()
