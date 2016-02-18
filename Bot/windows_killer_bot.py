import irc.bot
import irc.strings
import irc.client
import irc.connection
import irc.server
import irc
from irc import *

class WindowsBot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6667)], "winbot2", "botwin2")

    def on_welcome(self, serv, ev):
        print("connexion au chan!!")
        serv.join("#big_rennes")

    def on_pubmsg(self, serv, ev):
        # message = ev.arguments()  # message = ev.arguments()[0] petit pb là...
        serv.privmsg("#big_rennes",  "ta geule batard!")
        pass



"""
port = 6667
channel = "#big_rennes"
nickname = "winbot"
server = "irc.freenode.net"

bot = WindowsBot(channel, nickname, server, port)
"""

print("instance")
bot = WindowsBot()
print("ok")
bot.start()

