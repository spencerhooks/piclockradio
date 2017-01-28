#!/usr/bin/python2

import sched, time
import time
from phue import Bridge

TRANSITION_TIME = 4*60 # 4 minutes in seconds
DELAY_TIME = 30*60 # 30 minutes in seconds

# Create Hue bridge instance
b = Bridge('192.168.1.217')

# Create scheduler instance
s = sched.scheduler(time.time, time.sleep)

# Define the color transitions. Each list element runs for a duration defined by TRANSITION_TIME.
color_list = [{'on' : True, 'bri' : 0, 'hue' : 0}] # red
color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 15, 'hue' : 2000}) # lighter red
color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 25, 'hue' : 5000}) # red orange
color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 50, 'hue' : 9977}) # orange
color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 100, 'hue' : 9980}) # orange yellow
color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 150, 'hue' : 13390}) # yellow
color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 200, 'hue' : 15191}) # yellow white
color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 255, 'hue' : 38000}) # white

# Send the list elements to the light and wait until the transition is done before sending the next
for element in color_list:
    b.set_light(3, element)
    time.sleep(TRANSITION_TIME)
time.sleep(DELAY_TIME) # Leave the light on in the final color for DELAY_TIME
b.set_light(3,'on', False)





print(time.strftime('%H:%M:%S'))

def print_stuff():
    print(time.strftime('%H:%M:%S'))

e1 = s.enterabs(time.time()+10, 1, print_stuff, ())

print(s.queue)
s.cancel(e1)
print(s.queue)
s.run()
