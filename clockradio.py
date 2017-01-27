#!/usr/bin/python2

from flask import Flask, render_template
from threading import Thread
from phue import Bridge
import json, time, datetime
import alsaaudio, streamgen

noiseplayer = streamgen.Player()
alarmplayer = streamgen.Player()
mixer = alsaaudio.Mixer(device='pulse')

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

@app.route('/settings/')
def settings():
    return render_template('settings.html')

# General purpose route to capture the simple commands
@app.route('/<cmd>')
def command(cmd='NONE'):
    if cmd == 'generate_noise':
        if clock_data['generating_noise'] == False:
            noiseplayer.generate(gain=-10)
            clock_data['generating_noise'] = True
        elif clock_data['generating_noise'] == True:
            noiseplayer.stop()
            clock_data['generating_noise'] = False

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

# Alarm state
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
    full_time = (datetime.datetime.now().strftime('%H:%M'))
    if not clock_data['indicate_snooze']: clock_data['time'] = full_time # Pause clock refesh to indicate snooze
    if full_time == clock_data['alarm_reset_time'] and datetime.datetime.now().strftime('%w') in ('1', '2', '3', '4', '5'): # Turn on alarm automatically on weekdays
        clock_data['alarm_on_off'] = True
    return (json.dumps(clock_data))

# Set the volume according to the slider input
@app.route('/change_volume/<volume_target>')
def volume(volume_target):
    mixer.setvolume(int(volume_target))
    clock_data['volume'] = str(mixer.getvolume()[0])
    print("volume target: " + str(mixer.getvolume()[0]))
    write_file()
    return (json.dumps(clock_data))  # There's a bug when dragging the slider, need to fix this.

# Alarm time setting
@app.route('/alarm_time_set/<time>')
def alarm_time(time):
    clock_data['alarm_time'] = time
    write_file()
    return (json.dumps(clock_data))

# Alarm duration setting
@app.route('/alarm_duration_set/<time>')
def alarm_duration(time):
    clock_data['alarm_duration'] = time
    write_file()
    return (json.dumps(clock_data))

# Alarm rest time setting
@app.route('/alarm_reset_time_set/<time>')
def alarm_reset_time(time):
    clock_data['alarm_reset_time'] = time
    write_file()
    return (json.dumps(clock_data))

# Auto alarm reset switch
@app.route('/alarm_auto_set/<state>')
def alarm_auto(state):
    clock_data['alarm_auto_reset'] = str2bool(state)
    write_file()
    return (json.dumps(clock_data))

# Sleep time setting
@app.route('/sleep_time_set/<time>')
def sleep_time(time):
    clock_data['sleep_light_duration'] = time
    write_file()
    return (json.dumps(clock_data))

# Snooze duration setting
@app.route('/snooze_duration_set/<time>')
def snooze_duration(time):
    clock_data['snooze_duration'] = time
    write_file()
    return (json.dumps(clock_data))

# Coffee pot setting
@app.route('/coffee_pot_set/<state>')
def coffee_pot(state):
    clock_data['coffee_pot'] = str2bool(state)
    write_file()
    return (json.dumps(clock_data))

# Sunrise setting
@app.route('/sunrise_set/<state>')
def sunrise(state):
    clock_data['sunrise'] = str2bool(state)
    write_file()
    return (json.dumps(clock_data))

# Sound the alarm
def run_alarm():
    while True:
        mytime = clock_data['alarm_time']
        if clock_data['snoozing'] == True: mytime = clock_data['snooze_time']
        if clock_data['time'] == mytime and clock_data['alarm_on_off'] == True and clock_data['alarm_sounding'] == False:
            print("Sound the alarm for " + clock_data['alarm_duration'] + " minutes!!")
            alarmplayer.play(duration=(int(clock_data['alarm_duration'])*60))
            clock_data['alarm_sounding'] = True
        elif clock_data['alarm_sounding'] == True:
            if alarmplayer.is_playing() == False:
                clock_data['alarm_sounding'] = False
                clock_data['snoozing'] == False
                print("stopped automatically after duration")
            elif clock_data['alarm_on_off'] == False:
                alarmplayer.stop()
                clock_data['alarm_sounding'] = False
                clock_data['snoozing'] == False
                print("stopped because of switch")
        if clock_data['alarm_on_off'] == False:
            clock_data['snoozing'] = False
        time.sleep(.5)
            # Play KQED for 15 minutes with fade in/out

# Spawn thread for alarm
alarm_thread = Thread(target=run_alarm)
alarm_thread.daemon = True
alarm_thread.start()

# Make the sunrise
def run_sunrise():
    TRANSITION_TIME = 4*60 # 4 minutes in seconds
    DELAY_TIME = 30 # 30 minutes

    # Change to your IP address
    b = Bridge('192.168.1.217')

    # Define the color transitions. Each variable runs for a duration defined by TRANSITION_TIME.
    color_list = [{'on' : True, 'bri' : 0, 'hue' : 0}] # red
    color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 15, 'hue' : 2000}) # lighter red
    color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 25, 'hue' : 5000}) # red orange
    color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 50, 'hue' : 9977}) # orange
    color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 100, 'hue' : 9980}) # orange yellow
    color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 150, 'hue' : 13390}) # yellow
    color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 200, 'hue' : 15191}) # yellow white
    color_list.append({'transitiontime' : TRANSITION_TIME*10, 'on' : True, 'bri' : 255, 'hue' : 20000}) # white

    while True:
        if(datetime.datetime.now() + datetime.timedelta(minutes=-32)).strftime('%H:%M') == clock_data['alarm_time']:
            for element in color_list:
                b.set_light(3, element)
                time.sleep(TRANSITION_TIME)

            time.sleep(DELAY_TIME)
            b.set_light(3,'on', False)
        time.sleep(30)

# Spawn the sunrise thread
sunrise_thread = Thread(target=run_sunrise)
sunrise_thread.daemon = True
sunrise_thread.start()

# Snooze the alarm
def snooze():
    if clock_data['alarm_sounding'] == False or clock_data['alarm_on_off'] == False: return ('', 204)
    elif clock_data['alarm_sounding'] == True:

        # Stop playback of KQED
        alarmplayer.stop()
        clock_data['alarm_sounding'] = False
        clock_data['snoozing'] = True

        # Pause the clock and indicate a snooze to the client
        clock_data['indicate_snooze'] = True

        # Get the time in 10 min to set snooze_time
        print (datetime.datetime.now() + datetime.timedelta(minutes=int(clock_data['snooze_duration']))).strftime('%H:%M')
        clock_data['snooze_time'] = (datetime.datetime.now() + datetime.timedelta(minutes=int(clock_data['snooze_duration']))).strftime('%H:%M')

        # Display a snooze indicator on the clockface
        clock_data['time'] = "snooze"
        time.sleep(2)
        clock_data['time'] = clock_data['snooze_duration'] + " min"
        time.sleep(2)

        # Resume clock function, tell the client to stop indicating snooze, and write the file
        clock_data['indicate_snooze'] = False
        write_file()
    print("snoozing")
    # When snooze is trigger the alarm should be turned off and snoozed for the duration in settings

# Write the data to file
def write_file():
    with open('clock_data_file.json', 'w') as f:
        json.dump(clock_data, f, indent=4, sort_keys=True)

# Convert string to boolean
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cache.init_app(app)
