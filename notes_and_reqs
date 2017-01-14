# Notes and Requirements #

## Known Issues ##
1. The volume slider has a bug where holding and dragging (but not letting go) causes a visual problem because the slider position is updated by javascript from the previous position in json file.
2. 

## List of Requirements ##
1. Sunrise light (control external Hue light)
2. Snooze
3. Brownian noise playback
4. Play NPR
5. Play NPR as alarm
6. Alarm ON/OFF
7. Sleep mode for the light (light comes on and fades out through duration of 30 min)
8. Clock display
9. Internet time (including automatic DST)
10. Display alarm status (on/off)
11. Power switch (if shutdown needed before pulling the plug)
12. Volume
13. Backup battery with auto shutdown after battery dies (save state and resume upon power up)
14. Control via MQTT
15. Large snooze button
16. Sunrise light should only come on if needed based on alarm time and time of sunrise
17. Should be set for weekdays with a manual setting to turn on for the next day
18. Physical controls for basic settings with others via a website

## Basic Features Needed: ##
1. Hue control
2. Stream KQED audio stream (m3u/mp3): mpg123 seems to work well
3. Loop local audio file noisegen module complete. Not looping file, but using noise generation.
4. Physical input switches
5. Alarm display
6. MQTT
7. Web server
8. Volume control: use alsaauio and device 'Power Amplifier'

## Notes: ##
1. Use pygame to loop brownian noise:
  ```python
  import pygame
  pygame.init()
  pygame.mixer.music.load('brownnoise2.mp3')
  pygame.mixer.music.play(-1)```
2. Better still, use sox to generate brown noise (no looping)
  1. See script
  2. There's a python wrapper, but it doesn't add much in this case and is blocking when it calls the sox player
3. Setting volume:
  ```python
  import alsaaudio
  m = alsaaudio.Mixer()   # defined alsaaudio.Mixer to change volume. Default device is Mixer. Chip needs to use 'Power Amplifier'
  m.setvolume(50) # set volume
  vol = m.getvolume() # get volume float value```
4. Need to figure out a user interaction so the alarm can be turned off (after it has gone off) but remain on for the next day.

## Needed packages: ##
1. Sox: apt-get install sox
2. Mpg123: apt-get install mpg123
3. Alsaaudio: apt-get install python-alsaaudio

Material Design Alarm Design: http://tutorialzine.com/2015/04/material-design-stopwatch-alarm-and-timer/

Github token: 9046ff1e95dbfa91346d67b4b2f9dc9bbbffd581
Gist ID: 9d81a5614c32af52bba68fa1ea8c258a
