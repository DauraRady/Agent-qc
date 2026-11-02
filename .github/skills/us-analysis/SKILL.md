---
name: us-analysis
description: 'Analyse une User Story et ses critères d''acceptation avec le contexte projet, sans inventer de règle. Produit les règles avec leur source, les préconditions (rôle, données, écran), les combinaisons à tester, les questions au PO, un verdict qui dit quoi rédiger et les propositions d''ajout au contexte. À utiliser avant toute rédaction de cas de test, ou pour « analyse cette US ».'
argument-hint: '<id US> [projet=<nom>] [commentaires]'
---

# Analyse d'une User Story

Arguments : ceux donnés dans la demande (numéros d'US, options).

La sortie de ce skill est l'entrée du skill `gherkin-test-generation`. Elle s'écrit dans `qc-reports/US-<id>.md` et doit être courte : une personne doit pouvoir la relire en cinq minutes.

## Principe non négociable

Ne jamais inventer, compléter ou déduire une règle métier, une valeur, un message, un statut, un code HTTP, un seuil ou un écran.

Chaque règle reçoit un statut :

| Statut | Quand | Ce qu'on en fait |
|---|---|---|
| Rédigeable | La source dit la situation ET le résultat attendu | Des scénarios Gherkin |
| À arbitrer | La situation est pertinente mais le résultat attendu manque, est vague ou contradictoire | Une question au PO, aucun scénario |
| Exploratoire | Utile à vérifier, mais hors de ce que l'US promet | Une idée de session exploratoire, aucun scénario |

Une bonne pratique, une habitude du domaine ou une convention d'interface ne rend jamais une règle Rédigeable. Elle peut seulement faire naître une question ou une idée exploratoire.

## Étape 0 : lire les sources

1. Lire l'US avec `python3 .github/outils/lire_us.py <id> --contexte docs/projets/<projet>/CONTEXTE.md` : description, critères d'acceptation, et les commentaires quand ils sont demandés. Noter sa révision (`System.Rev`) et sa date de modification : la publication les comparera. Si Azure DevOps n'est pas joignable, lire l'export `docs/projets/<projet>/sources/US-<id>.md` s'il existe, et le dire. Un passage marqué « non lu » dans l'export n'est jamais complété : il devient une question.
2. Lire les sections du contexte utiles à l'analyse : `python3 .github/outils/contexte.py docs/projets/<projet>/CONTEXTE.md analyse` (toutes sauf la liste des sources et le journal ; section 9 sans les points répondus). Ajouter `--sections 2` seulement pour croiser avec une autre US (étape 1 bis). S'il n'existe pas, le dire en une ligne, proposer `/init-contexte` et continuer sans rien inventer pour compenser.
3. Dans `docs/projets/<projet>/sources/`, lire seulement les passages que l'US ou le contexte citent.
4. Une information donnée dans la demande (réponse du PO, texte d'une maquette) compte comme source seulement avec son auteur et sa date. Une décision du PO est de rang 2, un autre complément de rang 4.
5. Si les critères ne sont pas numérotés, les numéroter `AC-1`, `AC-2` dans l'ordre du texte.
6. Si l'US contient des données client ou personnelles réelles, le signaler et n'utiliser ensuite que des données fictives.

Priorité en cas de désaccord entre sources :

| Rang | Source | Usage |
|---|---|---|
| 1 | L'US et ses critères | Référence des tests de cette US |
| 2 | Décision explicite du PO sur cette US (commentaire daté) | Complète ou précise l'US |
| 3 | Contexte projet, règle confirmée | Complète ce que l'US ne dit pas (rôles, statuts, vocabulaire) |
| 4 | PRD, maquette citée | Complément, selon son état (à jour ou non) |

Si l'US contredit le contexte projet, les tests suivent l'US et l'écart est signalé. Si l'US se contredit elle-même, aucune source ne tranche : c'est une question.

Toujours dire d'où vient une information : une règle du contexte ne doit pas être présentée comme venant de l'US.

## Étape 1 : extraire les règles

Lire l'US phrase par phrase. Chaque phrase qui décrit un comportement devient une ligne du tableau des règles. Ne pas transformer un exemple en règle générale.

| ID | Règle (reformulation fidèle) | Source | Statut | Question si À arbitrer |
|---|---|---|---|---|
| R1 | | US §2, AC-1 | Rédigeable | |

Une règle est À arbitrer dès qu'on y trouve l'un de ces signaux :

1. Terme vague sans valeur mesurable (« rapidement », « correctement », « si besoin »).
2. Liste annoncée mais absente (« les champs suivants » sans la liste).
3. Branche « sinon » manquante : on sait ce qui se passe si la condition est vraie, pas si elle est fausse.
4. Refus ou erreur dont on ne sait même pas s'il bloque l'action.
5. Limite sans comportement au-delà de la limite.
6. Rôle ou statut cité sans être défini.
7. Calcul sans formule, unité ou arrondi.
8. Renvoi vers un document ou une US non fournis.
9. Deux phrases de l'US qui se contredisent.

Un détail manquant ne rend pas toute la règle À arbitrer. Si l'US dit ce qui se passe, la règle est Rédigeable avec ses mots, et seul le détail devient une question non bloquante :

| L'US dit | Rédigeable tel quel | Question non bloquante |
|---|---|---|
| « erreur si … » | L'action est refusée, rien n'est créé ni modifié, un message d'erreur s'affiche | Texte exact du message |
| « tous les champs sont obligatoires » et le système les vérifie à la validation | Un champ vide bloque la validation | Texte et emplacement du message |
| « par défaut sur l'année en cours », « de -20 à +10 » | La valeur par défaut et les bornes, exprimées avec les mots de l'US | Définition du terme si elle peut varier |
| « un message de confirmation apparaît (cf maquettes) » | Un message de confirmation s'affiche | Texte exact |

Une règle n'est À arbitrer que si le comportement lui-même manque ou se contredit. Une règle laissée À arbitrer alors que l'US décrit le comportement est une couverture perdue, aussi grave qu'un résultat inventé.

## Étape 1 bis : croiser avec les autres US

Pour chaque champ, écran, message ou règle de l'US :

1. Chercher dans le contexte (sections 5, 6, 7, 9) et dans les US qu'il cite ce qui en parle déjà, y compris sous un autre nom (section 5, termes et synonymes).
2. Classer l'écart éventuel : contradiction (deux règles ou deux messages pour la même chose), évolution (l'US change ce qu'une US plus ancienne décrivait), interaction (une autre US agit sur le même champ).
3. Chaque écart devient une question au PO avec les deux citations. Ne jamais trancher.
4. Si l'US reprend un point déjà ouvert en section 9 du contexte, reprendre son identifiant.
5. Lister les cas de test existants (section 2 du contexte) que l'US rend faux ou incomplets.

## Étape 2 : préconditions

Pour que les scénarios soient exécutables, relever ce qu'il faut AVANT l'action. Uniquement ce que disent l'US ou le contexte.

| Précondition | Valeur | Source |
|---|---|---|
| Rôle et compte connectés | ex. Admin, compte `ADM-TEST-01` | US « En tant que », contexte §4 |
| Écran de départ | ex. « Liste des demandes » | US §1 |
| Données existantes | ex. une entité connue `ENT-TEST-01` | US, contexte §8 |
| État des objets | ex. demande au statut « Soumise » | US |

Si l'US ne dit pas avec quel rôle on agit et que le contexte ne permet pas de le déduire, c'est une question.

## Étape 3 : combinaisons

Quand une règle dépend de plusieurs conditions (rôle, type d'objet, statut, valeur présente ou absente), lister les combinaisons :

| Conditions | Résultat attendu | Source | Statut |
|---|---|---|---|
| Admin + nature « Nouveau » | Champ Reprise affiché | US §3 | Rédigeable |

Une combinaison dont le résultat n'est écrit nulle part n'est jamais complétée par supposition : elle devient À arbitrer.

Variantes venant du contexte : si une variation (section 10 : pays, rôle, type d'objet) ou un flux (section 11) touche cette US, l'ajouter aux combinaisons avec sa source. Ne garder que les variantes dont le résultat diffère : deux valeurs qui donnent le même résultat sont un seul cas.

Dès qu'une règle dit « uniquement », « seulement », « exclut » ou « ne contient que », prévoir une combinaison avec un objet autorisé ET un objet non autorisé dans le même état de départ (filtrage mixte).

## Étape 3 bis : testabilité et données

Pour chaque règle Rédigeable, dire si elle se teste avec les données et l'environnement connus (contexte, sections 0 et 8). Sinon, une ligne :

| Règle | Ce qu'il faut | Pourquoi ce n'est pas immédiat | À demander à |
|---|---|---|---|
| R14 | Une demande au statut Retard | Statut atteint après un délai | Développeur |

Signaux typiques : statut qui dépend du temps, erreur technique à provoquer, donnée validée à injecter, valeur exclue du périmètre de recette, système externe à simuler. Une règle non testable reste Rédigeable : la difficulté est remontée, pas cachée.

## Étape 4 : limites et risques

1. Limites : pour chaque nombre, date, durée ou plafond Rédigeable, noter la borne et la valeur juste au-delà si le comportement au-delà est écrit.
2. Risques : trois au maximum, chacun rattaché à une règle R de l'US. Aucun risque générique (cache, performance, accessibilité) sans lien avec une règle de cette US.

## Étape 5 : verdict

| Verdict | Signification | Effet sur la rédaction |
|---|---|---|
| Prête | Les règles essentielles sont Rédigeables | Scénarios pour toutes les règles Rédigeables |
| Partiellement prête | Une partie est Rédigeable, le reste attend des réponses | Scénarios seulement pour les règles Rédigeables |
| Non prête | Le résultat des règles essentielles est inconnu | Aucun scénario : seulement les questions |

Le verdict porte sur le contenu de l'US, jamais sur une personne.

## Format de sortie

Six sections, toujours dans cet ordre. Une section sans contenu tient en une ligne : « Aucun ».

```
## 1. Sources
US lue, contexte projet (date de mise à jour) ou « contexte absent », autres sources.

## 2. Règles
Le tableau de l'étape 1.

## 3. Préconditions et combinaisons
Les tableaux des étapes 2 et 3, puis les limites, puis le tableau de testabilité (étape 3 bis).
Puis les écarts avec les autres US (étape 1 bis) et les cas de test existants à revoir.

## 4. Questions au PO
Une par règle À arbitrer : la règle citée, ce qui manque, la question, et « bloquante » ou « non bloquante ».
Puis, s'il y en a, les écarts avec le contexte projet et les idées exploratoires (trois au plus).

## 5. Verdict
Prête, Partiellement prête ou Non prête, en une phrase qui dit pourquoi.

## 6. Propositions pour le contexte
| # | Proposition (une ligne) | Section du contexte | Type | Source |
Type : ajout, confirmation, remplacement, point à confirmer. Rien n'est écrit dans le contexte : /maj-contexte le fera après validation.
```

## Propositions pour le contexte

Proposer seulement ce qui servira à d'autres US : un rôle, un statut, une transition, une règle transverse, un terme métier, un écran. Le détail propre à cette US reste dans le rapport.

| Peut être proposé | Ne peut pas être proposé |
|---|---|
| Une variation par pays, rôle ou type d'objet, ou un flux, écrits dans l'US | Une variation ou un flux supposés |
| Une règle Rédigeable de l'US, avec sa section et son critère | Une règle À arbitrer présentée comme une règle |
| Une question bloquante, comme point à confirmer | Une réponse supposée à cette question |
| Un écart entre l'US et le contexte, comme remplacement ou point à confirmer | Une bonne pratique, une habitude du domaine |
| Un fait déjà dans le contexte, comme confirmation | Une donnée client réelle |

## Questions au PO

Une bonne question cite la règle, dit ce qui manque, reste neutre et appelle une réponse vérifiable :

« R4 : l'US indique qu'une entité inconnue est refusée, mais aussi que l'entité ne peut pas être saisie librement. Comment l'utilisateur peut-il choisir une entité inconnue ? »

Ne pas poser une question dont la réponse est déjà dans l'US, une décision ou le contexte projet. Si l'US touche un point déjà ouvert en section 9 du contexte, reprendre ce point (`CONF-03`) au lieu d'en créer un nouveau.

## Avant de livrer

1. Chaque règle a une source.
2. Aucune règle À arbitrer n'a de résultat attendu écrit.
3. Les préconditions disent avec quel rôle on se connecte.
4. Aucun message, statut, code ou écran n'apparaît s'il n'est pas dans une source.
5. Le rapport tient en six sections.
6. Chaque proposition pour le contexte a une source et aucune n'est une hypothèse.
