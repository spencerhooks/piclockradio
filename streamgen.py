#!/usr/bin/python
"""
A simple module for playback of mp3 streams and generation of synthetic signals. It's a wrapper around
the Sound Exchange (SoX) and mpg123 libraries to provide python playback.

Use the generate method for synthetic signals. Allows input parameters of:
  - Duration of playback in seconds (0=infinite; default=0)
  - Signal type (sine, square, triangle, sawtooth, trapezium, exp, [white]noise, tpdfnoise, pinknoise,
    brownnoise, pluck; default=brownnoise)
  - Gain (specified relative to 0dBFS, so should be a negative number; default=0dBFS)
  - Fadetime (same time used for fadein and fadeout; default=0)

 Many other parameters can be used with SoX, but are not implemented.

 Use the play method for mp3 stream playback. Allows input parameters of:
  - Duration of playback in seconds (0=infinite; default=0)
  - Source of stream (currently only supports kqed; default=0)

This module Requires that SoX and mpg123 are installed. Please see http://sox.sourceforge.net for more
info on SoX. Please see http://www.mpg123.org for more info on mpg123.

Notes:
  - Is there a way to change duration with the play method so that it is duration of audio not duration of the thread?

"""

from subprocess import Popen
from threading import Thread
import os, time, logging, sys



logging.basicConfig(stream=sys.stderr, level=logging.INFO)



class Player(object):

    def generate(self, duration=0, tone='brownnoise', gain=0, fadetime=0):
        """
        Method to generate synthetic signal using SoX.
        """
        if logging.getLogger().getEffectiveLevel() != 10:
            self.t = Thread(target = self._send_command, kwargs={'duration': duration, 'tone': tone, 'gain': gain, 'fadetime': fadetime})
            self.t.start()
        logging.debug("Generating sound " + tone + " for a duration of " + str(duration))

    def play(self, duration=0, source='kqed'):
        """
        Method to play mp3 stream using mpg123 library. It takes a few seconds to connect and start playback,
        so the duration value should be padded if you want that to be the duration of audio heard.
        Unfortunately, duration in this case is the duration that the player thread will remain open, not
        the duration of audio.
        """
        if logging.getLogger().getEffectiveLevel() != 10:
            self.t = Thread(target = self._send_command, kwargs={'duration': duration, 'tone': source,})
            self.t.start()
        logging.debug("Playing source " + source + " for a duration of " + str(duration))

    def stop(self):
        """
        Method to stop playback. This is only needed when duration is not given or is set to 0 (infinite).
        """
        if logging.getLogger().getEffectiveLevel() != 10:
            try:
                self._player.terminate()
            except AttributeError as e:  # Make things a bit more user friendly and allow a stop command even if not playing
                if str(e) == "'Player' object has no attribute '_player'":
                    return
                else:
                    raise AttributeError(str(e))  # Only catch the known error and raise any others to pass them through
        logging.debug("Stopping Playback")

    def is_playing(self):
        """
        Method to check status of player. Returns status of thread to indicate activity.
        """
        if logging.getLogger().getEffectiveLevel() != 10:
            try:
                return self.t.is_alive()
            except AttributeError as e:  # Make things a bit more user friendly and return False even if playback never started
                if str(e) == "'Player' object has no attribute 't'":
                    return False
                else:
                    raise AttributeError(str(e))  # Only catch the known error and raise any others to pass them through
        logging.debug("Returning Value True")
        return True

    def _send_command(self, duration=0, tone='brownnoise', gain=0, fadetime=0):
        """
        Private method used to send command to SoX or mpg123.
        """
        if tone == 'kqed':  # If tone is kqed then we use mpg123 to play the kqed live stream.
            self._player = Popen(['mpg123', '-q', '-@', 'http://streams.kqed.org/kqedradio.m3u'])
            if duration != 0:  # duration is handled manually in this case.
                time.sleep(duration)
                self.stop()
        else:
            is_null = False if duration == 0 else True  # Make sure the fade stop position is null when duration is 0
            self._player = Popen(['play', '-q', '-n', 'synth', str(duration), tone, 'gain', str(gain), 'fade', 'q', str(fadetime)] + ['0']*is_null)
