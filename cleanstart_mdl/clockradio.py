#!/usr/bin/python

from flask import Flask, render_template
# from streamgen import Player
#
# p = Player()

app = Flask(__name__)

@app.route('/')
def clock():
    return render_template('clock.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cache.init_app(app)
