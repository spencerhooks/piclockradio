#!/usr/bin/python

from flask import Flask, render_template
from streamgen import Player

p = Player()

app = Flask(__name__)

@app.route('/')
def clock():
    return render_template('clock.html', play_state='Play')

@app.route('/settings/')
def settings():
    return render_template('settings.html', button_state='Press Me')

@app.route('/play_sound/<ps>')
def play_sound(ps):
    if ps == 'Play':
        p.play()
        ps = 'Stop'
    elif ps == 'Stop':
        p.stop()
        ps = 'Play'
    return render_template('clock.html', play_state=ps)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cache.init_app(app)
