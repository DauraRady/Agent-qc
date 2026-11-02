#!/usr/bin/env python3
"""Lit une User Story Azure DevOps et n'affiche que ce dont l'agent a besoin.

Pourquoi : la réponse brute de l'API ($expand=all) contient le HTML, les liens,
les métadonnées de chaque champ. Elle reste ensuite dans la conversation et
est relue à chaque action de l'agent. Ce script la réduit à un texte court.

Usage :
  python3 .github/outils/lire_us.py <id> --url <url organisation> --projet <projet ADO>
         [--commentaires] [--export <dossier sources>]

Le PAT est lu dans la variable ADO_PAT. Il n'est jamais affiché.
Sans PAT ou sans réponse d'Azure DevOps, le script lit l'export
<dossier sources>/US-<id>.md s'il existe.

Codes de sortie : 0 lu, 2 échec Azure DevOps, 3 ni Azure DevOps ni export.
"""
import argparse
import base64
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

CHAMPS = [
    ("System.Title", "Titre"),
    ("System.WorkItemType", "Type"),
    ("System.State", "État"),
    ("System.Rev", "Révision"),
    ("System.ChangedDate", "Modifiée le"),
    ("System.TeamProject", "Projet"),
    ("System.AreaPath", "Area Path"),
    ("System.IterationPath", "Itération"),
]
TEXTES = [
    ("System.Description", "Description"),
    ("Microsoft.VSTS.Common.AcceptanceCriteria", "Critères d'acceptation"),
]
MESSAGES = {
    203: "PAT invalide ou sans le droit requis",
    401: "PAT invalide ou sans le droit requis",
    403: "pas d'accès",
    404: "work item introuvable",
}


def html_en_texte(valeur):
    """Convertit le HTML d'un champ Azure DevOps en texte lisible."""
    if not valeur:
        return ""
    t = re.sub(r"(?i)<br\s*/?>", "\n", valeur)
    t = re.sub(r"(?i)</(p|div|h[1-6]|tr|table|ul|ol)>", "\n", t)
    t = re.sub(r"(?i)<li[^>]*>", "\n1. ", t)
    t = re.sub(r"(?i)</t[dh]>", " | ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("\xa0", " ")
    lignes = [re.sub(r"[ \t]+", " ", l).strip() for l in t.splitlines()]
    sortie, vide = [], False
    for l in lignes:
        if not l:
            if not vide:
                sortie.append("")
            vide = True
        else:
            sortie.append(l)
            vide = False
    return "\n".join(sortie).strip()


def appel(url, pat):
    jeton = base64.b64encode((":" + pat).encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": "Basic " + jeton, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, str(getattr(e, "reason", e))


def depuis_export(dossier, us_id, raison):
    chemin = os.path.join(dossier or "", "US-%s.md" % us_id)
    if dossier and os.path.isfile(chemin):
        print("US %s lue dans l'export %s (%s), sans les commentaires." % (us_id, chemin, raison))
        print()
        with open(chemin, encoding="utf-8") as f:
            print(f.read().strip())
        return 0
    print("ÉCHEC : %s, et aucun export %s." % (raison, chemin if dossier else "indiqué (--export)"))
    return 3


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    p.add_argument("--url", required=True, help="https://dev.azure.com/<organisation> ou https://<organisation>.visualstudio.com")
    p.add_argument("--projet", required=True)
    p.add_argument("--commentaires", action="store_true")
    p.add_argument("--export", help="dossier docs/projets/<projet>/sources")
    a = p.parse_args()

    if not re.fullmatch(r"\d+", a.id):
        print("ÉCHEC : identifiant d'US invalide.")
        return 2
    pat = os.environ.get("ADO_PAT", "")
    if not pat:
        return depuis_export(a.export, a.id, "ADO_PAT absent")

    base = "%s/%s/_apis/wit/workitems/%s" % (a.url.rstrip("/"), urllib.request.quote(a.projet), a.id)
    code, corps = appel(base + "?$expand=relations&api-version=7.1", pat)
    if code != 200:
        raison = "Azure DevOps a répondu %s (%s)" % (code, MESSAGES.get(code, "échec")) if code else "Azure DevOps ne répond pas"
        if code in (0, 401, 203):
            return depuis_export(a.export, a.id, raison)
        print("ÉCHEC : " + raison + ".")
        return 2

    wi = json.loads(corps)
    f = wi.get("fields", {})
    print("# US %s : %s" % (a.id, f.get("System.Title", "")))
    print()
    for cle, nom in CHAMPS[1:]:
        if cle in f:
            print("%s : %s" % (nom, f[cle]))
    for cle, nom in TEXTES:
        print()
        print("## " + nom)
        print(html_en_texte(f.get(cle)) or "Aucun")

    liens = wi.get("relations") or []
    print()
    print("## Liens (%d)" % len(liens))
    for r in liens:
        nom = (r.get("attributes") or {}).get("name", r.get("rel", ""))
        cible = r.get("url", "").rstrip("/").split("/")[-1]
        print("%s : %s" % (nom, cible))

    if a.commentaires:
        code, corps = appel(base.replace("/workitems/", "/workItems/") + "/comments?order=asc&api-version=7.1-preview.4", pat)
        print()
        if code != 200:
            print("## Commentaires : non lus (Azure DevOps a répondu %s)" % code)
        else:
            com = json.loads(corps).get("comments", [])
            print("## Commentaires (%d, auteurs non affichés)" % len(com))
            for c in com:
                print()
                print("Le %s :" % c.get("createdDate", "")[:10])
                print(html_en_texte(c.get("text")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
