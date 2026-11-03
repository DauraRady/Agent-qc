# Agent QA pour l'onglet Agents de GitHub

## Installer (une fois, sur une branche du dépôt de l'équipe)

1. Copier à la racine du dépôt : `.github/agents/qc.agent.md` (il remplace l'actuel), `.github/skills/`, `docs/`, `qc-reports/`.
2. Ajouter `.qc-agent/` au `.gitignore`.
3. Vérifier que le secret `ADO_PAT` existe dans Settings, Environments, `copilot` (l'agent actuel l'utilise déjà). En lecture seule pour analyser ; lecture et écriture seulement pour publier.
4. Ouvrir une pull request, la faire relire, fusionner.

## Utiliser

Dans l'onglet Agents du dépôt, choisir « qc agent », puis écrire :

| Je veux | J'écris |
|---|---|
| Contrôler un sprint | `coherence-sprint 1201 1202 1203 1204 sprint=4` |
| Analyser une US | `us-analysis 1204` |
| Écrire les scénarios | `gherkin-test-generation 1204` |
| Enrichir le contexte | `maj-contexte 1204` |
| Obtenir le CSV | `publication-ado 1204 csv` |
| Publier dans Test Plans | `publication-ado 1204` |
| Rédiger un bug | `redaction-anomalie` puis ce que j'ai constaté |

L'agent fait une étape, écrit son fichier dans `qc-reports/`, s'arrête et propose la suite. Ses fichiers arrivent dans la pull request de la session : relire, puis fusionner.

## À savoir

1. Sur GitHub, aucun script ne bloque une écriture dans Azure DevOps : c'est une consigne de l'agent. Le vrai verrou est le PAT en lecture seule.
2. Premier test conseillé : `coherence-sprint` sur le sprint 4, puis comparer avec le rapport de référence `qc-reports/reference-sprint-4-coherence.md` s'il est fourni.

## Utiliser dans VS Code sans gaspiller de crédits

VS Code lit le même agent et les mêmes skills (`.github/agents`, `.github/skills`). À chaque message, Copilot renvoie au modèle tout l'historique du chat, les fichiers joints et la description des outils actifs, et il le refait à chaque action de l'agent. Le coût dépend donc surtout de ces règles d'usage :

| Règle | Pourquoi |
|---|---|
| Choisir « qc agent » dans la liste des agents, pas l'agent par défaut | « qc agent » n'a que trois outils (lire, modifier, lancer une commande). L'agent par défaut envoie aussi la description de tous les outils et serveurs MCP installés |
| Choisir un modèle standard | Le prix au token change beaucoup d'un modèle à l'autre ; le plus puissant n'est pas nécessaire pour ces étapes |
| Un nouveau chat par étape | Un chat qui s'allonge renvoie tout son historique à chaque message |
| Écrire la demande complète en un seul message (`us-analysis 1201`) | Un message sans demande appelle une réponse, puis un deuxième envoi de tout l'historique |
| Ne pas coller l'US : donner son numéro | Le texte collé est renvoyé à chaque message. Sans accès à Azure DevOps, déposer l'US une fois dans `docs/projets/<projet>/sources/US-<id>.md` |
| Fermer les gros fichiers avant d'écrire, retirer les pièces jointes proposées | Le fichier ouvert est souvent joint automatiquement au message |

Pour mesurer : noter les crédits Copilot avant et après une étape, dans les paramètres du compte GitHub.
