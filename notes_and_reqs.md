# Notes and Requirements #

## Known Issues/To Do List ##
1. The volume slider has a bug where holding and dragging (but not letting go) causes a visual problem because the slider position is updated by javascript from the previous position in json file.
  1. Volume not working in chrome on Ubuntu for some reason (works in Firefox on Ubuntu)
2. If you turn off alarm within one minute and immediately turn it back on the alarm sounds because it's still the right time
3. Text inputs on settings page send entry even though it doesn't match the regex pattern. Need to stop that from going into the file/dict
4. Finish adding logging messages

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
pygame.mixer.music.load("brownnoise2.mp3")
pygame.mixer.music.play(-1)
```
2. Better still, use sox to generate brown noise (no looping)
  1. See script
  2. There's a python wrapper, but it doesn't add much in this case and is blocking when it calls the sox player
3. Setting volume:
```python
import alsaaudio
m = alsaaudio.Mixer()   # defined alsaaudio.Mixer to change volume. Default device is Mixer. Chip needs to use 'Power Amplifier'
m.setvolume(50) # set volume
vol = m.getvolume() # get volume float value
```
4. Need to figure out a user interaction so the alarm can be turned off (after it has gone off) but remain on for the next day.
5. regex for time ```pattern="^([0[0-9]|1[0-2]):[0-5][0-9][ap][m]$"```
6. regex for number 1-60 ```pattern="^([1-9]|[0-5][0-9]|60)$"```
7. check the host OS, name, cpu, etc using ```os.uname()```
    1. get cpu with ```os.uname()[4]```
    2. match arm* with ```os.uname()[4].startswith('arm')```

## Needed packages: ##
1. Sox: apt-get install sox
2. Mpg123: apt-get install mpg123
3. Alsaaudio: apt-get install python-alsaaudio

Material Design Alarm Design: http://tutorialzine.com/2015/04/material-design-stopwatch-alarm-and-timer/
