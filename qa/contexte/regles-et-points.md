# Contexte projet : [NOM DU PROJET] : regles-et-points

Sources et US du projet, règles transverses, points à confirmer, variations, flux. Lu par l'analyse et les cas de test.

## 2. Sources

| ID | Document ou décision | Date ou version | État (à jour, partiel, historique) | Emplacement |
|---|---|---|---|---|
| SRC-01 | | | | |

US du projet connues de l'agent (une ligne par US analysée, mise à jour par `/maj-contexte`) :

| US | Titre | Sprint | Source lue (Azure DevOps révision n, ou export) | Cas de test |
|---|---|---|---|---|
| | | | | |

## 6. Règles transverses et décisions

Une seule table pour les règles qui valent pour plusieurs US et les décisions du PO.

| ID | Règle ou décision | Périmètre | Source et date | Statut | Remplacée par |
|---|---|---|---|---|---|
| RT-01 | | | | confirmée / remplacée | [ID ou vide] |

## 9. Points à confirmer et écarts

Une ligne ouverte ne produit aucun résultat attendu.

| ID | Sujet | Ce qui est connu | Question | Impact si sans réponse (règles, US, scénarios bloqués) | Bloquante ? | État (ouvert, répondu) |
|---|---|---|---|---|---|---|
| CONF-01 | | | | | oui / non | |

## 10. Variations

Ce qui change le comportement selon le pays, le rôle ou le type d'objet. Chaque variation décrite devient une combinaison à tester dans les US qu'elle touche.

| ID | Varie selon | Valeurs | Ce qui change | Source | Statut |
|---|---|---|---|---|---|
| VAR-01 | [pays, rôle, type d'objet] | [valeurs] | [champ, règle, écran] | | confirmée / à confirmer |

## 11. Flux entrants et sortants

Les échanges avec les autres systèmes. Un flux touché par une US donne une précondition (donnée reçue) ou un résultat (donnée envoyée) à vérifier.

| ID | Sens | Système | Déclencheur | Données échangées | Ce qu'on peut vérifier en test | Source | Statut |
|---|---|---|---|---|---|---|---|
| FLX-01 | entrant / sortant | [système] | [événement, planification] | [objet, champs] | [écran, statut, fichier, trace] | | confirmé / à confirmer |
