__author__ = 'christopher'


import threading
import telnetlib
import director
import runtime
import logger



class telnet_connect_telnetlib(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        try:
            global out
            out = telnetlib.Telnet(runtime.host, runtime.port,5)
            out.read_until("password:")
            out.write(runtime.password + "\n")
            while runtime.run:
                line = out.read_until("\r\n").strip()
                if line != "":
                    try:
                        director.route(line)
                        #print line
                    except Exception as e:
                        logger.log_debug(e.message)
        except Exception as e:
            if runtime.run:
                logger.log("unable to connect : " + e.message )


def write_out(cmd):
    try:
        out.write(cmd + "\n")
    except Exception as e:
        logger.log_debug(e.message)

def initialize():
    try:
        t = telnet_connect_telnetlib(1, "Thread-1", 1)
        t.start()
    except Exception as e:
        logger.log_debug(e.message)


