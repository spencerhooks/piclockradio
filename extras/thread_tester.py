#!/usr/bin/python

from subprocess import Popen
import os, time
from threading import Thread

# def myplayer():
#     global p
#     p = Popen(['play', '-q', '-n', 'synth', 'brownnoise'])
#     print "running thread"

t = Thread(target = do_stuff)
t.daemon = False
t.start()

def do_stuff():
    print
