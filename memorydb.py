__author__ = 'christopher'


global player_array
global last_airdrop

player_array = []
online_players = []
last_airdrop = ""
airdrops= []
import logger

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
        self.bag = ""


def player_exists(steamid):
    for person in player_array:
        if str(person.steamid) == steamid:
            return True
    return False

def player_exists_from_name(name):
    for person in player_array:
        if person.name == name:
            return True
    return False

def poi_exists(player,poiname):
    person = get_player_from_name(player)
    for poi in person.pois:
        if poiname == poi.split(",")[0]:
            return True
    return False


def add_online_player(player):
    if player not in online_players:
        online_players.append(player)

def get_online_players():
    player_list = []
    for player in online_players:
        player_list.append(player)
    return  player_list

def remove_online_player(player):
    online_players.remove(player)

def get_player_from_steamid(steamid):
    for person in player_array:
        if steamid == str(person.steamid):
            return person

def get_player_from_name(name):
    for person in player_array:
        if name == person.name:
            return person

def get_poi(player,poiname):
    person = get_player_from_name(player)
    for poi in person.pois:
        if poiname == poi.split(",")[0]:
            poilocation = poi.split(",")[1]
            return poilocation
    return ""

def add_player(name,entityid,steamid,ip,):
    logger.log("memorydb adding  new player")
    player = player_object()
    player.name = name
    player.entityid = entityid
    player.steamid = steamid
    player.ip = ip
    player_array.append(player)

def update_player(pl):
    player = get_player_from_steamid(pl.steamid)
    player.location = pl.position
    player.name = pl.name
    player.health = pl.health
    player.deaths = pl.deaths
    player.zombies = pl.zombies
    player.players= pl.players
    player.score = pl.score
    player.ping = pl.ping



def add_poi(player,name):
    person = get_player_from_name(player)
    if poi_exists(player,name):
        for poi in person.pois:
            if name == poi.split(",")[0]:
                person.pois.remove(poi)
                person.pois.append(name + "," + person.location)
    else:
        person.pois.append(name + "," + person.location)

def remove_poi(player,name):
    for person in player_array:
        if player == person.name:
            for poi in person.pois:
                if name == poi.split(",")[0]:
                    person.pois.remove(poi)


def remove_all_pois(player):
    person = get_player_from_name(player)
    del person.pois[:]

def set_player_home(player):
    person = get_player_from_name(player)
    person.home = person.location