# -*- coding: utf-8 -*-

import irc.bot
import irc.strings
import irc.client
import irc.connection
import irc.server
import irc.modes
import irc
from irc import *

import random as ran
import string
import time
"""
cat /udd/glebreto/Desktop/MesTrucs/Git/Bot/windows_killer_bot.py | ssh flamboyant python3 -
La mort ahahah
"""

class WindowsBot(irc.bot.SingleServerIRCBot):
    """
    faire un mode discussion pour que 2 bots se parlent
    recevoir des messages privés
    faire un truc pour faire chier munin
    /msg pour les messages privés
    il va faire tout noir!
    get_host pour changer adresse ip?
    parse mod string pour le ban pe
    on ne jure pas marie thèrèse
    la partie client.py à l'air importante
    ssh flamboyant
    string
    """
    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6667)], "gentilbot", "gentil")

        self.windows_error = ["An error as occured while displaying previous error",
                              "Windows problem reporting has stopped working",
                              "ERROR: The operation completed successfully",
                              "Cannot delete 6620: Not enough free disk space",
                              "A problem has been detected and windows shutdown to prevent damage to your computer",
                              "STOP error 0x1 (0x00000001) ",
                              "DRIVER_POWER_STATE_FAILURE",
                              "The program you are using has encountered a problem and needs to close",
                              "Unexpected error. Please investigate",
                              "Are you sur you want to send recycle bin to recycle bin?",
                              "Error 1603",
                              "Abort, Retry, Fail?",
                              "Windows Must Restart Because the Remote Procedure Call (RPC) Service Terminated"
                              " Unexpectedly ",
                              "https://www.youtube.com/watch?v=IW7Rqwwth84"]
        self.propaganda = [": La plupart des DABs (distributeurs de billets) tournent sous windows xp",
                           ": Ceux qui disent qu'il y a une alternative à Windows sont les"
                           " mêmes qui ont créé le goulag comme alternative au capitalisme"]

        self.anti_linux = [": Le saviez vous? Linux est l'OS préféré des pédophiles.",
                           ": lp0 on fire",
                           ": T'es pas au courrant? Linux c'est de la merde! Gratuite certes,"
                           " mais de la merde quand même."]
        self.welcome_message = ["Coucou, je suis votre nouvel ami!",
                                "Avec moi, vous allez oublier la propagande malhonnète ochestrée par le puissant"
                                " lobby de linux, en effet nul n'est plus esclave que celui qui se croit libre ",
                                "Tremblez, tas de cellules, une nouvelle ère d'intelligence artificielle viens de "
                                "naître !",
                                "Il va faire tout noir!"]
        self.insultes_personl = [": ta geule batard !", ": si ce que tu as à dire n'est plus beau que ferme ta gueule!",
                                 ": PSV t'envois un jolde en jif http://www.eazyhomepage.com/gold-bars4.gif",
                                 "Chut! Le silence est d'or la parole est d'argent, dors au lieu de faire chier les"
                                 "gens"]
        self.big_words = ["putain", "chier", "merde", "salope", "enculé", "enkulé", "bordel"]

        self.big_nick = ["Lex", "Natir", "DrIDK", "Char-Al", "elucator", "munin", "Nedgang", "neolem", "pirc", "Plopp",
                         "Elisyre", "Andrano"]


    def on_welcome(self, serv, ev):
        print("connexion au chan!!")
        serv.join("#big_rennes")
        serv.privmsg("#big_rennes",  self.welcome_message[ran.randint(0, len(self.welcome_message)-1)])

    def on_nicknameinuse(self, serv, ev):  # permet de changer de nick si déjà utilisé
        serv.nick(serv.get_nickname() + str(ran.randint(0, 1000)))

    def on_kick(self, serv, ev):
        serv.nick(serv.get_nickname() + str(ran.randint(0, 1000)))
        # serv.realname(serv.get_realname() + str(ran.randint(0, 1000)))

        serv.join("#big_rennes")

    def on_mode(self, serv, ev):
        print("je suis ban")
        pass

    def on_pubmsg(self, serv, ev):
        message = (ev.arguments[0], ev.source.nick)  # message = ev.arguments()[0] petit pb là...
        if str(message[0][0:5]) == "flood" and message[0][5:7].isnumeric():
            for i in range(0, int(message[0][5:7])):
                serv.privmsg("#big_rennes",  self.windows_error[ran.randint(0, len(self.windows_error)-1)])
                time.sleep(3)

        elif "linux" in message[0].lower():
            serv.privmsg("#big_rennes", message[1] + self.anti_linux[ran.randint(0, len(self.anti_linux)-1)])

        elif "windows" in message[0].lower():
            serv.privmsg("#big_rennes", message[1] + self.propaganda[ran.randint(0, len(self.propaganda)-1)])
            serv.privmsg("#big_rennes",  self.windows_error[ran.randint(0, len(self.windows_error)-1)])

        elif "err" in message[0].lower():  # pas au point, match que sur les mots entiers TODO: "probleme",
            serv.privmsg("#big_rennes",  self.windows_error[ran.randint(0, len(self.windows_error)-1)])

        elif "help" in message[0].lower():
            serv.privmsg("#big_rennes", message[1] + ": Demerde toi, je suis un bot libre! (mais payant)")

        elif "faire" in message[0].lower() and "noir" in message[0].lower():
            serv.privmsg("#big_rennes", message[1] + ": Ta gueule! ")

        elif len(message[0]) < 1: # TODO inf à 1
            print(message[0][0:4])
            serv.privmsg("#big_rennes", message[1] + ": PSV t'envois un jolde en jif http://www.eazyhomepage.com"
                                                     "/gold-bars4.gif. ERROR: Too short message")



"""
port = 6667
channel = "#big_rennes"
nickname = "winbot"
server = "irc.freenode.net"

bot = WindowsBot(channel, nickname, server, port)
"""

print("instanciation")
bot = WindowsBot()
bot.start()

