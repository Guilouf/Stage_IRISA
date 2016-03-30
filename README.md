# Stage_IRISA
Scripts et BDD sur la reconstruction des metagénomes

#Commandes utiles:
- git status
- git add fichier.txt
- git commit -m "message"
- git push
- si problemes: git fetch origin, puis git reset --hard origin/master
- les gist c'est un pastebin

#Les us et coutumes:
- Les .balec sont dans le gitignore 

#Memmo:
- http://eutils.ncbi.nlm.nih.gov/entrez/eutils/ =>le site de merde qui bug...

#AGENDA:
- 25 Avril 10h30: présentation des objectifs du stage 
- 28-29 Avril: Reunion Dyliss
- 13 Juin: 12 min 60 personnes..
... les dates rapport et oral?

#TODO:
- 154146A : matricule INRA LOG: gulebreton MD/
- Nouveau comptage des match en ASP
- Tester les variations pour la K
- Différencier en ASP les annotations primaires et refseq
- Mettre des pourcentages dans le tableau
- Ajouter des souches

- Pour le rdf, on peut utiliser des blank nodes avec rdflib qui font automatiquement des clés!!
- Récuprérer les réactions des vitamines
    - b9(acide folique, folate, glutamic) ,b12(cobalamine) et k2 (menaquinone, ds quinol biosynth)
- [x] Faire un schéma de la bdd (analyse si)
- [x] Compter les numéros EC
- Ajouter des données de qualité?
- [] Faire le graphe de schéma de mon truc rdf
- Relier les ec des annotations avec le nom des proteines, regarder les cross ref dispo dans les gbk
    - Il y a autant de xref uniprot que entrez..
    - Pour le lien des entrées entrez ds uniprot c ncbi/Embl CDS, EN FAIT C en bordel: ya des GI, des accessions etc..
    - Quelques GI sont presque bien annotés, 7-8 quoi.., et toujours dans la case entrez
    
 Télécharger les num_ec des vitamines, par rapport aux bactéries de références
    - Actino bactéries proches propio:
        - Corynebacterium glutamicum
        - Mycobacterium tuberculosis
        - Bifidobacterium longum
    - Gram + :
        - Bacillus subtilis (regarder ds la partie genome du ncbi)
    - Firmicutes:
        - Lactococcus lactis
        - Lactobacillus acidophilus
        - Lactobacillus delbrueckii subsp. bulgaricus
        - Streptococcus thermophilus

#Cheat markdown:
- _italic_
- **gras**
- [hypertexte](https://intranet.inria.fr/)
- >bloc note pour les images en lien ya ! aussi
* liste non ordonnée
1. liste numérotée, suivie avec un "*"
* voila, ca marche pas mais normalement c'est bon
* [x] checkbox
- double espace ca fait revenir à la ligne
