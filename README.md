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

#TODO:
- Ramener le tascam
- Regarder l'API de uniprot (ou metacyc?)
- Récuprérer les réactions des vitamines
    - b9(acide folique) ,b12(cobalamine) et k2 (menaquinone)
- Regarder bigg?
- [x] Faire un schéma de la bdd (analyse si)
- [x] Compter les numéros EC
- Ajouter des données de qualité?
- Ajouter une relation pour dire qu'une protéine appartient au voies de synthèse des vitamines

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
