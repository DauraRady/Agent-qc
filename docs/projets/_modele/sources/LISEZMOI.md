# Sources du projet

Déposer ici les documents de référence du projet : PRD, DAG, règles de gestion, décisions du PO, description des maquettes.

1. Format : Markdown de préférence. Un `.docx` se convertit avec `pandoc fichier.docx -t gfm -o fichier.md`. Un PDF peut rester en PDF.
2. Un document long se découpe en un fichier par chapitre (`PRD-03-demandes.md`), pour que l'agent ne lise que le chapitre utile à l'US.
3. Le nom ou la première ligne de chaque fichier donne sa version ou sa date.
4. Une nouvelle version remplace l'ancienne dans ce dossier ; Git garde l'historique. Lancer ensuite `/maj-contexte source <fichier>`.
5. Aucune donnée client réelle. Ces documents restent dans le dépôt de l'équipe.
