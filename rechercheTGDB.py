

with open('TGDB/tgdbRef.tgdb', 'r') as tgdb:
    motcle = input()
    j = 0
    for ligne in tgdb:
        if motcle in ligne:
            j += 1
            print(ligne)

print(j)
