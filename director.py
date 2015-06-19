__author__ = 'christopher'

import parse
import thread
import commands
import memorydb
import playerdb
import logger
import runtime
import event
import util





def route(line):
    try:
        p = parse.parse_log(line)

        if p.type == "Filtered":
            pass

        if p.type == "GMSG":
            logger.log(p.formatted_text)

        if p.type == "SystemEvent":
            if p.event == "Stats":
                runtime.time = p.time
                runtime.fps = p.fps
                runtime.heap = p.heap
                runtime.max = p.max
                runtime.chunks = p.chunks

                runtime.cgo = p.cgo
                runtime.ply = p.ply
                runtime.zom = p.zom
                runtime.ent = p.ent
                runtime.items = p.items

                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

            if p.event == "Version":
                runtime.version = p.version
                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

            if p.event == "Port":
                runtime.server_port = p.port
                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

            if p.event == "MaxPlayers":
                runtime.max_players = p.max_players
                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

            if p.event == "GameMode":
                runtime.game_mode = p.game_mode
                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

            if p.event == "World":
                runtime.world = p.world
                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

            if p.event == "GameName":
                runtime.game_name = p.game_name
                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

            if p.event == "Difficulty":
                runtime.difficulty = p.difficulty
                if runtime.gui:
                    system_event = []
                    system_event.append("SystemUpdate")
                    event.gui_event.append(system_event)

        if p.type == "GameEvent":
            if p.event == "Airdrop":
                location = util.format_coor(p.location)
                memorydb.airdrops.append(p.location)
                logger.log("Airdrop: " + location)
                playerdb.save_airdrop(p.location)
                if runtime.server:
                    commands.say("Airdrop: " + location)

        if p.type == "GameEvent":
            if p.event == "Horde":
                logger.log("Spawning Wandering Horde")
                if runtime.server:
                    commands.say("Spawning Wandering Horde")

        if p.type == "PlayerEvent":
            if p.event == "Connected":
                #logger.log("Player Connected: " + p.name)
                memorydb.add_online_player(p.name)
                player_event = []
                player_event.append("PlayerUpdate")
                event.gui_event.append(player_event)
                if runtime.server:
                    thread.start_new_thread(commands.send_motd,(p.name,))


            if p.event == "Disconnected":
                #logger.log("Player Disconnected: " + p.name)
                memorydb.remove_online_player(p.name)
                player_event = []
                player_event.append("PlayerUpdate")
                event.gui_event.append(player_event)

            if p.event == "Died":
                player = memorydb.get_player_from_name(p.name)
                player.bag = player.location
                playerdb.save_player(p.name)
                logger.log_verbose("Setting " + player.name + " revive point to: " + util.format_coor(player.location))
                logger.log(p.formatted_text)
                if runtime.server:
                    commands.pm(player.name, "Setting your revive point to: "+ util.format_coor(player.location))

            if p.event == "Update":
                memorydb.add_online_player(p.name)
                player_event = []
                player_event.append("PlayerUpdate")
                event.gui_event.append(player_event)
                if memorydb.player_exists_from_name(p.name):
                    memorydb.update_player(p)
                else:
                    memorydb.add_player(p.name, p.entityid, p.steamid, p.ip)
                    logger.log_verbose("Adding new player: " + p.name)
                    playerdb.save_player(p.name)

        if p.type == "PlayerCommand":
            if p.event == "Sethome":
                logger.log(p.formatted_text)
                memorydb.set_player_home(p.name)
                player = memorydb.get_player_from_name(p.name)
                logger.log("Setting "+util.format_coor(player.home) + " as home for " + player.name)
                playerdb.save_player(p.name)
                if runtime.server:
                    commands.pm(player.name,"Home has been set to: " + util.format_coor(player.home))


            if p.event == "Home":
                player = memorydb.get_player_from_name(p.name)
                logger.log(p.formatted_text)
                if player.home == "":
                    logger.log_verbose("No home set for: " + player.name)
                    if runtime.server:
                        commands.pm(player.name, "You need to set a home first")
                else:
                    logger.log_verbose("Teleporting "+player.name + " to " + util.format_coor(player.home))
                    if runtime.server:
                        commands.teleport(player.name,player.home)


            if p.event == "Setpoi":
                logger.log(p.formatted_text)
                player = memorydb.get_player_from_name(p.name)
                playerdb.save_poi(p.name,p.poiname,player.location)
                memorydb.add_poi(p.name,p.poiname)
                logger.log("Poi set for "+p.name +" with name "+ p.poiname +" at: " + util.format_coor(player.location))
                if runtime.server:
                    commands.pm(player.name,"Poi " + p.poiname + " set: "+ util.format_coor(player.location))


            if p.event == "Poi":
                logger.log(p.formatted_text)
                location = memorydb.get_poi(p.name,p.poiname)
                if location == "":
                    if runtime.server:
                        commands.pm(p.name,"No poi with that name.")
                else:
                    logger.log("Teleporting "+p.name + " to " + util.format_coor(location))
                    if runtime.server:
                        commands.teleport(p.name,location)


            if p.event == "Listpoi":
                logger.log(p.formatted_text)
                if runtime.server:
                    player = memorydb.get_player_from_name(p.name)
                    if len(player.pois) == 0:
                        commands.pm(p.name,"No pois to list")
                    for poi in player.pois:
                        name = poi.split(",")[0]
                        location = poi.split(",")[1]
                        commands.pm(player.name,name + ": " + util.format_coor(location))

            if p.event == "Removepoi":
                logger.log(p.formatted_text)
                if memorydb.poi_exists(p.name,p.poiname):
                    memorydb.remove_poi(p.name,p.poiname)
                    playerdb.delete_poi(p.name,p.poiname)
                    if runtime.server:
                        commands.pm(p.name,"Poi " + p.poiname+ " has been removed")

                else:
                    if runtime.server:
                        commands.pm(p.name,"No poi with that name")

            if p.event == "Clearpoi":
                logger.log(p.formatted_text)
                memorydb.remove_all_pois(p.name)
                playerdb.delete_all_poi(p.name)
                if runtime.server:
                    commands.pm(p.name,"All pois have been removed")

            if p.event == "Killme":
                logger.log(p.formatted_text)
                if runtime.server:
                    commands.kill_player(p.name)

            if p.event == "Help":
                logger.log(p.formatted_text)
                if runtime.server:
                    commands.help(p.name)

            if p.event == "Bag":
                logger.log(p.formatted_text)
                if runtime.server:
                    player = memorydb.get_player_from_name(p.name)
                    if player.bag != "":
                        commands.teleport(p.name,player.bag)

            if p.event == "Goto":
                logger.log(p.formatted_text)
                if runtime.server:
                    if memorydb.player_exists_from_name(p.othername):
                        commands.teleport(p.name,p.othername)
                    else:
                        commands.pm(p.name,"Player does not exist: " + p.othername)

            if p.event == "Where":
                logger.log(p.formatted_text)
                if runtime.server:
                    player = memorydb.get_player_from_name(p.name)
                    commands.pm(p.name,"Current location: " + util.format_coor(player.location))

            if p.event == "Drop":
                logger.log(p.formatted_text)
                if runtime.server:
                    for drop in memorydb.airdrops:
                        if util.is_coor_formatted(drop):
                            commands.pm(p.name,"Airdrop: " + drop)
                        else:
                            commands.pm(p.name,"Airdrop: " + util.format_coor(drop))

            if p.event == "Claim":
                logger.log(p.formatted_text)
                found = 0
                if runtime.server:
                    player = memorydb.get_player_from_name(p.name)
                    obj1 = player.location
                    for drop in memorydb.airdrops:
                        if util.in_radius(obj1,drop,runtime.drop_claim_radius):
                            memorydb.airdrops.remove(drop)
                            playerdb.delete_airdrop(drop)
                            if util.is_coor_formatted(drop):
                                commands.pm(p.name,"You have claimed the airdrop at: " + str(drop))
                            else:
                                commands.pm(p.name,"You have claimed the airdrop at: " + str(util.format_coor(drop)))
                            found = 1
                    if found == 0:
                        commands.pm(p.name,"You need to be in a " + str(runtime.drop_claim_radius) + " block radius of an airdrop to claim")

        if p.type == "":
            logger.log_verbose(p.formated_text)

    except Exception as e:
        print(e.message)