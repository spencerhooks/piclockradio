#!/usr/bin/python2

from threading import Thread, Timer
import time
from phue import Bridge

TRANSITION_TIME = 3
DELAY_TIME = 5

# change to your IP address
b = Bridge('192.168.1.217')

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
# for element in color_list:
#     b.set_light(3, element)
#     time.sleep(TRANSITION_TIME)
# time.sleep(DELAY_TIME) # Leave the light on in the final color for DELAY_TIME
# b.set_light(3,'on', False)

counter = 0

def get_input():
    while True:
        s = raw_input('-->')
        print("got input")
        if s == "stop":
            global t2
            b.set_light(3, 'on', False)
            print t2.is_alive()
            t2.cancel()
            break

t = Thread(target = get_input)
t.daemon = False
t.start()

def stop_light():
    while b.get_light(3, 'on'):
        b.set_light(3, 'on', False)

def run_light():
    global counter

    if counter <= len(color_list)-1:
        print counter, len(color_list)
        b.set_light(3, (color_list[counter]))
        print(color_list[counter])
        global t2
        t2 = Timer(TRANSITION_TIME, run_light)
        t2.daemon = False
        t2.start()
    elif counter == len(color_list):
        print "turning off in this time through"
        t2 = Timer(DELAY_TIME, stop_light)
        t2.daemon = False
        t2.start()
    counter += 1

t2 = Thread(target = run_light)
t2.daemon = False
t2.start()
