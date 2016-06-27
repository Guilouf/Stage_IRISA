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

prot => bactéries

final:
bacterie => ec (non en fait)
"""


class HMM():

    def __init__(self):
        self.ec_reac_dico = {}
        self.reac_prot_dico = {}
        self.souche_acc_dico = {}
        self.prot_souche_dico = {}

        self.ec_prot_dico = {}

        self.ec_reac()
        self.reac_prot()
        self.souche_acc()
        self.prot_bact()

        self.asso_ec_prot()
        # self.hmm_to_asp()



    def ec_reac(self):
        """
        Associe un ec en cle et un ou des nom de réaction en valeur
        """
        with open('HMM/EC_reactions_interet_meta18.5.txt', 'r') as ec_to_react:
            reader = csv.reader(ec_to_react, delimiter=';')
            for ligne in reader:
                # permet grace au get d'initialiser ou de récupérer la valeur de la clef (finalement plus par vit)
                # vit_ec_reac_dico[ligne[0]] = vit_ec_reac_dico.get(ligne[0], {})
                # vit_ec_reac_dico[ligne[0]][ligne[1]] = ligne[2:]
                num_ec = "ec(" + ','.join([num for num in ligne[1].replace("EC-", '').split('.') if num.isnumeric()]) +")"
                # print(num_ec)
                self.ec_reac_dico[num_ec] = ligne[2:]

        # [print(self.ec_reac_dico[key]) for key in self.ec_reac_dico.keys()]


    def reac_prot(self, seuil=1):
        """
        associe des reactions à des noms de proteines, prise en compte du seuil
        """
        # print(liligne)
        # self.reac_prot_dico[vit] = self.reac_prot_dico.get(vit, {})
        # self.reac_prot_dico[vit][liligne[1]] = liligne[1]
        list_vit = ['B9', 'K2_7', 'B12']

        for vit in list_vit:  # pour ouvrir les différents fichiers
            with open('HMM/assoc_HMMs_reactions_'+vit+'_1e10.txt', 'r') as assoc_vit_fich:
                assoc_reader = csv.reader(assoc_vit_fich, delimiter='\t')
                for liligne in assoc_reader:
                    if float(liligne[2]) < seuil:  # si la p-value est inferieure au seuil
                        self.reac_prot_dico[liligne[0]] = self.reac_prot_dico.get(liligne[0], []) + [liligne[1]]

        # print(self.reac_prot_dico)
        # [print(self.reac_prot_dico[key]) for key in self.reac_prot_dico.keys()]




    def souche_acc(self):
        """
        Associe un nom de souches à son accession
        """
        with open('ASP/trad_souches/correspondance_souches-CP.csv', 'r') as corres_souches_fich:
            corres_reader = csv.reader(corres_souches_fich, delimiter=';')
            for ligne in corres_reader:
                nom = ligne[1]
                nom = ''.join(ligne[:2])
                print(nom)
                self.souche_acc_dico[nom] = ligne[2]


        # print(dico_souche_to_acc)

    def asso_ec_prot(self):
        """
        Associe un ec (cle) à une prot
        """
        for key_ec in self.ec_reac_dico.keys():
            reactions = self.ec_reac_dico[key_ec]
            for reaction in reactions:
                prot = self.reac_prot_dico.get(reaction, [])  # toutes les reaction asso aux ec n'ont pas de prot asso, dc cle -
                self.ec_prot_dico[key_ec] = self.ec_prot_dico.get(key_ec, []) + prot

        # [print(self.ec_prot_dico[key]) for key in self.ec_prot_dico.keys()]




    @staticmethod
    def parse_fasta_com(seq_param):
        seq = seq_param.split('=')[1]  # trouve le nom de la souche
        return seq[:-2]  # pour supprimer le GN


    def prot_bact(self):
        """
        Associe une souche (cle) à des valeurs, les prots
        non, une prot (cle) à des valeurs, le nom complet des bacts (ou acc?
        """
        seq_fasta = SeqIO.parse(open('HMM/prot.fasta'), 'fasta')
        for fasta in seq_fasta:
            nom_prot = fasta.id.split('|')[2]
            # print(nom_prot)
            nom_souche = self.parse_fasta_com(fasta.description)
            # print(nom_souche)
            self.prot_souche_dico[nom_prot] = self.prot_souche_dico.get(nom_prot, []) + [nom_souche]

        # print(self.prot_souche_dico)
        # [print(self.prot_souche_dico[key]) for key in self.prot_souche_dico.keys()]




    def hmm_to_asp(self):
        """
        uniprot( ec(2,7,7,7),"A0A0A7SY43").
        num_access("NZ_CP010050.1","A0A0A7SY43", "REFSEQ").
        """
        for key_ec in self.ec_prot_dico.keys():  # itère les numéros ec
            prots = self.ec_prot_dico[key_ec]
            for prot in prots:  # itère les prots du numéro Ec
                print("uniprot( " + key_ec+", \"" + prot + "\").")
                yield "uniprot( " + key_ec+", \"" + prot + "\")."
                souches = self.prot_souche_dico.get(prot)
                for sou in souches:  # itère les souches associées à la prot
                    print("num_access(\""+sou+"\",\""+prot+"\", \"HMM\").")
                    yield "num_access(\""+sou+"\",\""+prot+"\", \"HMM\")."
                    """
                    print("############## original", sou)
                    for autresou in self.souche_acc_dico.keys():  # itère les cle(souches) qui correspondrait à la souche..
                        if autresou in sou:
                            sou = self.souche_acc_dico.get(autresou, "souchePB!")
                            print(sou)
                            # print("num_access("+sou+","+prot+", \"HMM\").")
                        if sou in autresou:
                            sou = self.souche_acc_dico.get(autresou, "souchePB!")
                            print(sou)
                            # print("num_access("+sou+","+prot+", \"HMM\").")
                        else:
                            # sou = self.souche_acc_dico.get(sou, "souchePB!")
                            # print(sou)
                            pass
                    """





inst_hmm = HMM()
with open("ASP/hmm.lp", "w") as sortie:
    for ligne in inst_hmm.hmm_to_asp():
        sortie.write(ligne)
