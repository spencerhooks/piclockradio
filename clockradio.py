#!/usr/bin/python2

from flask import Flask, render_template
from threading import Thread, Timer
from phue import Bridge
import json, time, datetime, logging, logging.handlers
import alsaaudio, streamgen

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# create a file handler
handler = logging.handlers.RotatingFileHandler('clockradio.log', maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

noiseplayer = streamgen.Player()
alarmplayer = streamgen.Player()
mixer = alsaaudio.Mixer(device='pulse') # should be control='PCM' for a pi headphone output

app = Flask(__name__)

# Hue bridge
b = Bridge('192.168.1.217')

# Constants for sunrise/sleep light
TRANSITION_TIME = 4*60 # 4 minutes
DELAY_TIME = 30*60 # 30 minutes
FADE_OFF_TIME = 600 # 10 minutes

# Define the color transitions for sunrise. Each variable runs for a duration defined by TRANSITION_TIME.
color_list = [{'on':True, 'bri':0, 'hue':0}] # red
color_list.append({'transitiontime':TRANSITION_TIME*10, 'on':True, 'bri':15, 'hue':2000}) # lighter red
color_list.append({'transitiontime':TRANSITION_TIME*10, 'on':True, 'bri':25, 'hue':5000}) # red orange
color_list.append({'transitiontime':TRANSITION_TIME*10, 'on':True, 'bri':50, 'hue':9977}) # orange
color_list.append({'transitiontime':TRANSITION_TIME*10, 'on':True, 'bri':100, 'hue':9980}) # orange yellow
color_list.append({'transitiontime':TRANSITION_TIME*10, 'on':True, 'bri':150, 'hue':13390}) # yellow
color_list.append({'transitiontime':TRANSITION_TIME*10, 'on':True, 'bri':200, 'hue':15191}) # yellow white
color_list.append({'transitiontime':TRANSITION_TIME*10, 'on':True, 'bri':255, 'hue':38000}) # white

# Counter used for recursive sunrise loop
sunrise_counter = 0

# Open the json file used for data storage, read the last state
with open('clock_data_file.json', 'r') as f:
    try:
        clock_data = json.load(f)
        logger.info("Successful opened json data file loaded into dictionary.")
    # if the file is empty the ValueError will be thrown
    except ValueError:
        clock_data = {}
        logger.info("Couldn't open json data file, creating new empty dictionary.")

####  Flask routes

# Primary clock page
@app.route('/')
def clock():
    logger.info("Responding to request for clock.html.")
    return render_template('clock.html')

# Settings page
@app.route('/settings/')
def settings():
    logger.info("Responding to request for settings.html.")
    return render_template('settings.html')

# General purpose route to capture the simple commands
@app.route('/<cmd>')
def command(cmd='NONE'):
    logger.info("Received command: %s", cmd)

    if cmd == 'generate_noise':
        if clock_data['generating_noise'] == False:
            noiseplayer.generate(gain=-10)
            clock_data['generating_noise'] = True
            logger.info("Noise button pressed. Generating brownian noise at a gain of -10dBFS.")
        elif clock_data['generating_noise'] == True:
            noiseplayer.stop()
            clock_data['generating_noise'] = False
            logger.info("Noise button pressed. Stopping brownian noise generation.")

    # Update the dictionary for snooze
    if cmd == 'snooze':
        snooze_thread = Thread(target=snooze)
        snooze_thread.daemon = True
        snooze_thread.start()
        logger.info("Snooze trigger; Starting snooze thread.")

    # Update the dictionary for mute
    if cmd == 'mute':
        if clock_data['mute'] == True:
            mixer.setvolume(int(clock_data['volume']))
            clock_data['mute'] = False
            logger.info("Mute button pressed. Muting volume and disabling volume slider.")
        else:
            mixer.setvolume(0)
            clock_data['mute'] = True
            logger.info("Mute button pressed. Unmuting volume and enabling volume slider.")

    # Write the dictionary out to file and return the dictionary to the client
    write_file()
    logger.info("Finished handling general purpose button captures; writing file and returning json to client.")
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Alarm state
@app.route('/alarm_on_off/<state>')
def alarm_state_change(state):
    clock_data['alarm_on_off'] = str2bool(state)
    logger.info("Received alarm on/off state: %s; Setting dictionary and writing to file.", state)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Sleep light on/off
@app.route('/sleep_light_on_off/<state>')
def sleep_light_state_change(state):
    logger.info("Sleep light switch flipped.")
    clock_data['sleep_light_on_off'] = str2bool(state)
    if clock_data['sleep_light_on_off'] == True:
        b.set_light(3, {'on':True, 'bri':200, 'hue':15191})
        sleep_light_thread = Timer(FADE_OFF_TIME*2, fade_off_light)
        sleep_light_thread.start()
        logger.info("Received sleep light on/off state: %s; Starting sleep light thread to turn on light for %s minutes before fading off", state, FADE_OFF_TIME*3/60)
    elif clock_data['sleep_light_on_off'] == False:
        try:
            sleep_light_thread.cancel()
        except UnboundLocalError as e:
            if str(e) == "local variable 'sleep_light_thread' referenced before assignment":
                pass
            else:
                raise UnboundLocalError(str(e))  # Only catch the known error and raise any others to pass them through
        logger.info("Received sleep light on/off state: %s; Cancelling sleep light thread and turning off light.", state)
        turn_off_light()
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Update time for clock face
@app.route('/get_time/')
def get_time():
    full_time = (datetime.datetime.now().strftime('%H:%M'))
    if not clock_data['indicate_snooze']: clock_data['time'] = full_time # Pause clock refesh to indicate snooze
    if full_time == clock_data['alarm_reset_time'] and datetime.datetime.now().strftime('%w') in ('1', '2', '3', '4', '5'): # Turn on alarm automatically on weekdays
        clock_data['alarm_on_off'] = True
        logger.info("Turning the alarm on automatically.")
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Set the volume according to the slider input
@app.route('/change_volume/<volume_target>')
def volume(volume_target):
    mixer.setvolume(int(volume_target))
    logger.info("Volume slider was moved. Setting volume to: %s.", volume_target)
    clock_data['volume'] = str(mixer.getvolume()[0])
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Alarm time setting
@app.route('/alarm_time_set/<time>')
def alarm_time(time):
    clock_data['alarm_time'] = time
    logger.info("Alarm time input received. Setting alarm to: %s.", time)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Alarm duration setting
@app.route('/alarm_duration_set/<time>')
def alarm_duration(time):
    clock_data['alarm_duration'] = time
    logger.info("Alarm duration input received. Setting alarm duration to: %s.", time)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Alarm rest time setting
@app.route('/alarm_reset_time_set/<time>')
def alarm_reset_time(time):
    clock_data['alarm_reset_time'] = time
    logger.info("Alarm reset time input received. Setting alarm rest time to: %s.", time)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Auto alarm reset switch
@app.route('/alarm_auto_set/<state>')
def alarm_auto(state):
    clock_data['alarm_auto_reset'] = str2bool(state)
    logger.info("Alarm auto set switch flipped. Setting alarm auto set state to: %s.", state)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Sleep time setting
@app.route('/sleep_time_set/<time>')
def sleep_time(time):
    clock_data['sleep_light_duration'] = time
    logger.info("Sleep light duration input received. Setting sleep light duration to: %s.", time)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Snooze duration setting
@app.route('/snooze_duration_set/<time>')
def snooze_duration(time):
    clock_data['snooze_duration'] = time
    logger.info("Snooze duration input received. Setting snooze duration to: %s.", time)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Coffee pot setting
@app.route('/coffee_pot_set/<state>')
def coffee_pot(state):
    clock_data['coffee_pot'] = str2bool(state)
    logger.info("Coffee pot switch flipped. Setting coffee pot to: %s.", state)
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))

# Sunrise setting
@app.route('/sunrise_set/<state>')
def sunrise(state):
    clock_data['sunrise'] = str2bool(state)
    logger.info("Sunrise light switch flipped. Setting sunrise light to: %s.", state)
    if clock_data['sunrise'] == False:
        turn_off_light()
        logger.info("Sunrise light was switched off, turning off light and cancelling any timed threads.")
        try:
            sunrise_thread.cancel()
        except NameError as e:
            if str(e) == "global name 'sunrise_thread' is not defined":
                pass
            else:
                raise NameError(str(e))  # Only catch the known error and raise any others to pass them through
    write_file()
    logger.debug("Returning file: %s", json.dumps(clock_data))
    return (json.dumps(clock_data))


#### Non route functions

# Sound the alarm
def alarm_loop():
    while True:
        mytime = clock_data['alarm_time']
        if clock_data['snoozing'] == True: mytime = clock_data['snooze_time']
        if clock_data['time'] == mytime and clock_data['alarm_on_off'] == True and clock_data['alarm_sounding'] == False:
            logger.info("Sound the alarm for " + clock_data['alarm_duration'] + " minutes!!")
            alarmplayer.play(duration=(int(clock_data['alarm_duration'])*60))
            clock_data['alarm_sounding'] = True
        elif clock_data['alarm_sounding'] == True:
            if alarmplayer.is_playing() == False:
                clock_data['alarm_sounding'] = False
                clock_data['snoozing'] == False
                logger.info("Alarm stopped automatically after %s minute duration.", clock_data['alarm_duration'])
            elif clock_data['alarm_on_off'] == False:
                alarmplayer.stop()
                clock_data['alarm_sounding'] = False
                clock_data['snoozing'] == False
                logger.info("Alarm stopped because it was switched off by the user.")
        if clock_data['alarm_on_off'] == False:
            clock_data['snoozing'] = False
        time.sleep(.5)

# Spawn thread for alarm
alarm_thread = Thread(target=alarm_loop)
alarm_thread.daemon = True
alarm_thread.start()

# Turn off light
def turn_off_light():
    while b.get_light(3, 'on'):
        logger.info("Turning off the light.")
        b.set_light(3, 'on', False)

def fade_off_light():
    logger.info("Fading off the light for %s minutes.", FADE_OFF_TIME/60)
    b.set_light(3, {'transitiontime':FADE_OFF_TIME*10, 'bri':0})
    time.sleep(FADE_OFF_TIME)
    turn_off_light()
    clock_data['sleep_light_on_off'] = False
    write_file()

# Recursive function to run the sunrise light by using the color_list elements
def make_sunrise():
    global sunrise_counter

    if sunrise_counter <= len(color_list)-1:
        b.set_light(3, (color_list[sunrise_counter]))
        global sunrise_thread
        sunrise_thread = Timer(TRANSITION_TIME, make_sunrise)
        sunrise_thread.start()
    elif sunrise_counter == len(color_list):
        logger.info("Turning off light in %s minutes.", DELAY_TIME/60)
        sunrise_thread = Timer(DELAY_TIME, turn_off_light)
        sunrise_thread.start()

    sunrise_counter += 1

# Make the sunrise
def sunrise_loop():
    while True:
        if(datetime.datetime.now() + datetime.timedelta(minutes=32)).strftime('%H:%M') == clock_data['alarm_time']:

            logger.info("Making the sunrise.")
            global sunrise_counter
            sunrise_counter = 0
            # Spawn the first sunrise thread
            sunrise_thread = Thread(target = make_sunrise)
            sunrise_thread.start()

        time.sleep(60)

# Spawn the sunrise thread
sunrise_loop_thread = Thread(target=sunrise_loop)
sunrise_loop_thread.daemon = True
sunrise_loop_thread.start()

# Snooze the alarm
def snooze():
    if clock_data['alarm_sounding'] == False or clock_data['alarm_on_off'] == False:
        logger.info("Snooze button was pressed, but alarm is off. Nothing to do.")
        return ('', 204)
    elif clock_data['alarm_sounding'] == True:
        logger.info("Snooze button was pressed and alarm is on, time to execute snooze.")

        # Stop playback of KQED
        logger.info("Stopping playback of the alarm (KQED stream)")
        alarmplayer.stop()
        clock_data['alarm_sounding'] = False
        clock_data['snoozing'] = True

        # Pause the clock and indicate a snooze to the client
        logger.info("Pausing the clock updates and indicating a snooze to the user.")
        clock_data['indicate_snooze'] = True

        # Get the time in 10 min to set snooze_time
        clock_data['snooze_time'] = (datetime.datetime.now() + datetime.timedelta(minutes=int(clock_data['snooze_duration']))).strftime('%H:%M')

        # Display a snooze indicator on the clockface
        clock_data['time'] = "snooze"
        time.sleep(2)
        clock_data['time'] = clock_data['snooze_duration'] + " min"
        time.sleep(2)

        # Resume clock function, tell the client to stop indicating snooze, and write the file
        logger.info("Snooze indicated, resuming the normal clock function")
        clock_data['indicate_snooze'] = False
        write_file()

# Write the data to file
def write_file():
    logger.debug("Writing data to clock_data_file.json. Here's the data: ", json.dumps(clock_data))
    with open('clock_data_file.json', 'w') as f:
        json.dump(clock_data, f, indent=4, sort_keys=True)

# Convert string to boolean
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cache.init_app(app)
