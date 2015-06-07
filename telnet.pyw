#!/usr/bin/python

import telnetlib
import thread
import threading
import re
import os
import pickle
import random
import string
import socket
import time
import ConfigParser
from time import strftime, sleep
from Tkinter import *
from ttk import *

VERBOSE = False

out = ""
run = True

#http://steamcommunity.com/profiles/steamid

SessionLog = []
PlayerObjectArray = []
OnlinePlayerList = []
PlayerUpdateList = []
AirDrops = []

def create_config():
    config = ConfigParser.RawConfigParser()
    config.add_section('Configuration')
    config.set('Configuration', 'host', 'localhost')
    config.set('Configuration', 'port', '81')
    config.set('Configuration', 'password', 'changeme')
    config.set('Configuration', 'motd', '')
    config.set('Configuration', 'gui', 'false')
    config.set('Configuration', 'server', 'true')
    config.set('Configuration', 'verbose', 'false')
    with open('config.cfg', 'wb') as configfile:
        config.write(configfile)

def read_config():
    global HOST, PORT, PASSWORD, MOTD, GUI, SERVER, VERBOSE
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    HOST = config.get('Configuration', 'host')
    PORT = config.get('Configuration', 'port')
    PASSWORD = config.get('Configuration', 'password')
    MOTD = config.get('Configuration', 'motd')
    GUI = config.getboolean('Configuration', 'gui')
    SERVER = config.getboolean('Configuration', 'server')
    VERBOSE = config.getboolean('Configuration', 'verbose')

DesktopNotify = False
Debug = True


root = Tk()
root.title("7dtd Telnet Client")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
note = Notebook(root)
note.columnconfigure(0, weight=1)
note.rowconfigure(0, weight=1)
note.grid(sticky=NSEW)



tab1 = Frame(note)
tab1.columnconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)
tab1.rowconfigure(0, weight=1)
textbox = Text(tab1, height=20, width=80)
textbox.columnconfigure(0, weight=1)
textbox.rowconfigure(0, weight=1)
playerbox = Text(tab1, height=20, width=20)
commandLabel = Label(tab1, width=10, text="Command:")
input = Entry(tab1, width=80)


tab2 = Frame(note)
tab2.columnconfigure(0, weight=1)
tab2.rowconfigure(0, weight=1)
playerlist = Listbox(tab2, height=20, width=20)
infobox = Text(tab2, height=10, width=80)


def getPlayerObject(name):
	for player in PlayerObjectArray:
		if player.name == name:
			return player

def show_player_info(name):
    infobox.delete("1.0", END)
    player = getPlayerObject(name)
    infobox.insert(END, "Name:"+ player.name+ "\n")
    infobox.insert(END, "SteamID:"+ player.steamid+ "\n")
    infobox.insert(END, "IP:"+ player.ip+ "\n")
    infobox.insert(END, "Last Location:"+ player.position+ "\n")

def addInfo(info):
	textbox.insert(END,info + '\n')
	textbox.see(END)

def refreshPlayerList():
	playerbox.delete("1.0", END)
	for player in OnlinePlayerList:
		playerbox.insert("1.0",player+ "\n")
def refreshInfoList():
    playerlist.delete(1, END)
    for player in PlayerObjectArray:
        playerlist.insert(1, player.name)

def func(event):
	send_command(input.get())
	input.delete(0, END)

def listclick(e):
    show_player_info(str(playerlist.get(playerlist.curselection())))


def handler():
    global run
    run = False
    root.destroy()
    sys.exit()


textbox.grid(row=0, column=0, sticky=NSEW, columnspan=2)
playerbox.grid(row=0, column=3, sticky=N+S)
commandLabel.grid(row=1, column=0, sticky=W)
input.grid(row=1, column=1, sticky=E+W, columnspan=3)
input.bind('<Return>', func)
note.add(tab1, text="Console", compound=TOP)

playerlist.grid(row=0,column=1,sticky=N+S)
playerlist.bind('<<ListboxSelect>>', listclick)
infobox.grid(row=0, column=0, sticky=N+E+W)
note.add(tab2, text = "Players")

root.protocol("WM_DELETE_WINDOW", handler)

def log(info):
    print info
    if GUI:
        addInfo(info)



def decode_players():
    player_export = open("player_export.csv", "wb")
    poi_export= open("poi_export.csv", "wb")
    try:
        with open("players.pickle", "rb") as f:
            log("Trying to load player information...")
            while True:
                try:
                    PlayerObjectArray.append(pickle.load(f))
                except EOFError:
                    break
        log("The following players have been loaded...")
        for player in PlayerObjectArray:
            player_export.write(player.name + "," + player.steamid +",,," + player.home+ ",,,,," +"\n")
            log("-------------")
            log("Name:" + player.name)
            log("SteamID:" + str(player.steamid))
            log("IP:" + str(player.ip))
            log("EntityID:" + str(player.entityid))
            log("Home:" + str(player.home))
            log(" ")
            for poi in player.pois:
                poi_export.write(player.name +"," +player.steamid+","+poi.split(",")[1]+","+poi.split(",")[0]+","+player.steamid+poi.split(",")[1]+"\n")
        f.close()
        player_export.close()
    except:
         log("Error opening players pickle file")

def encode_players():
    with open("players.pickle", "wb") as f:
        for player in PlayerObjectArray:
                    pickle.dump(player, f, -1)
    f.close()

def send_command(cmd):
    out.write(cmd + "\n")

def delayed_teleport(tp):
    out.write(tp)
    time.sleep(1)
    out.write(tp)
    time.sleep(1)
    out.write(tp)	

def pm(message,player):
    out.write( "pm " + player + " " + '"' + message + '"' + "\n")

def say(message):
    out.write("say " + '"' + message + '"' + "\n")



def shutdown():
   out.write("shutdown " + "\n")

def kick(player, reason=""):
    out.write("kick " + player + " " + reason + "\n")

def whitelistUpdate(player, operation, level=0):
    if level > 0:
        out.write("whitelist " + operation + " " + player + " " + level + "\n")
    else:
        out.write("whitelist " + operation + " " + player + "\n")

def airDrop():
    out.write("spawnairdrop " + "\n")

def warn(player, reason=""):
    for idx, playerobject in enumerate(PlayerObjectArray):
        if player in playerobject.name:
            out.write("pm " + player + " You have been issued a warning:" + reason + "\n")
            playerobject.warned += 1
            out.write("pm " + player + " You have been warned " + str(playerobject.warned) + " times" + "\n")

def update_player_objects_timed():
    out.write("lp\n")
    while True:
        if len(OnlinePlayerList)>0:
            out.write("lp\n")
        sleep(1)
def update_player_objects():
    out.write("lp\n")

def send_motd(player):
    sleep(5)
    pm(MOTD,player)
    pm("Type /help for a list of available commands",player)


def notify(msg):
    if DesktopNotify:
        os.system("notify-send "+msg)

class player_object(object):
    def __init__(self):
        self.name = ""
        self.entityid = 0
        self.steamid = 0
        self.ip= ""
        self.lastlogon = ""
        self.home = ""
        self.warned = 0
        self.location = ""
        self.home = ""
        self.health = 0
        self.deaths = 0
        self.zombies = 0
        self.players = 0
        self.score = 0
        self.ping = 0
        self.position = ""
        self.pois = []
        self.tprequests = []
        self.admin = False
        self.adminlevel = 0
        self.mod = False
        self.revive = ""

    def adminAdd(self):
        pass

    def adminRemove(self):
        pass

    def adminUpdate(self,level):
        pass
    def modAdd(self):
        pass

    def modRemove(self):
        pass

    def modUpdate(self,level):
        pass



def parse_players_update(line):
            try:
                    position = str(int(round(float(line.split(" ")[3].replace("pos=(", "").replace(",", ""))))) + " " + str(int(round(float(line.split(" ")[4].replace(",", ""))))) + " " + str(int(round(float(line.split(" ")[5].replace("),", "")))))
                    entityid = line.split(",")[0].split("=")[1]
                    name = line.split(",")[1].replace(" ", "")
                    health = line.split(",")[9].split("=")[1]
                    death = line.split(",")[10].split("=")[1]
                    zombies = line.split(",")[11].split("=")[1]
                    players = line.split(",")[12].split("=")[1]
                    score = line.split(",")[13].split("=")[1]
                    steamid = line.split(",")[15].split("=")[1]
                    ip = line.split(",")[16].split("=")[1]
                    ping = line.split(",")[17].split("=")[1].rstrip(string.whitespace)

                    if name not in OnlinePlayerList:
                                OnlinePlayerList.append(name)
                                if GUI:
                                    refreshPlayerList()

                    if len(PlayerObjectArray) < 1:
                        log(" object array is empty.creating new player object")
                        player = player_object()
                        player.health = health
                        player.deaths = death
                        player.zombies = zombies
                        player.players = players
                        player.score = score
                        player.ping = ping
                        player.position = position
                        player.name = name
                        player.steamid = steamid
                        player.ip = ip
                        player.entityid = entityid
                        PlayerObjectArray.append(player)
                        log("-------------")
                        log("Name:" + player.name)
                        log("SteamID:" + str(player.steamid))
                        log("IP:" + str(player.ip))
                        log("EntityID:" + str(player.entityid))
                        encode_players()

                    found = 0
                    for player in PlayerObjectArray:
                        if steamid == player.steamid:
                            found = 1
                            player.health = health
                            player.deaths = death
                            player.zombies = zombies
                            player.players = players
                            player.score = score
                            player.ping = ping
                            player.position = position
                            player.name = name
                            player.steamid = steamid
                            player.ip = ip
                            player.entityid = entityid

                    if found == 0:
                        log("new player joined.creating new player object")
                        player = player_object()
                        player.health = health
                        player.deaths = death
                        player.zombies = zombies
                        player.players = players
                        player.score = score
                        player.ping = ping
                        player.position = position
                        player.name = name
                        player.steamid = steamid
                        player.ip = ip
                        player.entityid = entityid
                        PlayerObjectArray.append(player)
                        log("-------------")
                        log("Name:" + player.name)
                        log("SteamID:" + str(player.steamid))
                        log("IP:" + str(player.ip))
                        log("EntityID:" + str(player.entityid))
                        encode_players()
                        if GUI:
                            refreshInfoList()

            except:
                log("error parsing player lp")

def readsession(line):
            # SessionLog.append(line)# necessary for stats and time?
            if VERBOSE:
                log(line)
            STATS = re.search("STATS", line)
            CONNECTED = re.search("Player connected", line)
            JOINED = re.search("joined the game", line)
            DISCONNECTED = re.search("left the game", line)
            MESSAGE = re.search("GMSG: ", line)
            NIGHTHORDE = re.search("Spawning Night Horde for day", line)
            WANDERINGHORDE = re.search("Spawning Wandering Horde", line)
            WAVESPAWN = re.search("Spawning this wave", line)
            LISTPLAYERS = re.search("([0-9][.]\sid=)", line)
            AIRDROP = re.search("INF AIAirDrop: Spawned supply crate",line)

            if NIGHTHORDE:
                log(line)

            if WAVESPAWN:
                log(line)

            if WANDERINGHORDE:
                 log(line)

            if CONNECTED:
                playername = line.split(",")[2].split("=")[1]
                update_player_objects()
                log(strftime("%m-%d-%y %I:%M:%S %p") + ":Player connected: " + playername)
                notify("Connected:" + playername)
                if SERVER:
                    send_motd(playername)


            if DISCONNECTED:
                playername = line.split(' ')[4]
                log(strftime("%m-%d-%y %I:%M:%S %p") + ":Player disconnected: " + playername)
                notify("Disconnected:" + playername)
                try:
                    OnlinePlayerList.remove(playername)
                    if GUI:
                        refreshPlayerList()
                except:
                    pass


            if AIRDROP:
                try:
                    line = line.replace("(","").replace(")","").replace(",","").split()
                    x = line[8]
                    y = line[10]
                    z = line[9]
                    location = str(x)+","+str(64)+","+str(y)
                    AirDrops.append(location)
                    say("Airdrop at " + location)
                except:
                    log("Error parsing airdrop info")

            if MESSAGE:
                log(line)
                if SERVER:
                    playername = line.split(" ")[4].rstrip(':')
                    DEBUG = re.search("/debug", line)
                    SETHOME = re.search("/sethome", line)
                    HOME = re.search("/home", line)
                    RANDOM = re.search("/random", line)
                    SETPOI = re.search("/setpoi", line)
                    POI = re.search("/poi", line)
                    RPOI = re.search("/rpoi", line)
                    LISTPOI = re.search("/listpoi", line)
                    LPOI = re.search("/lpoi", line)
                    CLEARPOI = re.search("/clearpoi", line)
                    KILLME = re.search("/killme", line)
                    GOTO = re.search("/goto", line)
                    HELP = re.search("/help", line)
                    REVIVE = re.search("/bag",line)
                    DIED = re.search("died",line)

                    if DIED:
                        try:
                            playername = line.split(" ")[5]
                            #log(playername + " has died")
                            for player in PlayerObjectArray:
                                if playername == player.name:
                                    #log(player.position)
                                    player.revive = player.position
                                    log("Setting " + player.name + " revive point to: " + player.position)
                                    pm("Setting your revive point to: "+ player.position,player.name )
                        except:
                            log("Failed to parse player death output (line 436)")


                    if HELP:
                        pm("The following are the available commands",playername)
                        pm("/sethome <name> Sets your home",playername)
                        pm("/home <name> Teleports you to your set home location",playername)
                        pm("/setpoi <name> Creates a new poi at the given location",playername)
                        pm("/rpoi <name> Removes the named poi",playername)
                        pm("/listpoi or /lpoi Lists all of your pois",playername)
                        pm("/clearpoi Clears all of your pois",playername)
                        pm("/killme Instantly kills you",playername)
                        pm("/goto <player> Teleports you to the named player",playername)
                        pm("/home <name> Teleports you to your set home location",playername)


                    if KILLME:
                        out.write("kill " + playername + "\n")

                    if GOTO:
                        try:
                            player2 = line.split(" ")[6]
                            #out.write("tele " + playername + " " + player2 + "\n")
                            try:
                                thread.start_new_thread(delayed_teleport, ("tele " + playername + " " + player2 + "\n",))
                            except Exception as errtxt:
                                print errtxt

                        except:
                            pm("Teleport failed. Check target name and try again",playername)

                    if SETHOME:
                        for player in PlayerObjectArray:
                            if playername in player.name:
                                player.home = player.position
                                pm("Home has been set to " + player.home,player.name)
                                log(player.name + " Home has been set to " + player.home)
                                encode_players()

                    if HOME:
                        for player in PlayerObjectArray:
                            if playername in player.name:
                                #out.write("tele " + playername + " " + player.home + "\n")
                                try:
                                    thread.start_new_thread(delayed_teleport, ("tele " + playername + " " + player.home + "\n",))
                                except Exception as errtxt:
                                    print errtxt
				
                    if RANDOM:
                        randomx = random.randint(-1000, 1000)
                        randomy = random.randint(-1000, 1000)
                        #out.write("tele " + playername + " " + str(randomx) + " 64 " + str(randomy) + "\n")

                    if SETPOI:
                        for player in PlayerObjectArray:
                            if playername in player.name:
                                try:
                                    found = 0
                                    poiname = line.split(" ")[6].rstrip(string.whitespace)
                                    poistring = player.position + "," + poiname
                                    for poi in player.pois:
                                        if poiname == poi.split(",")[1]:
                                            player.pois.remove(poi)
                                            player.pois.append(poistring)
                                            found = 1

                                    if found == 0:
                                        player.pois.append(poistring)
                                    pm(player.position + " has been set as " + poiname,player.name)
                                    encode_players()
                                except:
                                    pm("Failed to set poi",player.name)

                    if POI:
                        error = 0
                        try:
                            poiname = line.split(" ")[6].rstrip(string.whitespace)
                        except:
                            error = 1
                        for player in PlayerObjectArray:
                            if playername in player.name:
                                if error != 1:
                                    found = 0
                                    for poi in player.pois:
                                        poilocation = poi.split(",")[0]
                                        if poiname == poi.split(",")[1]:
                                            #out.write("tele " + playername + " " + poilocation + "\n")
                                            try:
                                                thread.start_new_thread(delayed_teleport, ("tele " + playername + " " + poilocation + "\n",))
                                            except Exception as errtxt:
                                                print errtxt
                                            found = 1
                                    if found == 0:
                                        pm( "Could not find poi.Please check spelling and try again",player.name)
                                else:
                                        pm("Please use the following format /poi poiname",player.name)

                    if RPOI:
                        try:
                            found = 0
                            poiname = line.split(" ")[6].rstrip(string.whitespace)
                            for player in PlayerObjectArray:
                                if playername in player.name:
                                    for poi in player.pois:
                                        if poiname == poi.split(",")[1]:
                                            player.pois.remove(poi)
                                            pm(poiname + " has been remove from list",player.name)
                                            encode_players()
                                            found = 1

                                    if found == 0:
                                        pm("Failed to remove poi",playername)
                        except:
                            pm("Failed to remove poi",playername)
                    if LISTPOI or LPOI:
                        for player in PlayerObjectArray:
                            if playername in player.name:
                                if len(player.pois) < 1:
                                    pm( "You have no pois",player.name)
                                else:
                                    pm("The following are your pois:",player.name)
                                    for poi in player.pois:
                                        pm(poi.split(",")[1] + ":"+ poi.split(",")[0],player.name)

                    if CLEARPOI:
                        for player in PlayerObjectArray:
                            if playername in player.name:
                                del player.pois[:]
                                encode_players()
                                pm("All pois have been removed",player.name)

                    if REVIVE:
                        for  player in PlayerObjectArray:
                            if playername in player.name:
                                if player.revive != "":
                                    thread.start_new_thread(delayed_teleport, ("tele " + playername + " " + player.revive + "\n",))
                                else:
                                    pm("There is no revive point",player.name)



            if LISTPLAYERS:
                    parse_players_update(line)

class telnet_connect_telnetlib(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        try:
            global out
            out = telnetlib.Telnet(HOST, PORT,5)
            out.read_until("password:")
            out.write(PASSWORD + "\n")
            thread.start_new_thread(update_player_objects_timed, ())
            while run:
                #line = out.expect(["\r\n"],5)[2].strip()
                line = out.read_until("\r\n").strip()
                if line != "":
                    readsession(line)
        except Exception as e:
            if run:
                log("unable to connect : " + e.message )

read_config()
decode_players()

try:
    t = telnet_connect_telnetlib(1, "Thread-1", 1)
    t.start()
except (KeyboardInterrupt, SystemExit):
    run = False
    sys.exit()


if GUI:
    refreshInfoList()
    root.mainloop()


