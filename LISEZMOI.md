# Agents QA

Cinq agents, un fichier chacun, sans skill ni script. Chaque agent ne contient que sa méthode et ne lit que les fichiers dont il a besoin.

| Agent | Demande | Lit | Écrit |
|---|---|---|---|
| `qa-0-contexte` | `init`, `maj <id>`, `maj sprint-<n>`, `po "<réponse>" (auteur, date)` | Le rapport concerné, puis seulement les fichiers de contexte touchés | `qa/contexte/`, après « oui » |
| `qa-1-coherence-sprint` | `<id> <id> … sprint=<n>` | `socle.md`, `regles-et-points.md`, les US du sprint | `qa/rapports/sprint-<n>-coherence.md` et un `US-<id>-ecarts.md` par US |
| `qa-2-analyse-us` | `<id>`, ou l'id suivi du texte de l'US | `socle.md`, `regles-et-points.md`, `US-<id>-ecarts.md`, l'US | `qa/rapports/US-<id>-analyse.md` |
| `qa-3-cas-de-test` | `<id>`, `csv <id>`, `publie <id>` | `socle.md`, l'analyse | `qa/rapports/US-<id>-cas.md`, le CSV, Test Plans après « oui » |
| `qa-4-anomalie` | `rédige <id> : <constat>`, `crée`, `doublons <mots>` | `socle.md`, l'analyse ou l'US | `qa/anomalies/`, Azure DevOps après « oui » |

Ordre d'un sprint : `qa-1-coherence-sprint`, puis pour chaque US `qa-2-analyse-us` et `qa-3-cas-de-test`, puis `qa-0-contexte` pour enrichir le contexte. Chaque étape dans un nouveau chat : ce qui passe d'une étape à l'autre passe par les fichiers de `qa/`, pas par l'historique.

## Installer

1. Copier à la racine du dépôt : `.github/agents/`, `.github/copilot-instructions.md`, `qa/`.
2. Ajouter `.qc-agent/` au `.gitignore` (fichiers de travail des écritures dans Azure DevOps).
3. Remplir `qa/contexte/` avec l'agent `qa-0-contexte` (`init`), ou y copier un contexte existant.
4. Déposer les US à analyser dans `qa/sources/US-<id>.md` si l'agent ne peut pas les lire dans Azure DevOps.

Un dépôt correspond à un projet : les chemins sont fixes, l'agent n'a rien à chercher.

## Azure DevOps

Les agents lisent une US avec `curl` et le champ `fields=` : seuls le titre, l'état, la révision, l'Area Path, l'itération, la description et les critères sont demandés. Le PAT est lu dans la variable `ADO_PAT` (secret de l'environnement `copilot` sur GitHub, variable d'environnement en local). Sous Windows, les agents utilisent `curl.exe` et `$env:ADO_PAT`.

| Pour | Droits du PAT |
|---|---|
| Analyser, rédiger, cohérence | Work Items, lecture |
| Publier les cas | Work Items lecture et écriture, Test Management lecture et écriture |
| Créer un bug | Work Items lecture et écriture |

Aucune écriture sans aperçu et « oui ». Sur GitHub, ces règles sont des consignes : le verrou technique est le droit du PAT.

## Consommer peu de crédits

| Règle | Pourquoi |
|---|---|
| Choisir l'agent de l'étape, pas l'agent par défaut | L'agent par défaut envoie la description de tous les outils et serveurs MCP installés à chaque message |
| Un modèle standard, pas « Auto » ni le plus puissant | Le prix au token change beaucoup d'un modèle à l'autre |
| Un nouveau chat par étape | Un chat qui s'allonge renvoie tout son historique à chaque message |
| La demande complète en un seul message | Un message sans demande appelle une réponse, puis un deuxième envoi de tout l'historique |
| Donner le numéro de l'US plutôt que la coller, si elle est dans `qa/sources/` ou lisible dans Azure DevOps | Un texte collé est renvoyé à chaque message du chat |
| Supprimer les anciennes versions (`.github/skills/`, `.github/qc/`, ancien `qc.agent.md`) | Copilot annonce tous les skills du dépôt à chaque message, et deux agents du même nom se confondent |
