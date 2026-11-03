# Agents QC

Trois agents, un fichier chacun, sans skill ni script. Chaque agent ne contient que sa méthode et ne lit que les fichiers dont il a besoin.

| Agent | Rôle | Demandes | Écrit |
|---|---|---|---|
| `qc-analyse-us` | Trouver ce qui est ambigu, contradictoire, risqué ou oublié dans une US : cas limites, zones à risque, personas et cas d'usage à explorer, questions au PO | `<id>`, ou l'id suivi du texte de l'US | `qa/rapports/US-<id>-analyse.md` |
| `qc-cas-de-test` | Rédiger les cas en Gherkin français dans le tableau de l'équipe, les compléter en dialoguant, enrichir le contexte, produire le CSV, publier | `<id>`, puis `ajoute …`, `modifie TC-003 …`, `contexte`, `csv`, `publie` | `qa/rapports/US-<id>-cas.md`, `qa/contexte/` après « oui », Test Plans après « oui » |
| `qc-anomalie` | Rédiger un ticket de bug reproductible et sourcé, puis le créer | `rédige <id> : <constat>`, `crée`, `doublons <mots>` | `qa/anomalies/`, Azure DevOps après « oui » |

L'analyse est conseillée mais pas obligatoire : `qc-cas-de-test` part de l'US et du contexte, et s'appuie sur l'analyse quand elle existe.

Les agents se passent le travail par les fichiers de `qa/`, pas par l'historique du chat : une US, un chat par agent.

## Installer

1. Copier à la racine du dépôt : `.github/agents/`, `.github/copilot-instructions.md`, `qa/`.
2. Ajouter `.qc-agent/` au `.gitignore` (fichiers de travail des écritures dans Azure DevOps).
3. Remplir `qa/contexte/` : à la main à partir du modèle, ou avec `qc-cas-de-test` (demande `contexte`) à partir des documents déposés dans `qa/sources/`.
4. Déposer les US dans `qa/sources/US-<id>.md` si l'agent ne peut pas les lire dans Azure DevOps.

Un dépôt correspond à un projet : les chemins sont fixes, l'agent n'a rien à chercher.

| Fichier du contexte | Contenu | Lu par |
|---|---|---|
| `qa/contexte/socle.md` | Azure DevOps, projet, rôles, comptes de test, objets, statuts, termes, écrans, données de test | Les trois agents |
| `qa/contexte/regles-et-points.md` | Sources et US du projet, règles transverses, points à confirmer, variations, flux | Analyse, cas de test |
| `qa/contexte/journal.md` | Journal des modifications du contexte | Cas de test, à la mise à jour |

## Azure DevOps

Les agents lisent une US avec `curl` et le paramètre `fields=` : seuls le titre, l'état, la révision, l'Area Path, l'itération, la description et les critères sont demandés. Le PAT est lu dans la variable `ADO_PAT` (secret de l'environnement `copilot` sur GitHub, variable d'environnement en local). Sous Windows, les agents utilisent `curl.exe` et `$env:ADO_PAT`.

| Pour | Droits du PAT |
|---|---|
| Analyser, rédiger | Work Items, lecture |
| Publier les cas | Work Items lecture et écriture, Test Management lecture et écriture |
| Créer un bug | Work Items lecture et écriture |

Aucune écriture sans aperçu et « oui ». Sur GitHub, ces règles sont des consignes : le verrou technique est le droit du PAT.

## Consommer peu de crédits

| Règle | Pourquoi |
|---|---|
| Choisir l'agent dans la liste, pas l'agent par défaut | L'agent par défaut envoie la description de tous les outils et serveurs MCP installés à chaque message |
| Un modèle standard, pas « Auto » ni le plus puissant | Le prix au token change beaucoup d'un modèle à l'autre |
| Un nouveau chat par US et par agent | Un chat qui s'allonge renvoie tout son historique à chaque message |
| La demande complète en un seul message | Un message sans demande appelle une réponse, puis un deuxième envoi de tout l'historique |
| Donner le numéro de l'US plutôt que la coller, si elle est dans `qa/sources/` ou lisible dans Azure DevOps | Un texte collé est renvoyé à chaque message du chat |
| Supprimer les anciennes versions (`.github/skills/`, `.github/qc/`, `qc.agent.md`, agents `qa-0` à `qa-4`) | Copilot annonce tous les skills du dépôt à chaque message, et deux agents du même nom se confondent |
