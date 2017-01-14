#!/usr/bin/python

from flask import Flask, render_template
from threading import Thread
import json, time, datetime
# import alsaaudio, streamgen
#
# player = streamgen.Player()
# mixer = alsaaudio.Mixer()

app = Flask(__name__)

# Open the json file used for data storage, read the last state
with open('clock_data_file.json', 'r') as f:
    try:
        clock_data = json.load(f)
    # if the file is empty the ValueError will be thrown
    except ValueError:
        clock_data = {}

@app.route('/')
def clock():
    return render_template('clock.html')

# General purpose route to capture the simple commands
@app.route('/<cmd>')
def command(cmd='NONE'):
    # Return null so that we don't update the file unnecessarily
    if cmd == 'favicon.ico':
        return('', 204)

    # Update the dictionary to generate noise
    if cmd == 'generate_noise':
        # if player.is_playing() == False:
        #     player.generate()
        #     print("play noise generator")
        # else:
        #     player.stop()
        #     print("stop making noise")
        if clock_data['generating_noise'] == True: clock_data['generating_noise'] = False
        else: clock_data['generating_noise'] = True
        print("generating noise: " + str(clock_data['generating_noise']))

    # Update the dictionary for snooze
    if cmd == 'snooze':
        snooze_thread = Thread(target=snooze)
        snooze_thread.daemon = True
        snooze_thread.start()

    # Update the dictionary for mute
    if cmd == 'mute':
        if clock_data['mute'] == True:
            clock_data['mute'] = False
        else: clock_data['mute'] = True

    # Write the dictionary out to file and return the dictionary to the client
    write_file()
    return (json.dumps(clock_data))

# Alarm state (needs updating)
@app.route('/alarm_on_off/<state>')
def alarm_state_change(state):
    clock_data['alarm_on_off'] = str2bool(state)
    write_file()
    return (json.dumps(clock_data))

# Sleep light on/off
@app.route('/sleep_light_on_off/<state>')
def sleep_light_state_change(state):
    clock_data['sleep_light_on_off'] = str2bool(state)
    write_file()
    return (json.dumps(clock_data))

# Update time for clock face
@app.route('/get_time/')
def get_time():
    hour_minute = (datetime.datetime.now().strftime('%I:%M')).lstrip("0")
    am_pm = datetime.datetime.now().strftime('%p')
    full_time = hour_minute + am_pm.lower()
    if not clock_data['pause_clock']: clock_data['time'] = full_time
    return (json.dumps(clock_data))

# Set the volume according to the slider input
@app.route('/change_volume/<volume_target>')
def volume(volume_target):
    # mixer.setvolume(volume_target)
    clock_data['volume'] = volume_target
    print("volume target: " + volume_target)
    # return int(mixer.getvolume())
    write_file()
    return (json.dumps(clock_data))  # There's a bug when dragging the slider, need to fix this.

# Sound the alarm
def run_alarm():
    while True:
        if clock_data['time'] == clock_data['alarm_time'] and clock_data['alarm_on_off'] == True:
            clock_data['alarm_sounding'] = True
            print("sound the alarm for 15 minutes!!")
        time.sleep(.5)
            # Need to change alarm_sounding to False
            # Play KQED for 15 minutes with fade in/out; use global variable so other functions can stop playback

# Snooze the alarm
def snooze():
    if clock_data['alarm_sounding'] == False: return ('', 204)
    elif clock_data['alarm_sounding'] == True:
        clock_data['pause_clock'] = True

        # Get the time in 10 min to snooze the alarm time out by 10 min
        new_hour_minute = ((datetime.datetime.now() + datetime.timedelta(minutes = 10)).strftime('%I:%M')).lstrip("0")
        new_am_pm = datetime.datetime.now().strftime('%p')
        new_alarm_time = new_hour_minute + new_am_pm.lower()
        print new_alarm_time
        clock_data['alarm_time'] = new_alarm_time

        clock_data['time'] = "SNOOZE"
        time.sleep(3)
        clock_data['time'] = "10 min"
        time.sleep(3)
        clock_data['pause_clock'] = False
        write_file()
    print("snoozing")  # Maybe change clock face background color to indicate snooze?
    # When snooze is trigger the alarm should be turned off and reset for 10min in the future. Need to figure out interaction model here

# Spawn thread for alarm
alarm_thread = Thread(target=run_alarm)
alarm_thread.daemon = True
alarm_thread.start()

# Write the data to file
def write_file():
    with open('clock_data_file.json', 'w') as f:
        json.dump(clock_data, f)

# Convert string to boolean
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cache.init_app(app)
