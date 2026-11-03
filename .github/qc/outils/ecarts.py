#!/usr/bin/env python3
"""Extrait d'un rapport de cohérence de sprint ce qui concerne une US.

Pourquoi : le rapport de cohérence couvre tout le sprint et il est long.
L'analyse d'une US n'a besoin que de ses écarts, des cas à revoir, des données
à demander et de sa place dans l'ordre d'analyse. Le reste n'est pas relu.

Usage :
  python3 .github/qc/outils/ecarts.py <id US> [rapport.md]

Sans rapport indiqué, lit tous les qc-reports/sprint-*-coherence.md.
"""
import glob
import re
import sys

SECTIONS_UTILES = ("## 3.", "## 4.", "## 5.", "## 6.")


def extraire(chemin, us_id):
    with open(chemin, encoding="utf-8") as f:
        lignes = f.read().splitlines()
    sortie, titre, entete, dans = [], None, [], False
    motif = re.compile(r"(?<!\d)%s(?!\d)" % re.escape(us_id))
    for l in lignes:
        if l.startswith("## "):
            dans = l.startswith(SECTIONS_UTILES)
            titre, entete = l, []
            continue
        if not dans or not l.startswith("|"):
            continue
        if not entete or (len(entete) == 1 and set(l.replace("|", "").strip()) <= set("-: ")):
            entete.append(l)
            continue
        if motif.search(l):
            if titre:
                sortie += ["", titre] + entete
                titre = None
            sortie.append(l)
    return sortie


def main(argv):
    if len(argv) < 2 or not argv[1].isdigit():
        print(__doc__)
        return 2
    us_id = argv[1]
    rapports = argv[2:] or sorted(glob.glob("qc-reports/sprint-*-coherence.md"))
    if not rapports:
        print("Aucun rapport de cohérence de sprint dans qc-reports/.")
        return 0
    for r in rapports:
        lignes = extraire(r, us_id)
        print("[Rapport %s : %s]" % (r, "%d ligne(s) sur l'US %s" % (sum(1 for x in lignes if x.startswith("|") and us_id in x), us_id) if lignes else "aucun écart sur l'US %s" % us_id))
        print("\n".join(lignes).strip())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
