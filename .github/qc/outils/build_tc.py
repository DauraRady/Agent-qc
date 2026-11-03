#!/usr/bin/env python3
"""Contrôle et construction des scénarios Gherkin du QC agent, sans IA.

Quatre commandes :
  check  RAPPORT.md                         contrôle les blocs ```gherkin du rapport
  table  RAPPORT.md --out FICHIER.md        le tableau ID | Test case | Gherkin BDD scenario | Type of test,
                                            préconditions répétées dans chaque cas, paramètres en @param
  build  RAPPORT.md --us ID --out DOSSIER   un fichier JSON-Patch par scénario (API Azure DevOps)
                                            et un manifest.json
  csv    RAPPORT.md --us ID --out FICHIER   un CSV à importer dans Test Plans (aucune écriture API)

Type d'un scénario : une ligne de commentaire « # Type : UI » sous son titre. Sans elle : Fonctionnel.

Le rapport est qc-reports/US-<id>.md, relu par un humain. Le script lit tous les blocs
```gherkin du fichier. Aucun appel réseau.

Codes de sortie : 0 = OK, 1 = erreurs dans le rapport, 2 = fichier introuvable.
"""
import argparse
import csv
import json
import os
import re
import sys
from xml.sax.saxutils import escape

GIVEN = ("Étant donné", "Etant donné", "Soit")
WHEN = ("Quand", "Lorsque")
THEN = ("Alors",)
AND = ("Et", "Mais")
ENGLISH = re.compile(r"^(Given|When|Then|And|But|Feature|Scenario|Scenario Outline|Background|Examples)\b")
VAGUE = [r"\bcorrectement\b", r"\bnormalement\b", r"\bcomme prévu\b", r"\bfonctionne\b", r"\best OK\b",
         r"\bavec succès\b", r"\bbien\b"]
PARAM = re.compile(r"<([a-z_][a-z0-9_]*)>")
TYPE_LINE = re.compile(r"^#\s*Type\s*:\s*(.+)$", re.IGNORECASE)
TYPES = ("Fonctionnel", "UI", "API", "Sécurité", "Performance", "Accessibilité", "UAT", "Exploratoire")
MAX_TITLE = 128


def starts(line, words):
    return any(line == w or line.startswith(w + " ") or line.startswith(w + "'") or line.startswith(w + "’")
               for w in words)


def outside_quotes(text):
    return re.sub(r"[\"«“][^\"»”]*[\"»”]", "", text)


def gherkin_blocks(path):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    blocks, current = [], None
    for raw in lines:
        s = raw.strip()
        if current is None and s.startswith("```gherkin"):
            current = []
        elif current is not None and s.startswith("```"):
            blocks.append(current)
            current = None
        elif current is not None:
            current.append(s)
    return blocks


def parse(blocks):
    """Retourne la liste des scénarios : titre, plan, préconditions, actions, résultats, exemples."""
    scenarios, errors = [], []
    for block in blocks:
        context, scen, in_context, in_examples = [], None, False, False
        for line in block:
            m = TYPE_LINE.match(line)
            if m and scen is not None:
                scen["type"] = m.group(1).strip()
                continue
            if not line or line.startswith("#") or line.startswith("@"):
                continue
            if ENGLISH.match(line):
                errors.append(f"mot-clé anglais : « {line[:60]} »")
                continue
            if line.startswith("Fonctionnalité"):
                continue
            if line.startswith("Contexte"):
                in_context, in_examples = True, False
                continue
            if line.startswith("Scénario") or line.startswith("Plan du scénario"):
                in_context, in_examples = False, False
                scen = {"title": line.split(":", 1)[1].strip() if ":" in line else line,
                        "plan": line.startswith("Plan"), "context": list(context),
                        "given": [], "when": [], "then": [], "examples": [], "phase": None, "errors": [],
                        "type": "Fonctionnel"}
                scenarios.append(scen)
                continue
            if line.startswith("Exemples"):
                in_examples = True
                continue
            if in_examples and line.startswith("|"):
                scen["examples"].append([c.strip() for c in line.strip("|").split("|")])
                continue
            if in_context:
                context.append(line)
                continue
            if scen is None:
                continue
            if starts(line, GIVEN):
                if scen["phase"] in ("when", "then"):
                    scen["errors"].append("Étant donné après une action ou un résultat")
                scen["phase"] = "given"
                scen["given"].append(line)
            elif starts(line, WHEN):
                if scen["phase"] == "when":
                    scen["errors"].append("deuxième Quand : écrire les actions suivantes avec Et")
                if scen["phase"] == "then":
                    scen["errors"].append("Quand après Alors : deux comportements, faire deux scénarios")
                scen["phase"] = "when"
                scen["when"].append(line)
            elif starts(line, THEN):
                if scen["phase"] != "when":
                    scen["errors"].append("Alors sans Quand avant")
                scen["phase"] = "then"
                scen["then"].append(line)
            elif starts(line, AND):
                if scen["phase"] is None:
                    scen["errors"].append(f"« {line[:40]} » sans mot-clé avant")
                else:
                    scen[scen["phase"]].append(line)
            else:
                scen["errors"].append(f"ligne non reconnue : « {line[:60]} »")
    return scenarios, errors


def check(scenarios, block_errors):
    errors, warnings, seen = list(block_errors), [], {}
    if not scenarios:
        errors.append("aucun scénario trouvé dans les blocs ```gherkin")
    for sc in scenarios:
        t = sc["title"]
        errors += [f"« {t} » : {e}" for e in sc["errors"]]
        if t in seen:
            errors.append(f"titre en double : « {t} »")
        seen[t] = True
        if not sc["when"]:
            errors.append(f"« {t} » : aucun Quand")
        if not sc["then"]:
            errors.append(f"« {t} » : aucun Alors")
        pre = sc["context"] + sc["given"]
        if not pre:
            errors.append(f"« {t} » : aucune précondition (ni Contexte ni Étant donné)")
        elif not any("connecté" in p for p in pre):
            warnings.append(f"« {t} » : le rôle connecté n'est pas précisé")
        for line in sc["then"]:
            bare = outside_quotes(line)
            for pat in VAGUE:
                if re.search(pat, bare, re.IGNORECASE):
                    errors.append(f"« {t} » : résultat vague « {line[:60]} »")
                    break
            if re.search(r"\bou\b", bare):
                errors.append(f"« {t} » : résultat avec une alternative (« ou ») : « {line[:60]} »")
        steps = len(pre) + len(sc["when"]) + len(sc["then"])
        if steps > 14:
            warnings.append(f"« {t} » : {steps} étapes, vérifier qu'il ne teste qu'un comportement")
        used = set(PARAM.findall(" ".join(sc["context"] + sc["given"] + sc["when"] + sc["then"])))
        if sc["plan"]:
            if len(sc["examples"]) < 2:
                errors.append(f"« {t} » : Plan du scénario sans lignes d'Exemples")
            else:
                header = sc["examples"][0]
                missing = used - set(header)
                if missing:
                    errors.append(f"« {t} » : paramètres absents des Exemples : {', '.join(sorted(missing))}")
                rows = [tuple(r) for r in sc["examples"][1:]]
                if len(rows) != len(set(rows)):
                    errors.append(f"« {t} » : lignes d'Exemples en double")
                if len(rows) == 1:
                    warnings.append(f"« {t} » : une seule ligne d'Exemples, un Scénario simple suffit")
        elif used:
            errors.append(f"« {t} » : paramètres <…> dans un Scénario simple")
        if sc["type"] not in TYPES:
            warnings.append(f"« {t} » : type « {sc['type']} » inhabituel (attendu : {', '.join(TYPES)})")
    return errors, warnings


def cell(text):
    return "&lt;br/&gt;".join(escape(escape(line)) for line in text.split("\n"))


def to_ado(text):
    return PARAM.sub(r"@\1", text)


def steps_of(sc, transform=to_ado):
    """Pas 1 : préconditions ; un pas par action ; résultats sur le dernier pas d'action."""
    pairs = []
    pre = sc["context"] + sc["given"]
    if pre:
        pairs.append(("\n".join(transform(p) for p in pre), ""))
    for i, a in enumerate(sc["when"]):
        last = i == len(sc["when"]) - 1
        pairs.append((transform(a), "\n".join(transform(r) for r in sc["then"]) if last else ""))
    return pairs


def steps_xml(pairs):
    out, sid = [], 1
    for action, expected in pairs:
        sid += 1
        kind = "ValidateStep" if expected else "ActionStep"
        out.append(f'<step id="{sid}" type="{kind}"><parameterizedString isformatted="true">{cell(action)}'
                   f'</parameterizedString><parameterizedString isformatted="true">{cell(expected)}'
                   f'</parameterizedString><description/></step>')
    return f'<steps id="0" last="{sid}">' + "".join(out) + "</steps>"


def params_xml(names, rows):
    params = "<parameters>" + "".join(f'<param name="{n}" bind="default"/>' for n in names) + "</parameters>"
    cols = "".join(f'<xs:element name="{n}" type="xs:string" minOccurs="0" />' for n in names)
    data = "".join("<Table1>" + "".join(f"<{n}>{escape(v)}</{n}>" for n, v in zip(names, r)) + "</Table1>"
                   for r in rows)
    source = ('<NewDataSet><xs:schema id="NewDataSet" xmlns="" xmlns:xs="http://www.w3.org/2001/XMLSchema" '
              'xmlns:msdata="urn:schemas-microsoft-com:xml-msdata">'
              '<xs:element name="NewDataSet" msdata:IsDataSet="true" msdata:Locale="">'
              '<xs:complexType><xs:choice minOccurs="0" maxOccurs="unbounded">'
              '<xs:element name="Table1"><xs:complexType><xs:sequence>' + cols +
              '</xs:sequence></xs:complexType></xs:element></xs:choice></xs:complexType></xs:element>'
              '</xs:schema>' + data + '</NewDataSet>')
    return params, source


def short(title):
    return title if len(title) <= MAX_TITLE else title[:MAX_TITLE - 1] + "…"


def build_patch(sc, args):
    ops = [
        {"op": "add", "path": "/fields/System.Title", "value": short(sc["title"])},
        {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.Steps", "value": steps_xml(steps_of(sc))},
        {"op": "add", "path": "/fields/System.Tags", "value": f"QC-agent; US-{args.us}"},
    ]
    if args.assignee:
        ops.append({"op": "add", "path": "/fields/System.AssignedTo", "value": args.assignee})
    if args.area:
        ops.append({"op": "add", "path": "/fields/System.AreaPath", "value": args.area})
    if args.iteration:
        ops.append({"op": "add", "path": "/fields/System.IterationPath", "value": args.iteration})
    if sc["plan"] and len(sc["examples"]) > 1:
        header = sc["examples"][0]
        keep = [i for i, n in enumerate(header) if n != "cas"]
        rows = [[r[i] for i in keep] for r in sc["examples"][1:]]
        params, source = params_xml([header[i] for i in keep], rows)
        ops.append({"op": "add", "path": "/fields/Microsoft.VSTS.TCM.Parameters", "value": params})
        ops.append({"op": "add", "path": "/fields/Microsoft.VSTS.TCM.LocalDataSource", "value": source})
    return ops


def variants(sc):
    """Pour le CSV : un cas par ligne d'Exemples, paramètres remplacés par leur valeur."""
    if not sc["plan"] or len(sc["examples"]) < 2:
        return [(sc["title"], lambda s: s)]
    header, out = sc["examples"][0], []
    for row in sc["examples"][1:]:
        values = dict(zip(header, row))
        label = values.get("cas") or ", ".join(v for k, v in values.items() if k != "cas")
        out.append((f"{sc['title']} ({label})",
                    lambda s, v=values: PARAM.sub(lambda m: v.get(m.group(1), m.group(0)), s)))
    return out


def md(text):
    return text.replace("|", "\\|")


def write_table(scenarios, out):
    """Tableau à 4 colonnes, une ligne par cas ; les préconditions du Contexte sont répétées."""
    lines = ["| ID | Test case | Gherkin BDD scenario | Type of test |", "|---|---|---|---|"]
    params = []
    for i, sc in enumerate(scenarios, 1):
        tc = f"TC-{i:03d}"
        steps = [to_ado(l) for l in sc["context"] + sc["given"] + sc["when"] + sc["then"]]
        lines.append(f"| {tc} | {md(sc['title'])} | {'<br>'.join(md(l) for l in steps)} | {sc['type']} |")
        if sc["plan"] and len(sc["examples"]) > 1:
            header = sc["examples"][0]
            params.append(f"\n{tc} : paramètres\n")
            params.append("| " + " | ".join("cas" if n == "cas" else "@" + n for n in header) + " |")
            params.append("|" + "---|" * len(header))
            params += ["| " + " | ".join(md(v) for v in r) + " |" for r in sc["examples"][1:]]
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n" + ("\n".join(params) + "\n" if params else ""))
    return len(scenarios)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").add_argument("report")
    t = sub.add_parser("table")
    t.add_argument("report")
    t.add_argument("--out", required=True)
    for name in ("build", "csv"):
        q = sub.add_parser(name)
        q.add_argument("report")
        q.add_argument("--us", required=True)
        q.add_argument("--out", required=True)
        q.add_argument("--assignee", default="")
        q.add_argument("--area", default="")
        q.add_argument("--iteration", default="")
        q.add_argument("--state", default="Design")
    args = p.parse_args()

    if not os.path.isfile(args.report):
        print(f"ERREUR : rapport introuvable : {args.report}")
        return 2
    scenarios, block_errors = parse(gherkin_blocks(args.report))
    errors, warnings = check(scenarios, block_errors)
    for w in warnings:
        print(f"AVERTISSEMENT : {w}")
    for e in errors:
        print(f"ERREUR : {e}")
    print(f"BILAN : {len(scenarios)} scénario(s), {len(errors)} erreur(s), {len(warnings)} avertissement(s)")
    if errors:
        return 1
    if args.cmd == "check":
        return 0
    if args.cmd == "table":
        n = write_table(scenarios, args.out)
        print(f"TABLEAU : {n} cas dans {args.out}")
        return 0

    if args.cmd == "build":
        os.makedirs(args.out, exist_ok=True)
        manifest = []
        for i, sc in enumerate(scenarios, 1):
            path = os.path.join(args.out, f"tc-{i:02d}.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(build_patch(sc, args), fh, ensure_ascii=False)
            manifest.append({"title": short(sc["title"]), "file": path})
        with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
        print(f"CONSTRUIT : {len(manifest)} fichier(s), manifest dans {args.out}/manifest.json")
        return 0

    rows = [["ID", "Work Item Type", "Title", "Test Step", "Step Action", "Step Expected",
             "Area Path", "Assigned To", "State", "Tags"]]
    count = 0
    for sc in scenarios:
        for title, fill in variants(sc):
            count += 1
            rows.append(["", "Test Case", short(title), "", "", "", args.area, args.assignee, args.state,
                         f"QC-agent; US-{args.us}"])
            for n, (action, expected) in enumerate(steps_of(sc, fill), 1):
                rows.append(["", "", "", str(n), action, expected, "", "", "", ""])
    folder = os.path.dirname(args.out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(args.out, "w", encoding="utf-8-sig", newline="") as fh:
        csv.writer(fh).writerows(rows)
    print(f"CSV : {count} cas dans {args.out}")
    if not args.area:
        print("AVERTISSEMENT : Area Path vide, à remplir avant l'import (obligatoire sur Azure DevOps Services)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
