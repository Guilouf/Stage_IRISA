

with open('TGDB/tgdbRef.tgdb', 'r') as tgdb:
    motcle = input()
    for j, ligne in enumerate(tgdb):
        if motcle in ligne:
            print(ligne)

print(j)