#!/usr/bin/env python
""" Drone Pilot - Control of MRUAV """
""" mw-logdata.py: Script that logs data from a vehicle with MultiWii flight controller and a MoCap system."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2015 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import time, threading
from modules.pyMultiwii import MultiWii
import modules.UDPserver as udp
import modules.utils as utils

# MRUAV initialization
#vehicle = MultiWii("/dev/tty.usbserial-A801WZA1")
vehicle = MultiWii("/dev/ttyUSB0")

# Function to update commands and attitude to be called by a thread
def logit():
    global vehicle
    """
    Function to manage data, print it and save it in a csv file, to be run in a thread
    """
    while True:
        if udp.active:
            print "UDP server is active..."
            break
        else:
            print "Waiting for UDP server to be active..."
        time.sleep(0.5)

    try:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
        f = open("logs/"+"mw-"+st, "w")
        logger = csv.writer(f)
        logger.writerow(('timestamp','roll','pitch','yaw','proll','ppitch','throttle','pyaw','x','y','z'))
        while True:
            elapsed = time.time()
            vehicle.getData(MultiWii.ATTITUDE)
            vehicle.getData(MultiWii.RC)
            print "Time to ask two commands -> %0.2f" % time.time()-elapsed 
            print vehicle.attitude
            print vehicle.rcrcChannels

            # Save log
            #logger.writerow((time.time(), \
            #                 vehicle.attitude['angx'], vehicle.attitude['angy'], vehicle.attitude['heading'], \
            #                 vehicle.rcChannels['roll'], vehicle.rcChannels['pitch'], vehicle.rcChannels['throttle'], vehicle.rcChannels['yaw'], \
            #                 udp.message[5], udp.message[4], udp.message[6] ))
            time.sleep(0.01) # 100hz 

    except Exception,error:
        print "Error in logit thread: "+str(error)
        f.close()

if __name__ == "__main__":
    try:
        logThread = threading.Thread(target=logit)
        logThread.daemon=True
        logThread.start()
        udp.startTwisted()
    except Exception,error:
        print "Error on main: "+str(error)
        vehicle.ser.close()
    except KeyboardInterrupt:
        print "Keyboard Interrupt, exiting."
        exit()