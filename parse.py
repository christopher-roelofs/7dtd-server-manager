__author__ = 'christopher'

#parses the log and returns a parsed_log object

import re
import string
import memorydb
import logger
from time import strftime




class ParsedLog(object):
    def __init__(self):
        self.type = ""
        self.event = ""
        self.full_text = ""


def parse_log(line):
    pl = ParsedLog()
    pl.full_text = line

    INF = re.search("INF", line)
    WRN = re.search("WRN", line)
    ERR = re.search("ERR", line)
    LISTPLAYERS = re.search("([0-9][.]\sid=)", line)
    F2 = re.search("Total of", line) #message from player, system or admin

    VERSION = re.search("Server version:",line)
    PORT = re.search("Server port:",line)
    MAXP = re.search("Max players:",line)
    GAMEMODE = re.search("Game mode:",line)
    WORLD = re.search("World:",line)
    GAMENAME = re.search("Game name:",line)
    DIFFICULTY = re.search("Difficulty:",line)



    if INF:
        seperated_line = line.split(" ")
        F1 = re.search("Executing command", line) #message from player, system or admin
        GMSG = re.search("GMSG", line) #message from player, system or admin
        CONNECTED = re.search("Player connected", line) #message from player, system or admin
        DICONNECTED = re.search("Player disconnected", line) #message from player, system or admin
        TIME = re.search("INF Time", line)
        HORDE = re.search("INF Spawning Wandering Horde",line)
        AIRDROP = re.search("AIAirDrop: Spawned supply crate",line)



        if CONNECTED:
            player = seperated_line[6].split("=")[1][:-1]
            steamid = seperated_line[7].split("=")[1][:-1]
            pl.type = "PlayerEvent"
            pl.event = "Connected"
            pl.name = player
            pl.steamid = steamid
            return pl

        elif DICONNECTED:
            player = seperated_line[8].split("=")[1][:-1].replace("'","")
            steamid = seperated_line[7].split("=")[1][:-1].replace("'","")
            pl.type = "PlayerEvent"
            pl.event = "Disconnected"
            pl.name = player
            pl.steamid = steamid
            return pl

        elif TIME:
            try:
                pl.type = "SystemEvent"
                pl.event = "Stats"
                pl.time = seperated_line[4]
                pl.fps = seperated_line[6]
                pl.heap = seperated_line[8]
                pl.max = seperated_line[10]
                pl.chunks = seperated_line[12]
                pl.cgo = seperated_line[14]
                pl.ply = seperated_line[16]
                pl.zom = seperated_line[18]
                pl.ent = seperated_line[20] + " " + seperated_line[21]
                pl.items = seperated_line[23]
                return pl
            except Exception as e:
                return pl
                logger.log_debug("Error parsing stats update: "+e.message)

        elif AIRDROP:
            try:
                pl.type = "GameEvent"
                pl.event = "Airdrop"
                seperated_line = line.replace("(","").replace(")","").replace(",","").split()
                pl.x = seperated_line[8]
                pl.y = seperated_line[10]
                pl.z = seperated_line[9]
                pl.location = seperated_line[8] + " " + seperated_line[9] + " " + seperated_line[10]
                return pl

            except Exception as e:
                logger.log(line)
                logger.log_debug("Error parsing airdrop info")
                return pl

        elif HORDE:
            pl.type = "GameEvent"
            pl.event = "Horde"
            return pl

        elif F1:
            pl.type = "Filtered"
            return pl



        elif GMSG:
            player = seperated_line[4][:-1]
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
            BAG = re.search("/bag",line)
            DIED = re.search("died",line)
            WHERE = re.search("/where",line)
            DROP = re.search("/drop",line)
            CLAIM = re.search("/claim",line)

            if DIED:
                try:
                    player = seperated_line[5]
                    pl.formatted_text = " ".join(pl.full_text.split()[4:])
                    pl.type = "PlayerEvent"
                    pl.event = "Died"
                    pl.name = player
                    return pl
                except Exception as e:
                    logger.log("Error parsing died system message: "+ e.message)
                    return pl

            elif HELP:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Help"
                pl.name = player
                return pl

            elif SETHOME:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Sethome"
                pl.name = player
                return pl

            elif HOME:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Home"
                pl.name = player
                return pl

            elif SETPOI:
                try:
                    pl.formatted_text = " ".join(pl.full_text.split()[4:])
                    poiname = seperated_line[6]
                    pl.type = "PlayerCommand"
                    pl.event = "Setpoi"
                    pl.name = player
                    pl.poiname = poiname
                    return pl
                except Exception as e:
                    logger.log_verbose("Error parsing setpoi command: "+ e.message)
                    return pl

            elif POI:
                try:
                    pl.formatted_text = " ".join(pl.full_text.split()[4:])
                    poiname = seperated_line[6]
                    pl.type = "PlayerCommand"
                    pl.event = "Poi"
                    pl.name = player
                    pl.poiname = poiname
                    return pl
                except Exception as e:
                    logger.log_verbose("Error parsing poi command: "+ e.message)
                    return pl


            elif LISTPOI or LPOI:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Listpoi"
                pl.name = player
                return pl

            elif RPOI:
                try:
                    pl.formatted_text = " ".join(pl.full_text.split()[4:])
                    poiname = seperated_line[6]
                    pl.type = "PlayerCommand"
                    pl.event = "Removepoi"
                    pl.name = player
                    pl.poiname = poiname
                    return pl
                except Exception as e:
                    logger.log("Error parsing rpoi command: "+ e.message)
                    return pl

            elif CLEARPOI:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Clearpoi"
                pl.name = player
                return pl

            elif GOTO:
                try:
                    pl.formatted_text = " ".join(pl.full_text.split()[4:])
                    othername = seperated_line[6]
                    pl.type = "PlayerCommand"
                    pl.event = "Goto"
                    pl.name = player
                    pl.othername = othername
                    return pl
                except Exception as e:
                    logger.log("Error parsing goto command: "+ e.message)
                    return pl

            elif BAG:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Bag"
                pl.name = player
                return pl

            elif KILLME:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Killme"
                pl.name = player
                return pl

            elif WHERE:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Where"
                pl.name = player
                return pl

            elif DROP:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Drop"
                pl.name = player
                return pl

            elif CLAIM:
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                pl.type = "PlayerCommand"
                pl.event = "Claim"
                pl.name = player
                #pl.drop = seperated_line[6] +" " + seperated_line[7] + " " + seperated_line[8] + " " + seperated_line[9] + " " + seperated_line[10]
                return pl

            else:
                pl.type = "GMSG"
                pl.event = "Msg"
                pl.formatted_text = " ".join(pl.full_text.split()[4:])
                return pl

        else:
            pl.formated_text = " ".join(pl.full_text.split()[3:])
            return pl

    elif LISTPLAYERS:
        try:
            position = str(int(round(float(line.split(" ")[3].replace("pos=(", "").replace(",", ""))))) + " " + str(int(round(float(line.split(" ")[4].replace(",", ""))))) + " " + str(int(round(float(line.split(" ")[5].replace("),", "")))))
            entityid = line.split(",")[0].split("=")[1]
            name = line.split(",")[1].replace(" ", "")
            health = line.split(",")[9].split("=")[1]
            deaths = line.split(",")[10].split("=")[1]
            zombies = line.split(",")[11].split("=")[1]
            players = line.split(",")[12].split("=")[1]
            score = line.split(",")[13].split("=")[1]
            steamid = line.split(",")[15].split("=")[1]
            ip = line.split(",")[16].split("=")[1]
            ping = line.split(",")[17].split("=")[1].rstrip(string.whitespace)

            pl.type = "PlayerEvent"
            pl.event = "Update"
            pl.entityid = entityid
            pl.position = position
            pl.name = name
            pl.health = health
            pl.deaths = deaths
            pl.zombies = zombies
            pl.players= players
            pl.score = score
            pl.steamid = steamid
            pl.ip = ip
            pl.ping = ping
            return pl


        except Exception as e:
            logger.log_debug("Error parsing player update: "+ e.message)
            return pl

    elif WRN:
        pl.formated_text = " ".join(pl.full_text.split()[3:])
        return pl

    elif ERR:
        pl.formated_text = " ".join(pl.full_text.split()[3:])
        return pl

    elif F2:
        pl.type = "Filtered"
        return pl

    elif VERSION:
        pl.type = "SystemEvent"
        pl.event = "Version"
        pl.version = line.split()[3] + " " + line.split()[4] + " "+ line.split()[5]
        return pl

    elif PORT:
        pl.type = "SystemEvent"
        pl.event = "Port"
        pl.port = line.split()[2]
        return pl

    elif MAXP:
        pl.type = "SystemEvent"
        pl.event = "MaxPlayers"
        pl.max_players = line.split()[2]
        return pl

    elif GAMEMODE:
        pl.type = "SystemEvent"
        pl.event = "GameMode"
        pl.game_mode = line.split()[2]
        return pl

    elif WORLD:
        pl.type = "SystemEvent"
        pl.event = "World"
        pl.world = line.split()[1]
        return pl

    elif GAMENAME:
        pl.type = "SystemEvent"
        pl.event = "GameName"
        pl.game_name = line.split()[2]
        return pl

    elif DIFFICULTY:
        pl.type = "SystemEvent"
        pl.event = "Difficulty"
        pl.difficulty = line.split()[1]
        return pl

    else:
        pl.formated_text = pl.full_text
        return pl





