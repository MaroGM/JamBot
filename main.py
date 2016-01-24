#!/usr/bin/env python

"""
JamBot

Robot controlled via Twitch chat and showing Twitter hashtag usage.
Made for the Malta Global Game Jam 2016.

"""

# from ConfigParser import ConfigParser
# import tornado.ioloop
# import tornado.web
# import os.path
# from InputManager import *
# from TwitterLoop import *

import os
import sys
import time
import datetime
import json
import threading

from ConfigParser import ConfigParser
from twython import TwythonStreamer

import tornado.ioloop
import tornado.web

from TwitchParse import TwitchParse
from InputManager import *

# Change syspath to local folder
os.chdir(os.path.dirname(sys.argv[0]))

# Read config from settings file
config = ConfigParser()
config.read("settings.txt")

# Read Twitter Settings
TERMS = config.get('Twitter Settings', 'TERMS')
APP_KEY = config.get('Twitter Settings', 'APP_KEY')
APP_SECRET = config.get('Twitter Settings', 'APP_SECRET')
OAUTH_TOKEN = config.get('Twitter Settings', 'OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = config.get('Twitter Settings', 'OAUTH_TOKEN_SECRET')

# Read Twitch Settings
HOST = config.get('Twitch Settings', 'HOST')
PORT = config.get('Twitch Settings', 'PORT')
AUTH = config.get('Twitch Settings', 'AUTH')
USER = config.get('Twitch Settings', 'USER')
CHAN = config.get('Twitch Settings', 'CHAN')

# Tornado Server Settings
TORNADO_PORT = 8080

RPI_LIGHT = False
RPI_HPOS = 50
RPI_VPOS = 50
RPI_SPEED = 100

H_INCR = 10
V_INCR = 10

DEBUG = True

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def debugLog(output, context='MISC'):
    if DEBUG is True:
        timestamp = "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "]"
        print(timestamp + "[" + context.upper() + "] " + output)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class RaspiHandler(tornado.web.RequestHandler):
    def get(self):
        result = {'light': RPI_LIGHT,
                    'h_pos': RPI_HPOS,
                    'v_pos': RPI_VPOS,
                    'speed': RPI_SPEED
                    }
        kk = tornado.escape.json_encode(result)
        self.write(kk)
        debugLog("JSON data has been picked up", "RASPI")

class AdminPanelHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Percent towards democracy: " + str(InputManager.get_social_anarchy_percentage()) + "<br>")
        self.write("All buffered input: " + str(InputManager.buffered_input) + "<br>")

class InputHandler(tornado.web.RequestHandler):
    def post(self):
        input_str = self.get_argument('input', '')
        userid = self.get_argument('userid', '')
        self.write("Got input of " + input_str + " from user " + userid)
        InputManager.add_input(input_str)



# Setup callbacks from Twython Streamer
class TwitterStream(TwythonStreamer):
    def on_success(self, data):
        global RPI_LIGHT

        if 'text' in data:
            # print data['text'].encode('utf-8')
            RPI_LIGHT = True
            time.sleep(2)
            RPI_LIGHT = False
            time.sleep(1)


def serverThread():
    application = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/raspi_pickup", RaspiHandler),
            (r"/input", InputHandler),
            (r"/admin_panel", AdminPanelHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static")
        )

    application.listen(TORNADO_PORT)
    main_loop = tornado.ioloop.IOLoop.instance()
    inputmanager_update = tornado.ioloop.PeriodicCallback(InputManager.update, 10)
    inputmanager_update.start()

    vote_update = tornado.ioloop.PeriodicCallback(submitVotes, 10000)
    vote_update.start()

    main_loop.start()

t_server = threading.Thread(name='server-thread', target=serverThread)


def twitterThread():
    """ Starts the Twitter stream (blocking function!) """
    debugLog("Twitter Stream Started", "THREAD")
    twitterstream = TwitterStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitterstream.statuses.filter(track=TERMS)

t_twitter_daemon = threading.Thread(name='twitter-daemon', target=twitterThread)
t_twitter_daemon.setDaemon(True)


def twitchThread():
    """ Starts Twitch parsing (blocking function!) """

    global twitchstream

    debugLog("Twitch Parsing Started", "THREAD")
    twitchstream = TwitchParse(HOST, PORT, AUTH, USER, CHAN)
    twitchstream.start()

t_twitch_daemon = threading.Thread(name='twitch-daemon', target=twitchThread)
t_twitch_daemon.setDaemon(True)


def submitVotes():
    """ Send instructions to Raspi """
    global RPI_HPOS
    global RPI_VPOS

    outcome = twitchstream.getVotes()

    new_H = RPI_HPOS
    new_V = RPI_VPOS

    if outcome is 'center':
        new_H = 50
        new_V = 50 
    elif outcome is 'right':
        RPI_HPOS += H_INCR
    elif outcome is 'left':
        RPI_HPOS -= H_INCR
    elif outcome is 'up':
        RPI_VPOS += V_INCR
    elif outcome is 'down':
        RPI_VPOS -= V_INCR

    new_H = clamp(new_H, 0, 100)
    new_V = clamp(new_V, 0, 100)

    RPI_HPOS = new_H
    RPI_VPOS = new_V


if __name__ == "__main__":
    try:
        t_twitch_daemon.start()
        t_twitter_daemon.start()
        t_server.start()
        
    except (KeyboardInterrupt, SystemExit):
        t_server.stop()
        tornado.ioloop.IOLoop.instance().stop()
        debugLog("Bye bye", "EXIT")

