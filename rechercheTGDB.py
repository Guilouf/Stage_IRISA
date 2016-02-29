

with open('TGDB/tgdbRef.tgdb', 'r') as tgdb:
    motcle = input()
    for ligne in tgdb:
        if motcle in ligne:
            print(ligne)