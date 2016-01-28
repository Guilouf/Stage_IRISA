#Avancement
- Création de la base de données ORM(sqlite) avec le module python sqlalchemy
    - Deux types de relations(voir plus pour la suite, chaque accession peut avoir un numéro ec via RefSeq ou 
    l'annotation primaire, et bien sur chaque accesion ou numero ec est unique
- Testé la récupération des numéros ec directement via le ncbi, du créer des fichiers virtuels pour utiliser les
données téléchargées
    
#Problèmes rencontrés:
- La base de données ORM, qui s'avera plus simple à gérer pour l'utilisation et les modification, fut un peu 
complexe à mettre en place au début pour rapport à une base SQL conventionelle
- Du utiliser la méthode des fichiers virtuels pour traiter à la volée les données de genbank sans les sauvegarder
dans des fichiers à chaque fois pour les traiter
- De ce que j'ai vu, peu de numeros ec dans les génomes drafts, et parfois ils se trouvent dans des champs pas prévus 
pour, par exemple le numero ec se retrouve au millieu d'une partie "notes" alors que le champs "ec_number" habituel
est absent. 

#Ce qui reste à faire:
- Améliorer la partie concernant la récupération des numéros ec:
    - Récupérer et traiter les annotations primaires
    - Le code marche mais est assez brouillon à cause des multiples bugs et réparations, à remettre en forme.
    - Peut être essayer de récuperer les numéros ec qui se trouvent dans des endroit exotiques, mais je ne pense pas
    que ce soit une bonne solution
- ... Puis la connecter avec la bdd (rapide)

#Autres:
- Il faudra que j'essaye d'aller voir du coté d'uniprot, qui a parait il une API mieux faite que le NCBI

#Questions:
//