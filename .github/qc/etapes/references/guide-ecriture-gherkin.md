# Guide d'écriture Gherkin : exemples

Ce guide montre les règles du skill `gherkin-test-generation` sur des exemples. Les règles elles-mêmes sont dans le skill ; ici, seulement des cas bons et mauvais. Toutes les données sont fictives.

## 1. Écrire en français, avec toutes les préconditions

Mauvais : en anglais, et une ligne par mot-clé sans rien de concret.

```gherkin
Scenario: Create a request
  Given an active user
  When he creates a request
  Then the request is created
```

Bon : on sait qui est connecté, où, avec quelles données, ce qu'il fait et ce qu'on vérifie.

```gherkin
Scénario: Un Admin crée une demande de nouveau mandat
  Étant donné que l'utilisateur "ADM-TEST-01" est connecté avec le rôle "Admin"
  Et qu'il est sur la page "Liste des demandes"
  Et que l'entité "ENT-TEST-01" existe dans le référentiel
  Quand il clique sur "Nouvelle demande"
  Et qu'il choisit la nature "Nouveau"
  Et qu'il sélectionne l'entité "ENT-TEST-01"
  Et qu'il renseigne la référence "REF-TEST-01" et la reprise "Non"
  Et qu'il valide la création
  Alors une demande pour l'entité "ENT-TEST-01" apparaît dans la "Liste des demandes"
  Et le panneau de création est fermé
```

Le dernier « Alors » ne dit que ce que l'US décrit. Si l'US ne donne pas le statut de la nouvelle demande, on ne l'invente pas : on pose la question.

## 2. Le Contexte pour ce qui est commun à tous les scénarios

```gherkin
Fonctionnalité: Créer une demande

  Contexte:
    Étant donné que l'utilisateur "ADM-TEST-01" est connecté avec le rôle "Admin"
    Et qu'il est sur la page "Liste des demandes"

  Scénario: Le panneau de création s'ouvre à droite de la liste
    Quand il clique sur "Nouvelle demande"
    Alors un panneau de création s'affiche à droite de l'écran
    Et la "Liste des demandes" reste visible en arrière-plan
```

Mauvais : mettre dans le Contexte une donnée qui ne sert qu'à un seul scénario.

## 3. Une précondition est un état, pas une suite de clics

Mauvais :

```gherkin
Étant donné que je crée une demande
Et que je la soumets
```

Bon :

```gherkin
Étant donné que la demande "DEM-TEST-03" existe au statut "Soumise"
```

## 4. Plusieurs actions, un seul comportement

Les `Et` après `Quand` enchaînent les actions d'un même parcours. Mais si l'on veut vérifier deux choses à deux moments, ce sont deux scénarios.

Mauvais : on vérifie l'ouverture du formulaire ET la création dans le même scénario.

```gherkin
Quand il clique sur "Nouvelle demande"
Alors le panneau de création s'affiche
Quand il valide la création
Alors la demande est créée
```

Bon : un scénario pour l'ouverture (exemple du point 2), un autre pour la création (exemple du point 1).

## 5. Un résultat exact, jamais vague

| Mauvais | Bon |
|---|---|
| Alors la demande est correctement validée | Alors la demande "DEM-TEST-03" est au statut "Validée" |
| Alors un message d'erreur s'affiche | Alors le message "entité inconnue" s'affiche sous le champ "Entité" |
| Alors le millésime est présélectionné | Alors le champ "Millésime" affiche l'année fiscale en cours |

## 6. Jamais d'alternative

Mauvais :

```gherkin
Alors la réponse est "403 ou 404"
Alors l'utilisateur est redirigé ou un message s'affiche
```

Si la source dit seulement que l'accès est refusé :

```gherkin
Alors l'accès à la page "Administration" est refusé
```

et la forme exacte du refus devient une question au PO.

## 7. Un refus vérifie aussi que rien n'a changé

```gherkin
Scénario: Une entité inconnue bloque la création
  Étant donné que l'utilisateur "ADM-TEST-01" est connecté avec le rôle "Admin"
  Et que le panneau de création est ouvert avec la nature "Nouveau"
  Et que l'entité "ENT-INCONNUE-99" n'existe pas dans le référentiel
  Quand il renseigne tous les champs obligatoires avec l'entité "ENT-INCONNUE-99"
  Et qu'il valide la création
  Alors le champ "Entité" est surligné en rouge
  Et le message "entité inconnue" s'affiche sous le champ
  Et aucune demande pour l'entité "ENT-INCONNUE-99" n'apparaît dans la "Liste des demandes"
```

## 8. Un rôle non autorisé

```gherkin
Scénario: Un User ne voit pas le bouton de création
  Étant donné que l'utilisateur "USR-TEST-01" est connecté avec le rôle "User"
  Quand il ouvre la page "Liste des demandes"
  Alors la liste des demandes s'affiche
  Mais le bouton "Nouvelle demande" n'est pas affiché
```

## 9. Valeurs limites

Si la source dit « de l'année en cours moins 20 ans à plus 10 ans » :

```gherkin
Plan du scénario: Les bornes du millésime proposées à la création
  Étant donné que l'utilisateur "ADM-TEST-01" est connecté avec le rôle "Admin"
  Et que le panneau de création est ouvert avec la nature "Renouvellement"
  Quand il ouvre la liste du champ "Millésime"
  Alors le millésime "<millesime>" est <presence> dans la liste

  Exemples:
    | cas                  | millesime                    | presence |
    | borne basse          | année en cours moins 20 ans  | proposé  |
    | juste avant la borne | année en cours moins 21 ans  | absent   |
    | borne haute          | année en cours plus 10 ans   | proposé  |
    | juste après la borne | année en cours plus 11 ans   | absent   |
```

Les lignes « juste avant » et « juste après » ne sont écrites que si l'US dit ce qui se passe au-delà. Ici, l'US définit le contenu de la liste : ce qui est hors de la plage n'y est pas proposé.

## 10. Filtrage mixte

Une règle « l'auditeur voit uniquement ses demandes » se teste avec une demande autorisée et une demande interdite dans le même scénario :

```gherkin
Scénario: Un auditeur ne voit que les demandes dont il est contact
  Étant donné que l'utilisateur "AUD-TEST-01" est connecté avec le rôle "Auditeur"
  Et que "AUD-TEST-01" est contact de la demande "DEM-TEST-01"
  Et que "AUD-TEST-01" n'est pas contact de la demande "DEM-TEST-02"
  Quand il ouvre la page "Mes demandes"
  Alors la demande "DEM-TEST-01" est affichée
  Et la demande "DEM-TEST-02" n'est pas affichée
```

## 11. Dates relatives

| Mauvais | Bon |
|---|---|
| la demande créée le 15/08/2026 | la demande "DEM-TEST-05" créée il y a 61 jours |
| le millésime 2026 | le millésime de l'année fiscale en cours |

Une date fixe fait changer le résultat du cas avec le temps.

## 12. Pas de doublon

Reprise « Oui » et Reprise « Non » mènent au même résultat de création : un seul scénario suffit. Un deuxième ne se justifie que si l'US décrit un résultat différent.

## 13. Du Gherkin au cas manuel

Le scénario du point 7 devient :

| Pas | Action | Résultat attendu |
|---|---|---|
| 1 | Préconditions : connecté avec "ADM-TEST-01" (Admin) ; panneau de création ouvert, nature "Nouveau" ; l'entité "ENT-INCONNUE-99" n'existe pas | |
| 2 | Renseigner tous les champs obligatoires avec l'entité "ENT-INCONNUE-99" | |
| 3 | Valider la création | Le champ "Entité" est surligné en rouge. Le message "entité inconnue" s'affiche sous le champ. Aucune demande pour "ENT-INCONNUE-99" n'apparaît dans la liste |

## 14. Récupération après un refus

Seulement si la source dit que l'utilisateur peut corriger et recommencer. Le blocage et la récupération sont deux scénarios : la récupération part de l'état d'erreur.

Bon :

```gherkin
Scénario: Une demande refusée pour un champ vide est créée une fois le champ rempli
  Étant donné que l'utilisateur "ADM-TEST-01" est connecté avec le rôle "Admin"
  Et que le formulaire de création affiche le champ "N° Requête BSC" en erreur après une première validation
  Quand il renseigne le N° Requête BSC "BSC-TEST-01"
  Et qu'il clique sur "Valider la création"
  Alors une nouvelle demande est créée
  Et le champ "N° Requête BSC" n'est plus en erreur
```

Mauvais : enchaîner le refus puis la correction dans un seul scénario (deux comportements, deux Quand), ou écrire une récupération que la source ne décrit pas.

## 15. Type de test et tableau Azure DevOps

Un scénario d'interface porte une ligne de commentaire sous son titre :

```gherkin
Scénario: Le titre du champ en erreur passe en rouge
  # Type : UI
  Étant donné que …
```

Le tableau `ID | Test case | Gherkin BDD scenario | Type of test` se produit avec `build_tc.py table`. Ne pas le recopier à la main : une étape oubliée ou un paramètre mal renommé ne se voient pas à la relecture d'un tableau.
