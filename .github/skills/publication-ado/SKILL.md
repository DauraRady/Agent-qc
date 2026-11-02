---
name: publication-ado
description: 'Publie dans Azure Test Plans les scénarios relus d''une US (fichier qc-reports/US-<id>.md), exactement tels qu''ils sont, après aperçu et validation explicite, ou produit un CSV à importer soi-même (mode csv). Lie chaque cas à l''US, vérifie les liens, ne crée jamais de doublon ni de plan de test. À utiliser pour « publie les cas », « crée-les dans ADO », « fais-moi le CSV ».'
argument-hint: '<id US> [csv] [plan <id>] [suite <id>] [assigne <email>]'
---

# Publication des scénarios dans Azure DevOps

Arguments : ceux donnés dans la demande (numéros d'US, options).

`<url>` et `<projet ADO>` viennent de la section 0 du contexte du projet (`docs/projets/<projet>/CONTEXTE.md`).

Ce skill publie le fichier relu par un humain, tel quel. Il ne réécrit, ne complète et n'ajoute aucun scénario : si quelque chose doit changer, l'humain modifie le fichier ou relance `/gherkin-test-generation`.

## 0. Choisir le mode

| Demande | Mode | Écrit dans Azure DevOps |
|---|---|---|
| `/publication-ado <id>` | API : sections 1 à 5 | Oui, après « oui » explicite |
| `/publication-ado <id> csv`, ou PAT sans droit d'écriture | CSV : section 6 | Non |

Si une écriture répond 401 ou 403 en mode API, proposer le mode CSV au lieu de réessayer.

## 1. Construire les cas sans IA

1. Si `qc-reports/US-<id>.md` n'existe pas ou ne contient aucun bloc ```gherkin : STOP, « Rapport introuvable : lancer d'abord /us-analysis puis /gherkin-test-generation, et relire le rapport ».
2. Lire l'US avec `python3 .github/outils/lire_us.py <usId> …` pour `System.TeamProject`, `System.AreaPath`, `System.IterationPath` et `System.Rev`. Garder l'id comme `<usId>`. Si la révision est plus récente que celle notée dans le rapport, STOP : « L'US a changé depuis l'analyse (révision <a> lue, <b> actuelle) : relancer /us-analysis ou confirmer explicitement que la modification ne change pas les scénarios ».
3. Personne à qui assigner les cas : l'adresse donnée dans la demande, sinon personne (le dire).
4. Construire les corps de requête :
   ```bash
   python3 .github/skills/gherkin-test-generation/scripts/build_tc.py build qc-reports/US-<id>.md --us <usId> \
     --out .qc-agent/US-<id> --assignee "<email>" --area "<AreaPath>" --iteration "<IterationPath>"
   ```
5. Si le script signale une erreur : STOP, afficher les erreurs, ne rien publier. Ne jamais construire le XML des étapes à la main.
6. Lire `.qc-agent/US-<id>/manifest.json` : un fichier par scénario.

Ce que le script produit pour chaque scénario :

| Gherkin | Cas de test Azure DevOps |
|---|---|
| Titre du scénario | Titre du cas |
| `Contexte`, `Étant donné` et leurs `Et que` | Pas 1 : les préconditions, résultat attendu vide |
| `Quand` et chaque `Et` d'action | Un pas par action |
| `Alors` et ses `Et` | Résultat attendu du dernier pas d'action |
| `<param>` d'un Plan du scénario | `@param`, valeurs dans la grille Parameter values |
| US | Tags `QC-agent; US-<id>` |

## 2. Trouver le plan, la suite, écarter les doublons

1. Plan : `plan <id>` dans la demande, sinon le plan par défaut de la section 0 du contexte. Sans plan connu : STOP, le demander. `GET <url>/<projet ADO>/_apis/testplan/plans/<planId>?api-version=7.1`. En cas d'échec : STOP. Ne jamais créer de plan.
2. Suite : `suite <id>` dans la demande (suite statique), sinon la suite basée sur l'exigence de l'US : lister `GET <url>/<projet ADO>/_apis/testplan/Plans/<planId>/suites?api-version=7.1` et chercher `suiteType` = `requirementTestSuite` avec `requirementId` = `<usId>`. Si elle n'existe pas, elle sera créée sous la suite racine du plan.
3. Doublons : la section « Liens » de `lire_us.py` donne les cas déjà liés (lignes « Tested By »). Lire leurs titres en un seul appel : `curl -sS -w '\n%{http_code}' -u ":$ADO_PAT" "<url>/<projet ADO>/_apis/wit/workitems?ids=<id1>,<id2>&fields=System.Title&api-version=7.1"`. Un scénario dont le titre existe déjà n'est pas recréé : « déjà publié : <id> ».

## 3. Aperçu, puis validation

Afficher, sans rien écrire : le plan et la suite (existante ou à créer), la liste des cas à créer (titre), les cas déjà publiés, la personne assignée. Puis demander : « Je crée ces <n> cas dans Azure DevOps ? ». Continuer seulement sur un « oui » explicite.

## 4. Créer, lier, vérifier

1. Créer la suite si besoin, corps dans un fichier :
   `{"suiteType":"requirementTestSuite","name":"<usId> : <titre>","requirementId":<usId>,"parentSuite":{"id":<rootSuiteId>}}`
   envoyé en POST sur `<url>/<projet ADO>/_apis/testplan/Plans/<planId>/suites?api-version=7.1`.
2. Pour chaque cas :
   ```bash
   curl -sS -w '\n%{http_code}' -u ":$ADO_PAT" -H "Content-Type: application/json-patch+json" \
     --data-binary @.qc-agent/US-<id>/tc-01.json \
     "<url>/<projet ADO>/_apis/wit/workitems/\$Test%20Case?api-version=7.1"
   ```
   Erreur 400 sur l'assigné, la zone ou l'itération : reconstruire sans l'option concernée et réessayer une fois. Le signaler.
3. Lier chaque cas à l'US, un appel par cas :
   ```bash
   curl -sS -X PATCH -w '\n%{http_code}' -u ":$ADO_PAT" -H "Content-Type: application/json-patch+json" \
     -d '[{"op":"add","path":"/relations/-","value":{"rel":"Microsoft.VSTS.Common.TestedBy-Reverse","url":"<url>/_apis/wit/workItems/<usId>","attributes":{"comment":"Cree par QC agent"}}}]' \
     "<url>/<projet ADO>/_apis/wit/workitems/<testCaseId>?api-version=7.1"
   ```
4. Relancer `lire_us.py <usId>` et vérifier dans « Liens » une ligne « Tested By » pour chaque cas créé. Lien manquant : relancer une fois ; sinon « Lien TC <id> -> US <usId> non créé : HTTP <code> ».
5. Suite statique : ajouter les cas avec `POST <url>/<projet ADO>/_apis/testplan/Plans/<planId>/Suites/<suiteId>/TestCase?api-version=7.1`, corps `[{"workItem":{"id":<id>}}]` dans un fichier.
6. Cas paramétré : demander à l'utilisateur d'ouvrir ce cas une fois pour vérifier la grille des paramètres.

## 5. Compte rendu

1. Plan et suite (nom, id, créée ou existante).
2. Tableau des cas créés : id, titre, lien.
3. Cas non publiés : déjà publiés, en échec avec le code HTTP.
4. Dernière ligne : « Publication terminée dans Azure DevOps. » seulement si tous les cas créés sont liés. Sinon : « Publication partielle : voir les erreurs ci-dessus. »

## 6. Mode CSV (aucune écriture par l'API)

1. Mêmes étapes 1 et 2 de la section 1. Sans accès en lecture, demander l'Area Path à l'utilisateur.
2. Construire le fichier :
   ```bash
   python3 .github/skills/gherkin-test-generation/scripts/build_tc.py csv qc-reports/US-<id>.md --us <usId> \
     --out qc-reports/US-<id>-import.csv --area "<AreaPath>" --assignee "<email>"
   ```
   Erreur du script : STOP, afficher les erreurs.
3. Un Plan du scénario devient un cas par ligne d'Exemples (l'import CSV ne gère pas les paramètres). Titre limité à 128 caractères.
4. Compte rendu, puis STOP :
   1. Chemin du fichier et nombre de cas.
   2. Import : Test Plans, plan, suite de l'US, « Import test cases from CSV », vérifier la correspondance des colonnes, Import.
   3. Importer dans la suite basée sur l'exigence de l'US relie les cas à l'US ; dans une suite statique, faire le lien à la main. À vérifier au premier import.
   4. Réimporter un cas avec son ID remplace tous ses pas : corriger dans Azure DevOps, pas en réimportant.
