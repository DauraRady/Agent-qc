# Création du contexte projet

Ce skill crée le contexte. Il ne le met jamais à jour : pour cela, `/maj-contexte`.

## 1. Vérifier le point de départ

1. Projet : le nom donné en argument. Sans nom, le demander.
2. Si `docs/projets/<projet>/CONTEXTE.md` existe déjà : STOP, « Le contexte existe. Pour le compléter : /maj-contexte ».
3. Lister `docs/projets/<projet>/sources/`. Pour chaque fichier : nom, version ou date si elle est écrite, nombre de pages ou de lignes.
4. Sans source : STOP, « Déposer les documents dans docs/projets/<projet>/sources/ (voir docs/projets/_modele/sources/LISEZMOI.md) ».
5. Un `.docx` non converti : le signaler et proposer la commande `pandoc`. Ne pas le lire à moitié.

## 2. Lire et extraire

Lire chaque source en entier, chapitre par chapitre. Ne retenir que ce qui sert à tester plusieurs US :

| Section du contexte | Ce qu'on y met | Ce qu'on n'y met pas |
|---|---|---|
| 1. Le projet | Cinq réponses courtes | L'historique du projet |
| 2. Sources | Un identifiant `SRC-01` par document, sa version, son état | Le contenu des documents |
| 3. Rôles et droits | Rôles cités et ce qu'ils peuvent ou non faire | Un droit déduit d'un intitulé de rôle |
| 5. Objets, statuts, transitions | Vocabulaire, statuts affichés, transitions écrites | Une transition supposée |
| 6. Règles transverses | Règles valables pour plusieurs écrans ou US | Le détail propre à une seule US |
| 7. Écrans | Écrans cités et leur accès | Un export, une recherche ou une API non cités |
| 9. Points à confirmer | Contradictions entre sources, listes annoncées absentes, termes non définis, avec leur impact | Une réponse proposée par l'agent |
| 10. Variations | Ce qui change selon le pays, le rôle ou le type d'objet, écrit dans une source | Une variation supposée « par habitude du domaine » |
| 11. Flux | Échanges avec les autres systèmes : sens, système, déclencheur, données | Un flux déduit d'un nom de champ |

Les sections 4 (comptes de test) et 8 (données de test) sont remplies par l'équipe : les laisser au modèle.

Chaque ligne cite sa source précise : `SRC-02 §4.3` ou `SRC-01 p. 12`. Une phrase sans source précise ne rentre pas.

Deux sources qui se contredisent : aucune ne gagne. Les deux versions vont en section 9 avec la question.

## 3. Configuration Azure DevOps

Section 0 : demander en une seule fois les valeurs absentes des sources (URL de l'organisation, projet Azure DevOps, plan de test par défaut, Area Path, environnements). Ne jamais les deviner.

## 4. Écrire, puis s'arrêter

1. Copier `docs/projets/_modele/CONTEXTE.md` vers `docs/projets/<projet>/CONTEXTE.md` et le remplir.
2. En-tête : date du jour, version 0.1. Journal : « création par /init-contexte, à relire ».
3. Compte rendu, puis STOP :
   1. Sections remplies et nombre de lignes par section.
   2. Points à confirmer, les bloquants en premier.
   3. Ce qui manque pour analyser une US : comptes de test, données de test, documents absents.
   4. « Le fichier est dans la pull request de cette session : relis-le, fais-le relire par l'équipe, puis fusionne. »

## Avant de livrer

1. Chaque ligne a une source précise.
2. Aucune valeur de configuration devinée.
3. Aucune contradiction tranchée par l'agent.
4. Aucune donnée client réelle.
5. Le fichier est une synthèse : aucun paragraphe recopié.
