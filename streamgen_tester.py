#!/usr/bin/python

from streamgen import Player
import time

p = Player()

p.play(duration=5)

print ("playing stuff")
print (p.is_playing())

time.sleep(6)
p.stop()

print (p.is_playing())
