# Rédaction des scénarios Gherkin

Lire `.github/qc/etapes/references/guide-ecriture-gherkin.md` à la première utilisation de la session : il contient les exemples bons et mauvais.

## Point de départ

1. Partir de l'analyse écrite dans `qc-reports/US-<id>.md` : règles, préconditions, combinaisons, verdict. Ne pas refaire l'analyse et ne pas relire l'US : l'analyse contient ses citations. Rouvrir l'US avec `lire_us.py` seulement pour vérifier une citation douteuse. Du contexte, charger seulement `python3 .github/qc/outils/contexte.py docs/projets/<projet>/CONTEXTE.md gherkin` (rôles, comptes, écrans, données, synonymes). Les scénarios s'ajoutent à la suite, dans le même fichier.
2. S'il n'y a pas d'analyse, appliquer d'abord `us-analysis`.
3. Verdict « Non prête » : ne rédiger aucun scénario, renvoyer aux questions.
4. Ne rédiger des scénarios que pour les règles Rédigeables. Une règle À arbitrer ou Exploratoire n'a jamais de scénario.

## La langue : Gherkin en français, toujours

Jamais `Given`, `When`, `Then`, `And`, `Feature`, `Scenario`.

| Mot-clé | Sert à |
|---|---|
| `Fonctionnalité:` | La fonction de l'US, une seule fois |
| `Contexte:` | Les préconditions communes à TOUS les scénarios du bloc |
| `Scénario:` | Un comportement et son résultat |
| `Plan du scénario:` et `Exemples:` | Le même scénario rejoué avec des valeurs différentes |
| `Étant donné que` | Première précondition |
| `Et que` | Préconditions suivantes |
| `Quand` | Première action de l'utilisateur |
| `Et` (après Quand) | Actions suivantes du même parcours |
| `Alors` | Premier résultat observable |
| `Et` (après Alors) | Résultats suivants |
| `Mais` | Résultat négatif qui complète un Alors (« Mais le bouton "Valider" n'est pas affiché ») |

## Structure d'un scénario

### 1. Étant donné : TOUT ce qui doit être vrai avant d'agir

Écrire une précondition par ligne, dans cet ordre :

1. Qui est connecté : rôle et compte fictif. Le rôle vient du « En tant que » de l'US ou du contexte projet (section 4, Connexion et comptes de test). « l'utilisateur "ADM-TEST-01" est connecté avec le rôle "Admin" ».
2. Où il se trouve : l'écran de départ. « il est sur la page "Liste des demandes" ».
3. Ce qui existe déjà : chaque donnée qui influence le résultat, avec un identifiant fictif et la valeur qui compte. « la demande "DEM-TEST-03" est au statut "Soumise" ».
4. Les réglages ou états particuliers nécessaires au cas.

Une précondition décrit un état, pas des clics : « la demande "DEM-TEST-03" existe au statut "Soumise" », pas « je crée une demande puis je la soumets ».

Si un état est commun à tous les scénarios (même rôle, même écran), il va dans le `Contexte`, une seule fois.

Si on ne sait pas avec quel rôle agir, ou quelle donnée préparer, la règle n'est pas Rédigeable : elle redevient une question.

### 2. Quand : les actions de l'utilisateur

1. `Quand` porte la première action, chaque `Et` qui suit porte l'action suivante du même parcours : choisir une valeur, remplir un champ, cliquer.
2. Les actions décrivent ce que fait l'utilisateur, jamais une vérification.
3. Un scénario teste un seul comportement. Si deux résultats indépendants sont à vérifier à deux moments différents (ouvrir le formulaire, puis créer la demande), ce sont deux scénarios. L'état atteint par le premier devient une précondition du second.

### 3. Alors : chaque résultat observable

1. Un résultat par ligne : `Alors`, puis `Et`.
2. Chaque résultat se vérifie sans interprétation : statut exact, valeur exacte, message copié mot pour mot de la source, élément présent ou absent, champ en erreur. Si la source annonce un message sans en donner le texte, écrire « un message d'erreur s'affiche » (ou « de confirmation ») et laisser la question du texte ouverte : le scénario reste rédigé.
3. Interdits hors guillemets : correctement, normalement, comme prévu, fonctionne, est OK, avec succès (sans préciser le résultat), bien.
4. Jamais d'alternative : pas de « 403 ou 404 », pas de « est redirigé ou un message s'affiche ». Si la source ne tranche pas, garder seulement ce qu'elle dit (« la création est refusée ») et poser la question.
5. Un refus vérifie deux choses : le refus (message, champ en erreur) ET la donnée inchangée (« aucune nouvelle demande n'apparaît dans la liste », « la demande "DEM-TEST-03" est toujours au statut "Soumise" »).

## Quels scénarios écrire

| Famille | Quand l'écrire |
|---|---|
| Nominal | Chaque règle Rédigeable a au moins un scénario nominal |
| Négatif | Seulement si la source décrit un refus, une interdiction, une erreur ou une exclusion. Ne jamais supposer qu'une valeur non citée est invalide |
| Limite | Dès qu'une règle Rédigeable contient un nombre, une date, une durée ou un plafond : la borne, et la valeur juste au-delà si le comportement au-delà est écrit |
| Variante | Chaque combinaison Rédigeable de l'analyse dont le résultat diffère (rôle, type d'objet, nature) |
| Filtrage mixte | Règle avec « uniquement », « seulement », « exclut » : un objet autorisé et un objet non autorisé dans le même scénario |
| Récupération | Seulement si la source dit que l'utilisateur peut corriger et recommencer après un refus. Scénario séparé du blocage : il part de l'état d'erreur (Étant donné), l'utilisateur corrige (Quand), l'action aboutit (Alors). Sinon, c'est une idée exploratoire |

Technique à choisir selon la forme de la règle :

| Forme de la règle | Technique | Ce qu'on écrit |
|---|---|---|
| Catégories de valeurs | Partitions d'équivalence | Une valeur par catégorie décrite |
| Minimum, maximum, date limite | Valeurs limites | La borne et sa voisine dont le comportement est écrit |
| Conditions combinées | Table de décision | Une ligne par combinaison décrite |
| Statuts | Transitions d'état | Les transitions autorisées et les refus décrits |
| Droits | Matrice rôle × action | Les rôles cités et leur résultat |

Rôles et catégories de données : quand plusieurs rôles ou catégories mènent à des résultats différents par les mêmes étapes, un Plan du scénario avec une ligne d'Exemples par rôle ou catégorie, plutôt que des scénarios recopiés.

Type de test : sous le titre d'un scénario qui n'est pas fonctionnel, une ligne de commentaire `# Type : UI` (ou API, Sécurité, Performance, Accessibilité, UAT). Sans cette ligne, le type est Fonctionnel. Le type ne change ni la rédaction ni la publication : tous les cas retenus sont publiés.

Pas de doublon : un scénario par résultat attendu distinct. Deux valeurs qui mènent au même résultat sont le même scénario. Une valeur qui ne change pas le comportement décrit ne justifie pas un scénario.

## Données

1. Identifiants fictifs reconnaissables : `ADM-TEST-01`, `DEM-TEST-03`, `ENT-TEST-01`. Reprendre d'abord ceux du contexte projet (sections 4 et 8). Tout identifiant nouveau devient une proposition pour le contexte, pour que les US suivantes réutilisent les mêmes données.
2. Chaque scénario a ses propres données : aucun scénario ne dépend d'un autre.
3. Dates relatives (« créée il y a 61 jours », « l'année fiscale en cours ») plutôt que des dates fixes qui changeraient le résultat avec le temps.
4. Le même fait s'écrit avec la même phrase dans tous les scénarios.

## Plan du scénario

Seulement si les étapes sont identiques, que la règle est la même et que chaque ligne d'`Exemples` est une catégorie, une limite ou une combinaison différente. Première colonne `cas` : pourquoi la ligne existe. Une seule ligne utile : un `Scénario` simple.

## Cas manuel pour Azure Test Plans

Si le format manuel est demandé, chaque scénario devient un cas :

| Gherkin | Cas manuel |
|---|---|
| `Scénario:` | Titre |
| `Contexte` + `Étant donné` + `Et que` | Prérequis, et pas 1 (action : les préconditions, résultat attendu vide) |
| `Quand` et chaque `Et` d'action | Un pas par action |
| `Alors` et ses `Et` | Résultat attendu du dernier pas d'action |
| `Exemples` | Paramètres |

Objectif du cas : uniquement s'il apporte une information que le titre ne donne pas (la règle vérifiée ou l'erreur que le cas détecterait). Aucun prérequis n'est ajouté pendant la transformation : ils viennent tous du Gherkin.

## Tableau pour Azure DevOps

Le tableau `ID | Test case | Gherkin BDD scenario | Type of test` n'est jamais écrit à la main : il est produit par le script, à partir des blocs Gherkin relus.

```bash
python3 .github/qc/outils/build_tc.py table qc-reports/US-<id>.md --out qc-reports/US-<id>-ado.md
```

Ce que fait le script :

1. Une ligne par scénario, numérotée TC-001, TC-002…
2. Les étapes séparées par `<br>`, dans l'ordre Étant donné, Quand, Alors.
3. Les préconditions du `Contexte` répétées dans chaque cas, puisque Azure DevOps ne connaît pas le `Contexte`. Dans le Gherkin, elles restent écrites une seule fois.
4. Les paramètres `<role>` deviennent `@role`, avec un tableau des valeurs sous le tableau principal, un par cas paramétré.
5. Le type vient de la ligne `# Type : …`, sinon Fonctionnel.

## Format de sortie

```
## 1. Scénarios
Un bloc gherkin par fonctionnalité, en français.

## 2. Couverture
| Critère | Scénarios | Couvert ? |
Couvert, partiel ou non couvert, avec la raison (renvoi à la question de l'analyse).

## 3. Non rédigé
Les règles À arbitrer et Exploratoires de l'analyse, en une ligne chacune, avec le renvoi à la question. Ne pas les réécrire.

## 4. Propositions pour le contexte
| # | Proposition (une ligne) | Section du contexte | Type | Source |
Ce que la rédaction a fait apparaître et qui servira aux US suivantes : comptes de test par rôle (section 4), données fictives et leur état (section 8), écran ou terme précisé (sections 5 et 7). Rien n'est écrit dans le contexte : /maj-contexte le fera après validation.
```

Puis produire le tableau Azure DevOps avec le script (section Tableau pour Azure DevOps) et terminer en rappelant : « Pour enrichir le contexte : /maj-contexte <id> ».

## Contrôle sans IA

Lancer le script de ce skill sur le rapport avant de livrer (`python` si `python3` n'existe pas) :

```bash
python3 .github/qc/outils/build_tc.py check qc-reports/US-<id>.md
```

Il refuse les mots-clés anglais, un deuxième `Quand`, un `Quand` après `Alors`, un scénario sans précondition, sans action ou sans résultat, un résultat vague ou avec « ou », un paramètre absent des `Exemples`, les titres en double. Il signale un type de test inconnu. Corriger chaque erreur et relancer jusqu'à zéro. Si la commande demande une autorisation, la demander à l'utilisateur : ne jamais livrer sans ce contrôle.

## Avant de livrer

1. Tous les mots-clés sont en français.
2. Chaque scénario dit qui est connecté, sur quel écran, avec quelles données.
3. Les Étant donné décrivent des états, les Quand des actions, les Alors des résultats exacts.
4. Aucun résultat avec « ou », aucun mot vague.
5. Chaque refus vérifie la donnée inchangée.
6. Aucun scénario pour une règle À arbitrer ou Exploratoire.
7. Aucun doublon de résultat.
8. Aucun message, statut, code, écran ou champ absent des sources.
9. Un scénario de récupération n'existe que si la source dit que l'utilisateur peut corriger et recommencer.
10. Les nouveaux comptes et données de test sont dans les propositions pour le contexte.
11. Le tableau Azure DevOps vient du script, pas d'une saisie à la main.
