__author__ = 'christopher'



from Tkinter import *
from ttk import *
import memorydb
import telconn
import threading
import logger
import event
import runtime
import time
import config



selected_player = ""

def toggle_verbose():
    if verbose_chk.get() == 1:
        runtime.verbose = True
    else:
        runtime.verbose = False

def toggle_debug():
    if debug_chk.get() == 1:
        runtime.debug = True
    else:
        runtime.debug = False

def toggle_server():
    if server_chk.get() == 1:
        runtime.server = True
    else:
        runtime.server = False

def save_settings():
    runtime.host = host_input.get()
    runtime.port = port_input.get()
    config.save_config()
    
root = Tk()
root.title("7dtd Telnet Client")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
note = Notebook(root)
note.columnconfigure(0, weight=1)
note.rowconfigure(0, weight=1)
note.grid(sticky=NSEW)

#console_tab stuff here
console_tab = Frame(note)
console_tab.columnconfigure(0, weight=1)
console_tab.columnconfigure(1, weight=1)
console_tab.rowconfigure(0, weight=1)
textbox = Text(console_tab, height=20, width=80)
textbox.grid(row=0, column=0, sticky=NSEW, columnspan=2)
textbox.columnconfigure(0, weight=1)
textbox.rowconfigure(0, weight=1)
playerbox = Text(console_tab, height=20, width=20)
playerbox.grid(row=0, column=3, sticky=N+S)
commandLabel = Label(console_tab, width=10, text="Command:")
commandLabel.grid(row=1, column=0, sticky=W)
input = Entry(console_tab, width=80)
input.grid(row=1, column=1, sticky=E+W, columnspan=3)

#players_tab stuff here
players_tab = Frame(note)
players_tab.columnconfigure(0, weight=1)
players_tab.rowconfigure(0, weight=1)
playerlist = Listbox(players_tab, height=20, width=20)
playerlist.grid(row=0,column=1,sticky=N+S)
infobox = Text(players_tab, height=10, width=80)
infobox.grid(row=0, column=0, sticky=N+E+W)

#settings_tab stuff here
settings_tab = Frame(note)
settings_tab.rowconfigure(0, weight=1)
settings_tab.rowconfigure(1, weight=1)
settings_tab.rowconfigure(2, weight=1)
settings_tab.rowconfigure(3, weight=1)
settings_tab.rowconfigure(4, weight=1)
settings_tab.rowconfigure(5, weight=1)
settings_tab.rowconfigure(6, weight=1)

verbose_chk = IntVar()
verbose_checkbox = Checkbutton(settings_tab,text = "Verbose Logging",command = toggle_verbose,variable=verbose_chk)
verbose_checkbox.grid(row=0, column=0, sticky=W)
if runtime.verbose:
    verbose_chk.set(1)

debug_chk = IntVar()
debug_checkbox = Checkbutton(settings_tab,text = "Debug Logging",command = toggle_debug,variable=debug_chk)
debug_checkbox.grid(row=1, column=0, sticky=W)
if runtime.debug:
    debug_chk.set(1)

server_chk = IntVar()
server_checkbox = Checkbutton(settings_tab,text = "Server",command = toggle_server,variable=server_chk)
server_checkbox.grid(row=2, column=0, sticky=W)
if runtime.server:
    server_chk.set(1)

motd_label = Label(settings_tab, width=10, text="MOTD: ")
motd_label.grid(row=3, column=0)
motd_input = Entry(settings_tab, width=30)
motd_input.grid(row=3, column=1, sticky=W)
motd_input.insert(0,runtime.motd)

host_label = Label(settings_tab, width=10, text="Host: ")
host_label.grid(row=4, column=0)
host_input = Entry(settings_tab, width=15)
host_input.grid(row=4, column=1, sticky=W)
host_input.insert(0,runtime.host)

port_label = Label(settings_tab, width=10, text="Port: ")
port_label.grid(row=5, column=0)
port_input = Entry(settings_tab, width=15)
port_input.grid(row=5, column=1, sticky=W)
port_input.insert(0,runtime.port)





save_btn = Button(settings_tab,text = "Save",command = save_settings)
save_btn.grid(row=6, column=0, sticky=E)
Label(settings_tab).grid(row=7,column=0)

#system_tab stuff here
system_tab = Frame(note)

time_var = StringVar()
time_var.set("Time: 0m")
time_label = Label(system_tab, width=15, textvariable = time_var)
time_label.grid(row=0, column=0)

fps_var = StringVar()
fps_var.set("FPS: 0")
fps_label = Label(system_tab, width=15, textvariable = fps_var)
fps_label.grid(row=1, column=0)

heap_var = StringVar()
heap_var.set("Heap: 0MB")
heap_label = Label(system_tab, width=15, textvariable = heap_var)
heap_label.grid(row=2, column=0)

max_var = StringVar()
max_var.set("Max: 0MB")
max_label = Label(system_tab, width=15, textvariable = max_var)
max_label.grid(row=3, column=0)

chunks_var = StringVar()
chunks_var.set("Chunks: 0")
chunks_label = Label(system_tab, width=15, textvariable = chunks_var)
chunks_label.grid(row=4, column=0)

cgo_var = StringVar()
cgo_var.set("CGO: 0M")
cgo_label = Label(system_tab, width=15, textvariable = cgo_var)
cgo_label.grid(row=5, column=0)

ply_var = StringVar()
ply_var.set("PLY: 0")
ply_label = Label(system_tab, width=15, textvariable = ply_var)
ply_label.grid(row=6, column=0)

zom_var = StringVar()
zom_var.set("Zom: 0")
zom_label = Label(system_tab, width=15, textvariable = zom_var)
zom_label.grid(row=7, column=0)

ent_var = StringVar()
ent_var.set("ENT: 0")
ent_label = Label(system_tab, width=15, textvariable = ent_var)
ent_label.grid(row=8, column=0)

items_var = StringVar()
items_var.set("Items: 0")
items_label = Label(system_tab, width=15,  textvariable = items_var)
items_label.grid(row=9, column=0)

version_var = StringVar()
version_var.set("Version: 0")
version_label = Label(system_tab, width=30,  textvariable = version_var)
version_label.grid(row=0, column=1)

port_var = StringVar()
port_var.set("Port: 0")
port_label = Label(system_tab, width=30,  textvariable = port_var)
port_label.grid(row=1, column=1)

max_players_var = StringVar()
max_players_var.set("Max Players: 0")
max_players_label = Label(system_tab, width=30,  textvariable = max_players_var)
max_players_label.grid(row=2, column=1)

game_mode_var = StringVar()
game_mode_var.set("Game Mode: 0")
game_mode_label = Label(system_tab, width=30,  textvariable = game_mode_var)
game_mode_label.grid(row=3, column=1)

world_var = StringVar()
world_var.set("World: 0")
world_label = Label(system_tab, width=30,  textvariable = world_var)
world_label.grid(row=4, column=1)

game_name_var = StringVar()
game_name_var.set("Game Name: 0")
game_name_label = Label(system_tab, width=30,  textvariable = game_name_var)
game_name_label.grid(row=5, column=1)

difficulty_var = StringVar()
difficulty_var.set("Difficulty: 0")
difficulty_label = Label(system_tab, width=30,  textvariable = difficulty_var)
difficulty_label.grid(row=6, column=1)




def show_player_info(name):
    infobox.delete("1.0", END)
    player = memorydb.get_player_from_name(name)
    infobox.insert(END, "Name:"+ player.name+ "\n")
    infobox.insert(END, "SteamID:"+ str(player.steamid)+ "\n")
    infobox.insert(END, "IP:"+ player.ip+ "\n")
    infobox.insert(END, "Last Location:"+ player.location+ "\n")

def addInfo(info):
	textbox.insert(END,info + '\n')
	textbox.see(END)

def refreshPlayerList():
    if int(playerbox.index('end-1c').split(".")[0])-1 != len(memorydb.online_players):
        playerbox.delete("1.0", END)
        online_players = memorydb.get_online_players()
        for player in online_players:
            playerbox.insert("1.0",player+ "\n")

def refreshInfoList():
    if int(playerlist.index('end')) != len(memorydb.player_array):
        playerlist.delete(0, END)
        for player in memorydb.player_array:
            playerlist.insert(1, player.name)

def func(event):
    cmd = input.get()
    telconn.write_out(cmd)
    logger.log("Command sent: " + cmd)
    input.delete(0, END)

def listclick(e):
    show_player_info(str(playerlist.get(playerlist.curselection())))

def set_motd(e):
    runtime.motd = motd_input.get()

def refresh_system_stats():
    time_var.set("Time: " + str(runtime.time))
    fps_var.set("FPS: " + str(runtime.fps))
    heap_var.set("Heap: " + str(runtime.heap))
    max_var.set("Max: " + str(runtime.max))
    chunks_var.set("Chunks: " + str(runtime.chunks))
    cgo_var.set("CGO: " + str(runtime.cgo))
    ply_var.set("PLY: " + str(runtime.ply))
    zom_var.set("Zom: " + str(runtime.zom))
    ent_var.set("Ent: " + str(runtime.ent))
    items_var.set("Items: " + str(runtime.items))

    version_var.set("Version: " + str(runtime.version))
    port_var.set("Port: " + runtime.server_port )
    max_players_var.set("Max Players: " + runtime.max_players)
    game_mode_var.set("Game Mode: " +runtime.game_mode )
    world_var.set("World: " +runtime.world )
    game_name_var.set("Game Name: " + runtime.game_name)
    difficulty_var.set("Difficulty: " + runtime.difficulty)


def handler():
    runtime.run = False
    root.destroy()
    telconn.write_out("exit")


input.bind('<Return>', func)
note.add(console_tab, text="Console", compound=TOP)

playerlist.bind('<<ListboxSelect>>', listclick)
note.add(players_tab, text = "Players")

motd_input.bind('<KeyRelease>',set_motd)

note.add(settings_tab, text = "Settings")

note.add(system_tab, text = "System")

root.protocol("WM_DELETE_WINDOW", handler)




def update():
    while runtime.run:
        time.sleep(.1)
        for event_record in event.gui_event: # this needs to be fixed but works for now
            if event.gui_event[-1][0] == "Log":
                addInfo(str(event.gui_event[-1][1]))
                event.gui_event.pop()

            if event_record[0] == "PlayerUpdate":
                refreshPlayerList()
                refreshInfoList()
                event.gui_event.pop()

            if event_record[0] == "SystemUpdate":
                refresh_system_stats()
                event.gui_event.pop()




def start():
    if runtime.gui:
        refreshInfoList()
        threading._start_new_thread(update, ())
        root.mainloop()


