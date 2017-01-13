#!/usr/bin/python

from flask import Flask, render_template
from datetime import datetime
import json
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
        if clock_data['snooze'] == True: clock_data['snooze'] = False
        else: clock_data['snooze'] = True
        print("snoozing: " + str(clock_data['snooze']))  # Maybe change clock face background color to indicate snooze?

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
    global clock_data
    hour_minute = datetime.now().strftime('%I:%M')
    am_pm = datetime.now().strftime('%p')
    full_time = hour_minute + am_pm.lower()
    clock_data['time'] = full_time
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
