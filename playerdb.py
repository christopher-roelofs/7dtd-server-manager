__author__ = 'christopher'


import memorydb
import sqlitedb as db


def save_player(name):
    player = memorydb.get_player_from_name(name)
    db.save_player(player)

def save_poi(name,poiname,location):
    player = memorydb.get_player_from_name(name)
    db.save_poi(player,poiname,location)

def delete_poi(name,poiname):
    player = memorydb.get_player_from_name(name)
    db.delete_poi(player,poiname)

def delete_all_poi(name):
    player = memorydb.get_player_from_name(name)
    db.delete_all_poi(player)

def save_airdrop(drop):
    db.save_airdrop(drop)

def delete_airdrop(drop):
    db.delete_airdrop(drop)