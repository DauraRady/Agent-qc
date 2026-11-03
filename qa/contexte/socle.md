# Contexte projet : [NOM DU PROJET] : socle

Socle : Azure DevOps, projet, rôles, comptes de test, objets, statuts, termes, écrans, données de test. Lu par tous les agents.

Fichier lu par l'agent QA avant chaque analyse d'US. Il donne la configuration Azure DevOps, le vocabulaire, les rôles, les statuts, les règles déjà validées et les données de test du projet, pour que chaque US ne soit pas analysée isolément.

| En-tête | Valeur |
|---|---|
| Dernière mise à jour | [date] |
| Responsable | [nom ou rôle] |
| Version | [version] |

Règles de tenue du fichier :

1. Une ligne n'entre ici que si elle a une source (US, décision du PO datée, PRD, maquette citée). Sans source, elle va en section 9.
2. Seul l'agent `qa-0-contexte` écrit dans ces fichiers (création, ou mise à jour après aperçu et « oui »). Un humain relit les différences avant chaque commit.
3. Une règle remplacée n'est pas supprimée : son statut passe à `remplacée` et la colonne « Remplacée par » est remplie.
4. Ce fichier ne remplace jamais l'US en cours : il la complète.
5. C'est une synthèse : une ligne par règle, pas de paragraphe recopié des sources.

## 0. Azure DevOps du projet

| Clé | Valeur |
|---|---|
| URL de l'organisation | [https://<organisation>.visualstudio.com ou https://dev.azure.com/<organisation>] |
| Projet Azure DevOps | [nom] |
| Plan de test par défaut | [id] |
| Area Path par défaut | [chemin] |
| Environnements de recette | [ex. ITG, PREPROD] |

## 1. Le projet en cinq lignes

| Question | Réponse |
|---|---|
| Ce que fait l'application | |
| Qui l'utilise | |
| Ce qu'elle remplace | |
| Systèmes connectés | |
| Mise en production | |

## 3. Rôles et droits

| Rôle | Peut faire | Ne peut pas faire | Source | Statut |
|---|---|---|---|---|
| [rôle] | [actions] | [interdictions] | [source] | confirmé / à confirmer / remplacé |

## 4. Connexion et comptes de test

C'est ici que l'agent trouve comment écrire la précondition « connecté avec le rôle … ».

| Compte fictif | Rôle | Environnement | Particularité | Usage |
|---|---|---|---|---|
| USR-TEST-01 | [rôle] | [ITG, PREPROD] | [ex. affecté à aucune demande] | [ex. cas nominaux] |

Écran d'arrivée après connexion : [écran]

## 5. Objets métier, statuts et transitions

### Objets

| Objet | Définition | Variantes | Source | Statut |
|---|---|---|---|---|
| [objet] | | [ex. Nouveau, Renouvellement] | | |

### Termes et synonymes

Le même objet porte souvent plusieurs noms selon les US. L'agent traite ces termes comme un seul, et signale tout écart de sens.

| Terme retenu | Autres formes dans les sources | Sources |
|---|---|---|
| | | |

### Statuts

| Objet | Statut affiché | Signification | Source | Statut |
|---|---|---|---|---|
| | | | | |

### Transitions

| Objet | Statut de départ | Action | Statut d'arrivée | Rôle autorisé | Source | Statut |
|---|---|---|---|---|---|---|
| | | | | | | |

## 7. Écrans

| Écran | Comment on y accède | Ce qu'il affiche | Actions possibles | Source |
|---|---|---|---|---|
| | | | | |

Ne pas déduire l'existence d'un export, d'une recherche, d'une API ou d'une pièce jointe qui n'est pas citée par une source.

## 8. Données de test

Toutes les données sont fictives. Elles ne créent aucune règle métier.

| ID fictif | Objet | État | Particularité utile aux tests |
|---|---|---|---|
| DEM-TEST-01 | [objet] | [statut] | [ex. créée il y a 61 jours] |
