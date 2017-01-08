#!/usr/bin/python

from flask import Flask, render_template
# import alsaaudio, streamgen
#
# player = streamgen.Player()
# mixer = alsaaudio.Mixer()

app = Flask(__name__)

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
    return 'True'

@app.route('/alarm_on_off/<state>')
def alarm_state_change(state):
    if state == 'true':
        print("change alarm state to " + state)
    return 'True'

@app.route('/change_volume/<volume_target>')
def volume(volume_target):
    # mixer.setvolume(volume_target)
    print(volume_target)
    # return int(mixer.getvolume())
    return 'True'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cache.init_app(app)
