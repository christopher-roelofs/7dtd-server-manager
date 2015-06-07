#!/usr/bin/python


import gui
import telconn
import threading
import commands




telconn.initialize()
threading._start_new_thread(commands.update_player_objects_timed, ())
gui.start()




