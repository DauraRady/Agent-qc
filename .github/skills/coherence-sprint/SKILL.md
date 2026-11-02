---
name: coherence-sprint
description: 'Compare plusieurs US d''un sprint entre elles et avec le contexte projet (US des sprints précédents) : même champ, même règle, même message décrits différemment, champs renommés, périmètre qui change, cas de test existants à revoir, données difficiles à obtenir. Produit une carte du sprint et les questions au PO, sans rédiger de scénario. À utiliser au début d''un sprint, avant /us-analysis.'
argument-hint: '<id US> <id US> … [sprint=<n>]'
---

# Cohérence d'un sprint

Arguments : ceux donnés dans la demande (numéros d'US, options).

Une US se lit rarement seule : une US du sprint 4 peut modifier, sans le dire, ce qu'une US du sprint 1 décrivait. Ce skill cherche ces écarts avant que chaque US soit analysée. Il n'écrit aucun scénario et ne modifie pas le contexte.

## 1. Lire

1. Le contexte du projet en entier (`docs/projets/<projet>/CONTEXTE.md`), en particulier la section 2 (US connues et leurs cas de test), la section 5 (termes et synonymes), la section 6 (règles) et la section 9 (points ouverts).
2. Chaque US citée, dans Azure DevOps, ou dans `docs/projets/<projet>/sources/US-<id>.md` si Azure DevOps n'est pas joignable (le dire). Noter pour chacune la révision lue (`System.Rev`) et sa date.
3. Les US plus anciennes citées par le contexte qui touchent les mêmes champs ou écrans : seulement les passages concernés.
4. Les fichiers de cas de test cités en section 2 du contexte, s'ils existent dans le dépôt : chercher les cas qui utilisent les champs touchés. S'ils n'existent pas, le dire.

## 2. Construire la carte du sprint

Un tableau par objet touché (champ, écran, règle, message), une ligne par source :

| Objet | US | Ce que dit l'US (citation courte) | Source précise |
|---|---|---|---|
| N° engagement : contrôle d'unicité | 1101 | « déjà associé à une demande » | 1101 scénario 7 |
| N° engagement : contrôle d'unicité | 1201 | « déjà associé à un engagement validé » | 1201 étape 4 |

Repérer les objets à travers les synonymes de la section 5 du contexte.

## 3. Classer chaque écart

| Type d'écart | Exemple | Ce qu'on en fait |
|---|---|---|
| Contradiction | Deux conditions ou deux messages pour la même règle | Question au PO, bloquante pour la règle |
| Évolution | La nouvelle US change un champ ou un écran décrit par une US plus ancienne (mot « CHANGEMENT », champ ajouté ou retiré) | Question : l'ancienne US est-elle remplacée ? Lister les cas de test existants à revoir |
| Incohérence interne | Le périmètre de l'US ne correspond pas à ses règles ou à son flow | Question au PO |
| Interaction | Deux US du sprint agissent sur le même champ (sauvegarde et contrôle, persistance et affichage) | Question si l'ordre ou le résultat n'est pas écrit |
| Hors périmètre de recette | L'US ne se teste qu'avec des valeurs exclues du périmètre décidé | Question à la Test Manager ou au PO |
| Testabilité | Statut qui dépend du temps, erreur technique à provoquer, donnée à injecter | Demande de données ou de moyen de test |

Ne jamais trancher un écart : chaque ligne devient une question, avec les deux citations.

## 4. Format de sortie

Écrire `qc-reports/sprint-<n>-coherence.md` :

```
## 1. Sources
US lues, révision et date ; US anciennes consultées ; contexte (version).

## 2. Carte du sprint
Les tableaux de l'étape 2, seulement pour les objets cités par au moins deux sources.

## 3. Écarts
| # | Type | Objet | Source A | Source B | Question | Bloquante pour |

## 4. Cas de test existants à revoir
| Fichier ou cas | Pourquoi | US qui le change |

## 5. Données et moyens de test à demander
| Besoin | Pour quelle règle | À qui |

## 6. Ordre conseillé pour /us-analysis
Les US dans l'ordre où les analyser, avec la raison (dépendances).

## 7. Propositions pour le contexte
| # | Proposition (une ligne) | Section du contexte | Type | Source |
```

Puis s'arrêter : « Pour analyser la première US : /us-analysis <id>. Pour enrichir le contexte : /maj-contexte sprint-<n>. »

## Avant de livrer

1. Chaque écart cite ses deux sources, au paragraphe près.
2. Aucun écart n'est tranché.
3. Aucun scénario n'est rédigé.
4. Les synonymes du contexte ont été utilisés pour rapprocher les objets.
