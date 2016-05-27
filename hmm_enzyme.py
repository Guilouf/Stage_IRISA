import csv
from Bio import SeqIO

# essayer de formatter les ec pareil que ds ma bdd... ou que le fichier ASP


"""
en gros le but serait d'ajouter des ec dans les souches asp, rien de très compliqué mis a part qu'il faille que je lie
les protéines détectées au numéro d'accession de la souche.
=>j'ai completement merdé en fait ===> il faut que je me serve du fasta aussi en fait
=>utiliser correspondance souches.csv
"""




"""
Associe un ec en cle et un nom de réaction en valeur, pour chaque vitamine (dico imbriqués)
"""
# todo formatter mieux les ec..
vit_ec_reac_dico = {}
with open('HMM/EC_reactions_interet_meta18.5.txt', 'r') as ec_to_react:
    reader = csv.reader(ec_to_react, delimiter=';')
    for ligne in reader:
        # permet grace au get d'initialiser ou de récupérer la valeur de la clef
        vit_ec_reac_dico[ligne[0]] = vit_ec_reac_dico.get(ligne[0], {})

        vit_ec_reac_dico[ligne[0]][ligne[1]] = ligne[2:]




# print(vit_ec_reac_dico)

"""
Associe un nom de souches à son accession
"""
dico_souche_to_acc = {}
with open('ASP/trad_souches/correspondance_souches-CP.csv', 'r') as corres_souches_fich:
    corres_reader = csv.reader(corres_souches_fich, delimiter=';')
    for ligne in corres_reader:
        nom = ''.join(ligne[:2])
        # print(nom)
        dico_souche_to_acc[nom] = ligne[2]


# print(dico_souche_to_acc)


"""
fait des choses..
associe des reactions à des noms de proteines
"""
list_vit = ['b9', 'k2_7', 'b12']
dico_reac_prot = {}
for vit in list_vit:
    with open('HMM/assoc_HMMs_reactions_'+vit+'.txt', 'r') as assoc_vit_fich:
        assoc_reader = csv.reader(assoc_vit_fich, delimiter='\t')
        for liligne in assoc_reader:
            # print(liligne)

            dico_reac_prot[vit] = dico_reac_prot.get(vit, {})
            dico_reac_prot[vit][liligne[1]] = liligne[1]
            pass


"""
Associe une souche (cle) à des valeurs, les prots
"""
def parse_fasta_com(seq_param):
    seq = seq_param.split('=')[1]  # trouve le nom de la souche
    return seq[:-2]  # pour supprimer le GN
dico_souche_prot = {}
seq_fasta = SeqIO.parse(open('HMM/prot.fasta'), 'fasta')
for fasta in seq_fasta:
    nom_prot = fasta.id.split('|')[2]
    # print(nom_prot)
    nom_souche = parse_fasta_com(fasta.description)
    # print(nom_souche)
    dico_souche_prot[nom_souche] = dico_souche_prot.get(nom_souche, []) + [nom_prot]

# print(dico_souche_prot)


"""
on veut des num acc de souches, associées à des numéros ec
"""
def hmm_to_asp(p_vit_ec_reac_dico, p_dico_souche_to_acc, p_dico_reac_prot, p_dico_souche_prot):
    for vit_ in p_vit_ec_reac_dico.keys():  #itère les vitamines
        for num_ec in p_vit_ec_reac_dico[vit_].keys():  # itère les nums ec
            list_nomreaction = p_vit_ec_reac_dico[vit_][num_ec]
            for reac in list_nomreaction:  # itère les reactions
                pass



hmm_to_asp(vit_ec_reac_dico, dico_souche_to_acc, dico_reac_prot, dico_souche_prot)