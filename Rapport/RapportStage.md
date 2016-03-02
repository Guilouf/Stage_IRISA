#Introduction


#Scripts de récupération de données
##Scripts de téléchargements
###Les informations à récupérer:
- Le numéro ec: Enzyme Commission number, c'est un schéma de classification numérique pour les enzymes, qui est basé
sur les réactions chimiques qu'elles catalysent. Chaque numéro ec est associé à un nom recommandé pour l'enzyme à 
laquelle il réfère.
Toutefois, un numéro ec ne spécifie pas une enzyme particulière, mais une réaction enzymatique, c'est à dire que des 
enzymes différentes provenant d'organismes différents peuvent recevoir un même numéro ec si elles catalysent la même 
réaction
- Les identifiants uniprot: Ils sont uniques pour chaque protéines, et vont de à 10 caractères alphanumériques. 
Cependant, une entrée de Uniprot peut avoir plusieurs numéros d'accession, notament à cause de fusions ou de séparation, 
les anciens numéros d'accession sont conservés.

###Les bases de données et leur relations avec ces informations:
- Metacyc: On peut effectuer une recherche à partir:
    - Des numéros ec
    - Les noms des composants, gènes, protéine ou pathway
    - Un identifiant PGDB (PAS human protate database..), mais pathway genome database, interne aux site biocyc
        - disonible en SBML
    - Des identifiants d'autres bdd(uniprot, ncbi), mais ce n'est pas toujours complet
    - Le locus id de biocyc
    
- Uniprot: 
    - 
- Bdd sql pour interoger plusieurs bdd bio: http://biowarehouse.ai.sri.com/PublicHouseOverview.html
    

##Base de données
