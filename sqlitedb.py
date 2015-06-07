import sqlite3
import os

import memorydb
import logger


db_filename = 'players.db'
db_exists = os.path.exists(db_filename)

def log(info):
    print info



def create_database():
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE Players(Name TEXT,Steamid INT PRIMARY KEY,Entityid INT,IP TEXT,Home TEXT,Zombies INT,Players INT,Score INT,Bag TEXT)")

            cur.execute("CREATE TABLE Poi(Player TEXT,Steamid INT,Name TEXT,Location TEXT,Uniqueid TEXT PRIMARY KEY)")

            cur.execute("CREATE TABLE Airdrop(Airdrop TEXT PRIMARY KEY)")
            conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.log("Failed to create database " + e.message)

    finally:
        if conn:
            conn.close()
            logger.log("Creating database")


def load_players():
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Players")
            rows = cur.fetchall()
            logger.log("Loading players...")
            for row in rows:
                player = memorydb.player_object()
                player.name = row[0]
                player.steamid = row[1]
                player.entityid = row[2]
                player.ip = row[3]
                player.home = str(row[4])
                player.zombies = row[5]
                player.players = row[6]
                player.score = row[7]
                player.bag = str(row[8])
                cur.execute("SELECT * FROM Poi WHERE Steamid = " + str(player.steamid))
                pois = cur.fetchall()
                for poi in pois:
                    player.pois.append(str(poi[2])+","+str(poi[3]))
                memorydb.player_array.append(player)
                logger.log("---------------------")
                logger.log("Name: " + player.name)
                logger.log("Steamid: " + str(player.steamid))
                logger.log("IP: " + str(player.ip))
                logger.log(" ")

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger(e)

    finally:
        if conn:
            conn.close()

def load_airdrops():
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Airdrop")
            rows = cur.fetchall()
            logger.log("Loading airdrops...")
            for row in rows:
                drop = str(row[0])
                memorydb.airdrops.append(drop)
                logger.log_verbose(drop)

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger(e)

    finally:
        if conn:
            conn.close()


def save_player(player):
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            name = player.name
            steamid = player.steamid
            entityid = player.entityid
            ip = player.ip
            home = player.home
            zombies = player.zombies
            players = player.players
            score = player.score
            bag = player.bag
            try:
                cur.execute("INSERT INTO Players(Name,Steamid,Entityid,IP,Home,Zombies,Players,Score,Bag) VALUES (?,?,?,?,?,?,?,?,?)",(name,steamid,entityid,ip,home,zombies,players,score,bag))
                logger.log_verbose("Creating new player record")
                conn.commit()
            except Exception as e:
                if "UNIQUE constraint failed" in e.message:
                    logger.log_debug("Player record exists,updatig it")
                    cur.execute("UPDATE Players SET Name = ?, IP = ?,Home= ?,Zombies = ?,Players =?,Score=?,Bag=? WHERE Steamid =? ",(name,ip,home,zombies,players,score,bag,steamid))
                    conn.commit()
                else:
                    logger.log_debug(e.message)

    except Exception as e:
        logger.log_debug(e.message)


def save_poi(player,poiname,location):
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            name = player.name
            steamid = player.steamid
            try:
                cur.execute("INSERT INTO Poi (Player,Steamid,Name,Location,Uniqueid) VALUES (?,?,?,?,?)",(name,steamid,poiname,location,str(steamid)+poiname))
                logger.log_verbose("Creating new poi record")
                conn.commit()
            except Exception as e:
                if "UNIQUE constraint failed" in e.message:
                    cur.execute("UPDATE Poi SET Player = ?, Steamid = ?,Name= ?,Location = ? WHERE Uniqueid = ? ",(name,steamid,poiname,location,str(steamid)+poiname))
                    logger.log_verbose("Updating poi record")
                    conn.commit()
    except Exception as e:
        logger.log_debug(e.message)

def save_airdrop(drop):
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Airdrop (Airdrop) VALUES (?)",(drop,))
                logger.log_verbose("Creating new airdrop record")
                conn.commit()
            except Exception as e:
                if "UNIQUE constraint failed" in e.message:
                    cur.execute("UPDATE Airdrop SET Airdrop = ?",(drop,))
                    logger.log_verbose("Updating airdrop record")
                    conn.commit()

    except Exception as e:
        logger.log_debug(e.message)

def delete_poi(player,poiname):
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            name = player.name
            steamid = player.steamid
            try:
                cur.execute("DELETE from Poi where Uniqueid = ? ",(str(steamid)+poiname,))
                logger.log_verbose("Deleting poi record " + poiname + " for "+ name)
                conn.commit()
            except Exception as e:
                logger.log_debug(e.message)

    except Exception as e:
        logger.log_debug(e.message)

def delete_airdrop(drop):
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE from Airdrop where Airdrop = ? ",(drop,))
                logger.log_verbose("Deleting airdrop record " + drop)
                conn.commit()
            except Exception as e:
                logger.log_debug(e.message)

    except Exception as e:
        logger.log_debug(e.message)

def delete_all_poi(player):
    try:
        conn = sqlite3.connect(db_filename)
        with conn:
            cur = conn.cursor()
            name = player.name
            steamid = player.steamid
            try:
                cur.execute("DELETE FROM Poi WHERE Steamid = ? ",(str(steamid),))
                logger.log_verbose("Deleteing all poi records for " + name)
                conn.commit()
            except Exception as e:
                logger.log_debug(e.message)

    except Exception as e:
        logger.log_debug(e.message)



if not db_exists:
    create_database()
load_players()
load_airdrops()


