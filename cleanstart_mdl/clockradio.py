#!/usr/bin/python

from flask import Flask, render_template
from datetime import datetime
import json
# import alsaaudio, streamgen
#
# player = streamgen.Player()
# mixer = alsaaudio.Mixer()

app = Flask(__name__)

clock_data = {}

@app.route('/')
def clock():
    return render_template('clock.html')

@app.route('/<cmd>')
def command(cmd='NONE'):
    if cmd == "play_pause":
        # if player.is_playing() == False:
        #     player.generate()
        #     print("play noise generator")
        # else:
        #     player.stop()
        #     print("stop making noise")
        print("play or pause")
    if cmd == "snooze":
        print("snooze")
    if cmd == "mute":
        print("mute")
    return ('', 204)

@app.route('/alarm_on_off/<state>')
def alarm_state_change(state):
    if state == 'true':
        print("change alarm state to " + state)
    return ('', 204)

@app.route('/get_time/')
def get_time():
    global clock_data
    t = datetime.now().strftime('%I:%M')
    p = datetime.now().strftime('%p')
    f = t + p.lower()
    clock_data['time'] = f
    return (json.dumps(clock_data))

@app.route('/sleep_light_on_off/<state>')
def sleep_light_state_change(state):
    if state == 'true':
        print("change sleep light state to " + state)
    return ('', 204)

@app.route('/change_volume/<volume_target>')
def volume(volume_target):
    # mixer.setvolume(volume_target)
    print("volume target: " + volume_target)
    # return int(mixer.getvolume())
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cache.init_app(app)
