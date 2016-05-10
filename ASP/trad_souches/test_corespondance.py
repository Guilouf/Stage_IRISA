import csv

dico_cor = {}
#chargement du dico
with open("correspondance_souches.csv", 'r') as fich_dico:
    reader = csv.reader(fich_dico, delimiter=';')
    for i in reader:  # création dico: clé: num_acc; valeur: le nom (complet) de la bact
        dico_cor[i[2]] = [i[0], i[1]]
#
# with open("list_traduction.txt", 'r') as source:
#     # reader2 = csv.reader(source, delimiter=';')
#     for j in source:
#         print(dico_cor[j.strip()])


list_key = [ key for key in dico_cor.keys()]
print(sorted(list_key))