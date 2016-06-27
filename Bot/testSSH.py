# -*- coding: utf-8 -*-

"""
le but du test: se connecter sur une machine et y copier un fichier
"""

from pexpect import pxssh
import pexpect
import sys
import os
import time


sess = pxssh.pxssh()
enemi_ordi = sys.argv[1]
me_param = "glebreto"
mdp_param = sys.argv[2]

sess2 = pexpect.spawn("ssh pi@192.168.0.11")


def methode_simple():  # ouais mais faut mixer os et pexpect..?

    """
    os.system("ssh pi@192.168.0.11")
    time.sleep(5)
    os.system(mdp_param)
    """
    sess2.expect("password")
    sess2.sendline(mdp_param)


def methode_complexe():
    sess.login(enemi_ordi, me_param, mdp_param)  # connexion ssh à l'enemi
    sess.sendline("eject")  # le lecteur cd...

while True:
    pass
