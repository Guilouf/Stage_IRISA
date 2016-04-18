#!/usr/bin/env python
from pyasp.asp import *
from io import StringIO
import csv

# TODO ya des numeros Gi qui se balladent en tant que uniprot..=> voir le todo pr abruti ds recup ec..

# TODO on peut envoyer les trucs asp en strings, regarder le tuto
# TODO matter si ya bien autant de ref que d'ec..

"""
#Memmo base#
common_name(reaction_id or enzyme_id or pathway_id or compound_id , common_name).
direction(reaction_id, reaction_direction).
ec_number(reaction_id, ec(x,x,x,x) ou ec(x,x,x)).
reactant(reaction_id, reactant_id, stochio)
product(reaction_id, product_id, stochio).
in_pathway(reaction_id, pathway_id).
catalysed_by(reaction_id, enzyme_id).
uniprotID(enzyme_id, uniprot_id).
is_a(class or compound, class_id).
is_a(pathway_id, pathway_id).

#Memmo ma base#
uniprot( ec(2,1,1,72),"A0A0L7Y7H5").
num_access("NC_020229.1","A0A0L7Y7H5").
"""
###########
# memmo ASP
###########
"""
Mettre des Maj aux noms de variables..
"""

goptions = ''  # soluce max gringo
soptions = ''  # solutions max solveur
solver = Gringo4Clasp(gringo_options=goptions, clasp_options=soptions)

#le test ASP en fichier virtuel..
testo = """
"""
test_io = StringIO(testo)

# Liste des fichiers asp
hidden = 'ASP/hidden.lp'
base = 'ASP/metacyc_18.5.lp'
query = 'ASP/explore.lp'
test = 'ASP/test.lp'
metagdb = 'ASP/ec_uni.lp'


# Solver
result = solver.run([hidden, base, test, metagdb], collapseTerms=True, collapseAtoms=False)

# impression de sortie ASP
for term in result[0]:
    print(term)

# Impression du nombre d'élément en sortie
print("Nombre: ", len(result[0]))


def tableau_1(souche):

    """
    A utiliser avec statS(V,S,T,N) du ASP
    :param souche:
    :return:
    """

    if souche not in str(result[0]):
        print("0 ; 0", end='')

    for term in result[0]:  # parcourt les resultats (aléatoire..)
        split_term = str(term).split(",")

        if split_term[1].replace("\"", '') == souche and int(split_term[3][0]) == 4 \
                and split_term[0][0:5] == "statS":
            # print(split_term[1], split_term[2][2:], split_term[3][0], split_term[4][0], end='; ')
            print(split_term[4].replace(')', ''), end=';')

    for term in result[0]:  # parcourt les resultats (t=3..)
        split_term = str(term).split(",")

        if split_term[1].replace("\"", '') == souche and int(split_term[3][0]) == 3 \
                and split_term[0][0:5] == "statS":
            # print(split_term[1], split_term[2][2:], split_term[3][0], split_term[4][0], end=' ')
            print(split_term[4].replace(')', ''), end='')

    print('')

# todo ce srait bien d'avoir un parseur csv..


def tableau_1bis(souche):

    if souche not in str(result[0]):
        print('X')

    for term_bis in result[0]:
        split_term_bis = str(term_bis).split(",")
        if split_term_bis[1].replace("\"", '') == souche:
            # print(term_bis)
            print(split_term_bis[2].replace(")", ''))


# le header
ligne_ec = []
# parcourt les enzymeV, pour tracer la ligne des EC
# faut l'exécuter qu'une seule fois, pas à chaque souche..
# pour b9 c normal qu'il y ai 2* 3.6.1, et ils ne sont pas tjr dans l'ordre a cause d'ASP
print("Num_Ec: ", end=' ; ')
for term in result[0]:
    split_term = str(term).split(",")
    if split_term[0][0:7] == "enzymeV":
        num_ec = [i for i in ''.join(split_term[1:]) if i.isdigit()]
        num_ec = ''.join(num_ec)
        ligne_ec.append(num_ec)
        print(num_ec, end=' ; ')
print('')
# ligne_ec = set(ligne_ec)  # TODO le set n'est pas ordonné..
# 3.6.1.o qui pose pb..


def tableau_2(souche):
    colone_souche = []
    print(souche, end=' ;')
    for ec_header in ligne_ec:  # parcourt les ec du header, cad du pathway de la vitamin, les colones

        boobool = True
        for termS in result[0]:  # fait défiler les facts ASP
            split_term_s = str(termS).split(",")  # todo attention ca va varier pour les ec de talle différentes.. genre 2* 3.6.1..
            # todo faut donc enlever un num ec
            if split_term_s[0][0:11] == "final_match" and split_term_s[1].replace('"', '') == souche:  # si la ligne correspond à la souche
                num_ecS = [i for i in ''.join(split_term_s[4:]) if i.isdigit()]
                num_ecS = ''.join(num_ecS)
                # print(num_ecS)
                if num_ecS == ec_header:  # si le num dans la souche corespond à celui de header §§§ il est là le pb!!
                    # print(split_term_s)
                    print(num_ecS, end=' ; ')
                    boobool = False
        if boobool == True:
            print('X', end=' ; ')
    print('')

    pass

with open('exemple/ListeAccess', mode='r') as list_souches:
    for numacc in list_souches:  # itère la liste des accessions à regarder
        # tableau_1(numacc.strip())  # gaffe aux espaces à la fin du doc.. le strip pour enlever les \n...
        # tableau_1bis(numacc.strip())
        tableau_2(numacc.strip())
        pass

with open('ASP/tableauSortie.csv', 'w') as sortie_csv:
    writer = csv.writer(sortie_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)  # quote tout les entrées


"""
LEKW00000000.1
NZ_CM003439.1
NZ_CP010528.1
NZ_CP009236.1
NC_021514.1
NC_020229.1
NC_014554.1
NC_021224.2
NC_012984.1
AL935263.2
FN806773
"""