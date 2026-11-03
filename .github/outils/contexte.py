#!/usr/bin/env python3
"""Affiche seulement les sections du contexte projet utiles à une étape.

Pourquoi : le contexte grossit à chaque US. Le lire en entier à chaque étape
fait payer, à chaque action de l'agent, des sections dont l'étape n'a pas besoin
(journal, liste des sources, points déjà répondus).

Usage :
  python3 .github/outils/contexte.py <CONTEXTE.md | auto> <étape>
  python3 .github/outils/contexte.py <CONTEXTE.md> --sections 2,9
  python3 .github/outils/contexte.py <CONTEXTE.md> <étape> --sections 10   (ajoute des sections)
  python3 .github/outils/contexte.py <CONTEXTE.md> tout

Étapes : coherence, analyse, gherkin, publication, anomalie, tout.
En section 9, les points à l'état « répondu » ou « remplacé » sont retirés,
sauf pour « tout ». Pour l'analyse, la rédaction et l'anomalie, la section 9
est aussi réduite aux colonnes ID, Sujet, Question et Bloquante : le détail
(« Ce qui est connu », « Impact ») ne sert qu'à la cohérence du sprint.
"""
import re
import sys

SECTIONS = {
    "coherence": [0, 2, 5, 6, 9],
    "analyse": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "gherkin": [1, 3, 4, 5, 7, 8],
    "publication": [0],
    "anomalie": [0, 1, 3, 4, 7],
}
FERME = re.compile(r"\|\s*(répondu|repondu|remplacé|remplacée|remplace)\b[^|]*\|\s*$", re.I)


def trouver_contexte(chemin):
    """« auto » : le seul docs/projets/<projet>/CONTEXTE.md autre que _modele."""
    if chemin != "auto":
        return chemin, None
    import glob
    trouves = [c for c in sorted(glob.glob("docs/projets/*/CONTEXTE.md")) if "/_modele/" not in c]
    if len(trouves) == 1:
        return trouves[0], None
    if not trouves:
        return None, "ÉCHEC : aucun contexte projet dans docs/projets/. Proposer init-contexte."
    return None, "ÉCHEC : plusieurs projets (%s). Préciser projet=<nom>." % ", ".join(c.split("/")[2] for c in trouves)


GARDER = ("id", "sujet", "question", "bloquante")
COMPACT = {"analyse", "gherkin", "anomalie"}


def compacter_tableaux(section):
    """Dans les tableaux, ne garde que les colonnes ID, Sujet, Question, Bloquante."""
    sortie, garder = [], None
    for ligne in section.splitlines():
        if not ligne.startswith("|"):
            garder = None
            sortie.append(ligne)
            continue
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if garder is None:
            garder = [i for i, c in enumerate(cellules) if c.lower().startswith(GARDER)]
            if len(garder) < 2:
                garder = list(range(len(cellules)))
        if set("".join(cellules)) <= set("-: "):
            sortie.append("|" + "|".join("---" for _ in garder) + "|")
            continue
        sortie.append("| " + " | ".join(cellules[i] for i in garder if i < len(cellules)) + " |")
    return "\n".join(sortie)


def decouper(texte):
    """Renvoie l'en-tête (avant la première section) et {numéro: texte}."""
    morceaux = re.split(r"(?m)^(?=## \d+\.)", texte)
    entete, sections = morceaux[0], {}
    for m in morceaux[1:]:
        n = int(re.match(r"## (\d+)\.", m).group(1))
        sections[n] = m
    return entete, sections


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    chemin, etape = argv[1], argv[2]
    chemin, erreur = trouver_contexte(chemin)
    if erreur:
        print(erreur)
        return 3
    print("[Contexte : %s]" % chemin)
    try:
        with open(chemin, encoding="utf-8") as f:
            texte = f.read()
    except FileNotFoundError:
        print("ÉCHEC : %s n'existe pas. Proposer init-contexte." % chemin)
        return 3

    if etape == "tout":
        print(texte)
        return 0
    if etape == "--sections":
        voulues = [int(x) for x in argv[3].split(",")]
    elif etape in SECTIONS:
        voulues = list(SECTIONS[etape])
        if len(argv) > 4 and argv[3] == "--sections":
            voulues += [int(x) for x in argv[4].split(",") if int(x) not in voulues]
    else:
        print("ÉCHEC : étape inconnue « %s ». Étapes : %s, tout." % (etape, ", ".join(SECTIONS)))
        return 2

    entete, sections = decouper(texte)
    absentes = [n for n in voulues if n not in sections]
    print(entete.strip())
    print()
    print("[Sections lues : %s. Les autres sont disponibles avec --sections.]" % ", ".join(map(str, voulues)))
    if absentes:
        print("[Sections absentes du fichier : %s]" % ", ".join(map(str, absentes)))
    for n in voulues:
        if n not in sections:
            continue
        s = sections[n]
        if n == 9:
            s = "\n".join(l for l in s.splitlines() if not FERME.search(l))
            if etape in COMPACT:
                s = compacter_tableaux(s)
        print()
        print(s.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
