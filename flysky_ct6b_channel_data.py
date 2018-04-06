#!/usr/bin/env python
import time
import serial
from message import *


def read_msg(serialdev):
	import select

	msglen = 0
	msg = None
	s = 0
	while True:
		try:
			c = ord(serialdev.read(1))
		except select.error: #normal syscal interrupt
			continue
		if s == 0:
			s = (c == MSGSTART)
		elif s == 1:
			if c in MSGMAP:
				s = 2
				msg = [c] + [0]*(MSGMAP[c]-1)
				msglen = 1
			else: #we are not in sync, reset
				s = 0
		else:
			msg[msglen] = c
			msglen += 1
			if msglen >= MSGMAP[msg[0]]:
				if checksum(msg):
					return msg
				s = 0

ser = serial.Serial(
               port='/dev/ttyUSB0',
               baudrate = 115200,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
      )

while 1:
    msg=read_msg(ser)
    print msg
    for i, channel in enumerate(channels):
        data = channel.read(msg)
        print data
