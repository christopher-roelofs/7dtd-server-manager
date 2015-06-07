__author__ = 'christopher'

import runtime
import event




def add_log(info):
    print(info)
    if runtime.gui:
        log_event = []
        log_event.append("Log")
        log_event.append(info)
        event.gui_event.insert(0,log_event)


def log_verbose(info):
    if runtime.verbose:
        add_log(info)

def log_debug(info):
    if runtime.debug:
        add_log(info)

def log(info):
    add_log(info)



