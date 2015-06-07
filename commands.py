__author__ = 'christopher'

import time
import telconn
import runtime
import logger
import memorydb



def teleport(player,location):
    telconn.write_out("tele " + player + " " + location)
    time.sleep(1)
    telconn.write_out("tele " + player + " " + location)
    time.sleep(1)
    telconn.write_out("tele " + player + " " + location)

def p2p_teleport(player1,player2):
    teleport(player1,player2)

def say(message):
    telconn.write_out("say " + '"' + message + '"')

def pm(player,message):
    try:
        telconn.write_out( "pm " + player + " " + '"' + message + '"')
    except Exception as e:
        print "pm error: "+e.message


def kill_player(player):
    telconn.write_out("kill " + player)


def help(player):
    pm(player,"The following are the available commands")
    pm(player,"/home : Teleports you to your set home location")
    pm(player,"/setpoi <name> : Creates a new poi at the given location")
    pm(player,"/poi <name> : Teleports you to the named poi")
    pm(player,"/rpoi <name> : Removes the named poi")
    pm(player,"/listpoi or /lpoi : Lists all of your pois")
    pm(player,"/clearpoi : Clears all of your pois")
    pm(player,"/killme : Instantly kills you")
    pm(player,"/goto <player> : Teleports you to the named player")
    pm(player,"/bag : Teleports you your last death location")
    pm(player,"/where : Gives your position on the map")
    pm(player,"/drop : Displays a list of airdrops that have not been claimed")
    pm(player,"/claim : claims any airdrop in your radius")


def send_motd(player):
    try:
        time.sleep(5)
        pm(player,runtime.motd)
        pm(player,"Type /help for a list of available commands")
    except Exception as e:
        logger.log_debug("send_motd error: " + e.message)

def update_players():
    telconn.write_out("lp")

def update_player_objects_timed():
    time.sleep(5)
    update_players()
    while runtime.run:
        if len(memorydb.online_players)>0:
            update_players()
        time.sleep(1)