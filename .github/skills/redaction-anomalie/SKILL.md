---
name: redaction-anomalie
description: 'Rédige une anomalie (bug fonctionnel ou d''interface) reproductible et sourcée à partir de ce que le testeur a constaté, vérifie les doublons, puis la crée dans Azure DevOps après aperçu et validation explicite. À utiliser pour « rédige un bug », « j''ai trouvé une anomalie », « crée le bug dans ADO ».'
argument-hint: '<ce que j''ai constaté>'
---

# Rédaction d'une anomalie

Arguments : ceux donnés dans la demande (numéros d'US, options).

`<url>` et `<projet ADO>` viennent de la section 0 du contexte du projet.

Un bon bug se reproduit sans poser de question, compare un résultat obtenu à un résultat attendu sourcé, et ne contient qu'un seul écart.

## 1. Recueillir les faits

Demander ce qui manque, en une seule fois, parmi :
1. L'US concernée (id) et, si connu, le cas de test exécuté.
2. L'environnement (ceux de la section 0 du contexte), la version ou la date du déploiement, le navigateur.
3. Le rôle utilisé (jamais le nom d'une vraie personne : « compte Admin de test »).
4. Les étapes faites, dans l'ordre, et les données utilisées.
5. Ce qui s'est affiché.
6. Combien de fois c'est arrivé : systématique, ou x fois sur y.

Une capture d'écran qui montre des données client réelles ne doit pas être utilisée telle quelle : demander une version masquée. L'agent ne joint pas les captures : le testeur les ajoute lui-même après la création.

## 2. Trouver le résultat attendu

1. Lire l'US (description, critères, commentaires) avec le même accès que l'agent.
2. Le résultat attendu doit venir d'une source : un critère d'acceptation, une règle de l'US, un commentaire du PO (auteur et date), ou la maquette citée par l'US (le testeur décrit ce qu'elle montre ; l'agent ne la lit pas).
3. Si aucune source ne dit ce qui était attendu, ce n'est pas un bug mais une question : proposer de la formuler pour le PO au lieu de créer l'anomalie.

## 3. Vérifier les doublons

Chercher les bugs ouverts qui ressemblent, avec deux ou trois mots clés du titre (corps dans un fichier) :

```json
{"query": "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.TeamProject] = @project AND [System.WorkItemType] = 'Bug' AND [System.Title] CONTAINS 'Retard'"}
```

envoyé en POST sur `<url>/<projet ADO>/_apis/wit/wiql?api-version=7.1`. Montrer les résultats proches. Si l'un correspond, proposer de commenter ce bug plutôt que d'en créer un.

## 4. Rédiger

| Champ | Contenu |
|---|---|
| Titre | « <Écran ou fonction> : <résultat obtenu> au lieu de <résultat attendu> ». Exemple : « Liste des demandes : une demande créée il y a 61 jours reste « En cours » au lieu de « Retard » » |
| Environnement | Environnement, version ou date, navigateur, rôle de test |
| Préconditions | Les données nécessaires, avec identifiants fictifs ou de recette |
| Étapes | Numérotées, une action par étape, assez précises pour être rejouées sans question |
| Résultat obtenu | Ce qui s'affiche, mot pour mot pour un message |
| Résultat attendu | Ce qui devait s'afficher, avec sa source (US <id> et critère, ou commentaire du <date>) |
| Fréquence | Systématique, ou x fois sur y |
| Gravité proposée | Voir l'échelle, avec une phrase de justification |
| Liens | US concernée, et cas de test s'il existe |

Règles :
1. Un seul écart par bug. Deux écarts font deux bugs.
2. Des faits, pas de supposition sur la cause dans le corps du bug.
3. Pas de mots vagues : « ne marche pas », « bug d'affichage », « erreur » sans le texte affiché.
4. Bug d'interface (libellé, alignement, couleur, champ absent) : préciser l'élément, ce qui est affiché, ce que montre la maquette d'après le testeur, et la résolution d'écran si elle compte.

Échelle de gravité, à aligner sur celle de l'équipe :

| Gravité ADO | Quand |
|---|---|
| 1 - Critical | Blocage d'un parcours principal sans contournement, perte ou corruption de données, faille de droits |
| 2 - High | Règle métier fausse ou fonction principale en échec, avec contournement |
| 3 - Medium | Fonction secondaire en échec, ou règle fausse dans un cas limite |
| 4 - Low | Affichage, libellé, ergonomie, sans effet sur les données |

## 5. Aperçu, puis validation

Afficher l'anomalie complète telle qu'elle sera créée, puis demander : « Je crée ce bug dans Azure DevOps ? ». Continuer seulement sur un « oui » explicite. Le testeur peut corriger le texte avant.

## 6. Créer et lier

1. Écrire les champs dans `.qc-agent/bug.json` puis construire le corps sans écrire le HTML à la main :
   ```bash
   python3 - .qc-agent/bug.json > .qc-agent/bug-patch.json <<'EOF'
   import json, sys, html
   b = json.load(open(sys.argv[1], encoding="utf-8"))
   def h(t): return "<br/>".join(html.escape(l) for l in t.split("\n"))
   repro = ("<b>Environnement</b><br/>" + h(b["environnement"]) + "<br/><br/><b>Préconditions</b><br/>" + h(b["preconditions"])
            + "<br/><br/><b>Étapes</b><br/>" + h(b["etapes"]) + "<br/><br/><b>Résultat obtenu</b><br/>" + h(b["obtenu"])
            + "<br/><br/><b>Résultat attendu</b><br/>" + h(b["attendu"]) + "<br/><br/><b>Fréquence</b><br/>" + h(b["frequence"]))
   ops = [{"op": "add", "path": "/fields/System.Title", "value": b["titre"]},
          {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.ReproSteps", "value": repro},
          {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Severity", "value": b["gravite"]},
          {"op": "add", "path": "/fields/System.AreaPath", "value": b["area"]},
          {"op": "add", "path": "/fields/System.IterationPath", "value": b["iteration"]},
          {"op": "add", "path": "/fields/System.Tags", "value": "QC-agent; US-" + str(b["us"])}]
   json.dump(ops, sys.stdout, ensure_ascii=False)
   EOF
   ```
   Le champ `bug.json` contient : `titre`, `environnement`, `preconditions`, `etapes`, `obtenu`, `attendu`, `frequence`, `gravite` (ex. « 2 - High »), `area`, `iteration` (ceux de l'US), `us`.
2. Créer : `POST <url>/<projet ADO>/_apis/wit/workitems/$Bug?api-version=7.1`, `Content-Type: application/json-patch+json`, `--data-binary @.qc-agent/bug-patch.json`. Si le modèle de processus refuse un champ (400), le signaler et réessayer une fois sans ce champ.
3. Lier le bug à l'US (et au cas de test s'il est connu) avec une relation `System.LinkTypes.Related`, un appel par lien.
4. Relire le bug créé et vérifier le titre et les liens.

## 7. Compte rendu

Id et titre du bug, liens créés, et rappel : « Ajoute ta capture masquée en pièce jointe. »
