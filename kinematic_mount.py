#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:24:21 2019
@institute: Centro de Investigaciones en \'Optica A.C.
@group: Applied Science Terahertz Group
@author: Jorge Ludwig Regalado de la Rosa
"""
import serial, sys, time, struct
#microstep size = 0.000086 °
#range -5.27 to +5.27 °; -62000:62000
def send(device, command, data):
    # send a packet using the specified device number, command number, and data
    # The data argument is optional and defaults to zero
    packet = struct.pack('<BBl', device, command, data)
    ser.write(packet)
 
def receive():
    # return 6 bytes from the receive buffer
    # there must be 6 bytes to receive (no error checking)
    r = [0,0,0,0,0,0]
    for i in range (6):
        r[i] = ord(ser.read(1))
    return r
try:
   ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
except:
   print("Error opening com port. Quitting.")
   sys.exit(0)
print("Opening " + ser.portstr)
device = 2
command = 20
data = 0
print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
send(device, command, data)
time.sleep(1) # wait for 1 second

try:
   reply = receive()
   # Reply data is calculated from all reply bytes
   replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
   if reply[5] > 127:
      replyData -= 256.0**4

   print("Receiving reply " + str(reply))
   print("Device number: " + str(reply[0]))
   print("Command number: " +  str(reply[1]))
   print("Reply: " + str(replyData)) # Supply voltage must be divided by ten
except:
   print("No reply was received.")

print("Closing " + ser.portstr)
ser.close()
