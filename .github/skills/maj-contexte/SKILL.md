---
name: maj-contexte
description: 'Met à jour le contexte du projet avec ce que l''humain a validé, après aperçu et « oui » explicite. Trois entrées possibles : les propositions d''un rapport d''US, une réponse du PO avec son auteur et sa date, une nouvelle version d''une source. N''ajoute jamais une hypothèse, ne supprime jamais une ligne.'
argument-hint: '<id US> | po "<réponse>" (auteur, date) | source <fichier>'
---

# Mise à jour du contexte projet

Arguments : ceux donnés dans la demande (numéros d'US, options).

Le contexte est lu avant chaque analyse. Une erreur écrite ici se répète dans toutes les US suivantes : rien n'y entre sans source et sans validation humaine.

## 1. Identifier l'entrée

| Entrée | Ce que l'agent lit |
|---|---|
| `<id US>` | Les sections « Propositions pour le contexte » de `qc-reports/US-<id>.md` : celle de l'analyse et celle de la rédaction |
| `po "<réponse>"` avec auteur et date | La réponse, et le point de la section 9 auquel elle répond |
| `source <fichier>` | La nouvelle version dans `sources/`, comparée au contexte |
| `sprint-<n>` | La section « Propositions pour le contexte » de `qc-reports/sprint-<n>-coherence.md` |

Une réponse sans auteur ou sans date : la demander avant de continuer.

Lire ensuite `docs/projets/<projet>/CONTEXTE.md` en entier.

## 2. Classer chaque proposition

| Type | Quand | Effet |
|---|---|---|
| Ajout | Fait nouveau, écrit dans une source | Une ligne dans la bonne section, avec sa source |
| Confirmation | Le fait est déjà dans le contexte | Ajouter la source à la ligne existante |
| Remplacement | La source contredit une ligne existante et elle est plus récente : US plus récente, décision datée du PO, nouvelle version d'un document | L'ancienne ligne passe à `remplacée`, avec « Remplacée par » ; une nouvelle ligne est ajoutée |
| Réponse | Le PO répond à un point de la section 9 | Le point passe à « répondu » ; la règle entre en section 3, 5, 6 ou 7 |
| Écart | Contradiction sans source plus récente | Un point en section 9, rien d'autre ne change |
| Refus | Hypothèse, déduction, bonne pratique, question encore ouverte, détail propre à une seule US | Rien n'entre ; dire pourquoi |

Après chaque US analysée, proposer aussi sa ligne dans le tableau « US du projet » (section 2) : titre, sprint, source lue et révision, cas de test. Un nouveau nom pour un objet déjà connu va dans « Termes et synonymes » (section 5).

Ne retenir dans le contexte que ce qui servira à d'autres US : rôles, comptes et données de test, statuts, transitions, règles transverses, vocabulaire, écrans, variations (section 10), flux (section 11). Le détail d'une seule US reste dans son rapport.

## 3. Aperçu, puis validation

Afficher, sans rien écrire :

| # | Type | Section | Avant | Après | Source |
|---|---|---|---|---|---|

Puis les refus, une ligne chacun avec la raison. Puis demander : « J'applique ces <n> modifications au contexte ? ». Continuer seulement sur un « oui » explicite. L'utilisateur peut retirer des lignes : appliquer seulement celles qu'il garde.

## 4. Appliquer

1. Modifier uniquement les lignes de l'aperçu validé. Ne jamais supprimer une ligne, ne jamais reformuler une ligne non citée.
2. En-tête : date du jour, version augmentée de 0.1.
3. Journal (section 12) : date, « agent QA, validé par l'utilisateur », sections modifiées, motif (« US 1234 », « réponse PO du 22/10 »).
4. Laisser la modification dans la pull request de la session ; ne jamais fusionner.

## 5. Compte rendu

1. Nombre de lignes ajoutées, confirmées, remplacées ; points fermés et ouverts.
2. Si le fichier dépasse 400 lignes, proposer une condensation : doublons, règles remplacées depuis longtemps. Ne pas la faire sans demande.
3. « Relis les différences de CONTEXTE.md dans la pull request, puis fusionne si tout est juste. »
