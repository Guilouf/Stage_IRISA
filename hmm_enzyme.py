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
Ec => reactions (ec_reac_interet..)

reaction => prot (assoc_HMM)

bactérie => prots (fichier fasta
"""

"""
Le but:
Ec => prots Ok

bacterie <=> prot ?


final:
bacterie => ec
"""

class HMM():

    def __init__(self):
        self.ec_reac_dico = {}
        self.reac_prot_dico = {}
        self.souche_acc_dico = {}

        self.reac_ec_dico = {}

        self.ec_reac()
        self.reac_prot()
        self.souche_ec()

        self.asso_ec_prot()


    def ec_reac(self):
        """
        Associe un ec en cle et un ou des nom de réaction en valeur
        """
        # todo formatter mieux les ec..

        with open('HMM/EC_reactions_interet_meta18.5.txt', 'r') as ec_to_react:
            reader = csv.reader(ec_to_react, delimiter=';')
            for ligne in reader:
                # permet grace au get d'initialiser ou de récupérer la valeur de la clef (finalement plus par vit)
                # vit_ec_reac_dico[ligne[0]] = vit_ec_reac_dico.get(ligne[0], {})
                # vit_ec_reac_dico[ligne[0]][ligne[1]] = ligne[2:]
                self.ec_reac_dico[ligne[1]] = ligne[2:]

        # [print(self.ec_reac_dico[key]) for key in self.ec_reac_dico.keys()]


    def reac_prot(self, seuil=1):
        """
        associe des reactions à des noms de proteines, prise en compte du seuil
        """
        # print(liligne)
        # self.reac_prot_dico[vit] = self.reac_prot_dico.get(vit, {})
        # self.reac_prot_dico[vit][liligne[1]] = liligne[1]
        list_vit = ['b9', 'k2_7', 'b12']

        for vit in list_vit:  # pour ouvrir les différents fichiers
            with open('HMM/assoc_HMMs_reactions_'+vit+'.txt', 'r') as assoc_vit_fich:
                assoc_reader = csv.reader(assoc_vit_fich, delimiter='\t')
                for liligne in assoc_reader:
                    if float(liligne[2]) < seuil:  # si la p-value est inferieure au seuil
                        self.reac_prot_dico[liligne[0]] = self.reac_prot_dico.get(liligne[0], []) + [liligne[1]]

        # print(self.reac_prot_dico)
        # [print(self.reac_prot_dico[key]) for key in self.reac_prot_dico.keys()]




    def souche_ec(self):
        """
        Associe un nom de souches à son accession
        """
        with open('ASP/trad_souches/correspondance_souches-CP.csv', 'r') as corres_souches_fich:
            corres_reader = csv.reader(corres_souches_fich, delimiter=';')
            for ligne in corres_reader:
                nom = ligne[1]
                nom = ''.join(ligne[:2])
                # print(nom)
                self.souche_acc_dico[nom] = ligne[2] # todo faire un get..


        # print(dico_souche_to_acc)

    def asso_ec_prot(self):
        for key_ec in self.ec_reac_dico.keys():
            reactions = self.ec_reac_dico[key_ec]
            for reaction in reactions:
                prot = self.reac_prot_dico.get(reaction, None)  # toutes les reaction asso aux ec n'ont pas de prot asso, dc cle -
                self.reac_ec_dico[key_ec] = self.reac_ec_dico.get(key_ec, []) + [prot]

        [print(self.reac_ec_dico[key]) for key in self.reac_ec_dico.keys()]



    """
    Associe une souche (cle) à des valeurs, les prots
    """
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

    """
    on veut des num acc de souches, associées à des numéros ec
    """
    def hmm_to_asp(p_vit_ec_reac_dico, p_dico_souche_to_acc, p_dico_reac_prot, p_dico_souche_prot):
        for vit_ in p_vit_ec_reac_dico.keys():  #itère les vitamines
            for num_ec in p_vit_ec_reac_dico[vit_].keys():  # itère les nums ec
                list_nomreaction = p_vit_ec_reac_dico[vit_][num_ec]
                for reac in list_nomreaction:  # itère les reactions
                    pass



    # hmm_to_asp(vit_ec_reac_dico, dico_souche_to_acc, dico_reac_prot, dico_souche_prot)

inst_hmm = HMM()