# Launch.py
# Copyright (C) 2014 : Alex Edwards
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#

import ConfigParser
import os
import sys
import string
import time
import socket
from threading import Thread
# import win32com.client, win32api, win32con

settings = []
commands = []
readbuffer = ""
# GAME = os.listdir('game')[0]
# shell = win32com.client.Dispatch("WScript.Shell")


        
def addtofile():
    if len(commands) >= command_length:
        del commands[0]
        commands.extend([user[1:] + out.lower()])
        if mode.lower() == "democracy":
            list_commands.extend([out.lower()])
    else:
        commands.extend([user[1:] + out.lower()])
        if mode.lower() == "democracy":
            list_commands.extend([out.lower()])

            
def democracy():
    global list_commands
    list_commands = []
    last_command = time.time()
    up_counter = 0
    right_counter = 0
    down_counter = 0
    left_counter = 0
    start_counter = 0
    select_counter = 0
    a_counter = 0
    b_counter = 0
    selected_c = "None"
    
    while True:
        if time.time() > last_command + democracy_time:
            last_command = time.time()
            for list_command in list_commands:
                if list_command == "up":
                    up_counter = up_counter + 1
                if list_command == "right":
                    right_counter = right_counter + 1
                if list_command == "down":
                    down_counter = down_counter + 1
                if list_command == "left":
                    left_counter = left_counter + 1
                if list_command == "a":
                    a_counter = a_counter + 1
                if list_command == "b":
                    b_counter = b_counter + 1
                if list_command == "start":
                    start_counter = start_counter + 1
                if list_command == "select":
                    select_counter = select_counter + 1
            alloutputs = {'Up': up_counter, 'Right': right_counter, 'Down': down_counter, 'Left': left_counter, 'Start': start_counter, 'Select': select_counter, 'B': b_counter, 'A': a_counter}
            if(up_counter + right_counter + down_counter + left_counter + start_counter + select_counter + b_counter + a_counter == 0):
                selected_c = "None"
            else:
                selected_c = max(alloutputs, key = alloutputs.get)
            with open("lastsaid.txt", "w") as f:
                f.write("Selected %s\n" % selected_c)
                f.write("Time left: %s" % str(democracy_time)[0:1])
            list_commands = []
            if selected_c.lower() == 'up':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('up_arrow')
            if selected_c.lower() == 'right':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('right_arrow')
            if selected_c.lower() == 'down':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('down_arrow')
            if selected_c.lower() == 'left':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('left_arrow')
            if selected_c.lower() == 'a':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('z')
            if selected_c.lower() == 'b':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('x')
            if selected_c.lower() == 'start':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('enter')
            if selected_c.lower() == 'select':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('backspace')
            up_counter = 0
            right_counter = 0
            down_counter = 0
            left_counter = 0
            start_counter = 0
            select_counter = 0
            a_counter = 0
            b_counter = 0
        else:
            with open("lastsaid.txt", "w") as f:
                f.write("Selected %s\n" % selected_c)
                f.write("Time left: %s" % str(1.0 + last_command + democracy_time - time.time())[0:1])
        time.sleep(1)
        
# Generate a config file if one doesn't exist
while True:
    if os.path.isfile("settings.txt"):
        config = ConfigParser.ConfigParser()
        config.read("settings.txt")
        HOST = config.get('Settings', 'HOST')
        PORT = config.getint('Settings', 'PORT')
        AUTH = config.get('Settings', 'AUTH')
        NICK = config.get('Settings', 'USERNAME').lower()
        APP = config.get('Settings', 'APP')
        CHAT_CHANNEL = config.get('Settings', 'CHAT_CHANNEL').lower()
        command_length = config.getint('Settings', 'LENGTH')
        QUICK_PRESS = config.getboolean('Settings', 'QUICK_PRESS')
        break
    else:
        print("Let's make you a config file")
        
        settings.append("[Settings]\n")
        
        settings.append("; Where you're connecting to, if it's Twitch leave it as is")
        print("Where you're connecting to, if it's Twitch use irc.twitch.tv")
        settings_host = raw_input("Hostname: ")
        settings.append("HOST = " + settings_host + "\n")
        
        settings.append("; Port number, probably should use 6667")
        print("Port number, probably should use 6667")
        settings_port = raw_input("Port: ")
        settings.append("PORT = " + settings_port + "\n")
        
        settings.append("; Auth token, grab this from http://www.twitchapps.com/tmi")
        print("Auth token, grab this from http://www.twitchapps.com/tmi")
        settings_auth = raw_input("Auth Token: ")
        settings.append("AUTH = " + settings_auth + "\n")
        
        settings.append("; Your Twitch Bot's Username")
        print("Your Twitch Bot's Username")
        settings_bot = raw_input("Bot's Username: ")
        settings.append("USERNAME = " + settings_bot + "\n")
        
        settings.append("; Name of the application you run the file from, I suggest VBA")
        print("Name of the application you run the file from, if Visual Boy Advance use VisualBoyAdvance")
        settings_app = raw_input("Application name: ")
        settings.append("APP = " + settings_app + "\n")
        
        settings.append("; Username of who's channel you're connecting to")
        print("Username of who's channel you're connecting to")
        settings_chat = raw_input("Username: ")
        settings.append("CHAT_CHANNEL = " + settings_chat + "\n")
        
        settings.append("; The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        print("The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        settings_length = raw_input("Length: ")
        settings.append("LENGTH = " + settings_length + "\n")
        
        settings.append("; Oh how to explain this...")
        settings.append("; You get the chat command 'Left'")
        settings.append("; You are currently facing right")
        settings.append("; If QUICK_PRESS is true you turn left")
        settings.append("; If QUICK_PRESS is false you turn left and move one square left")
        print("Oh how to explain this...")
        print("You get the chat command 'Left'")
        print("You are currently facing right")
        print("If QUICK_PRESS is true you turn left")
        print("If QUICK_PRESS is false you turn left and move one square left")
        settings_press = raw_input("QUICK PRESS: ")
        settings.append("QUICK_PRESS = " + settings_press + "\n")
        
        with open("settings.txt", "w") as f:
            for each_setting in settings:
                f.write(each_setting + '\n')
    
# Select game type    
while True:
    print("Currently available: Anarchy, Democracy")
    mode = raw_input("Game type: ")
    if mode.lower() == "anarchy":
        break
    if mode.lower() == "democracy":
        print("Takes most said command every X second(s): ")
        democracy_time = float(raw_input("(must be integer) X="))
        break

# Anarchy Game Mode
if mode.lower() == "anarchy":
    with open("lastsaid.txt", "w") as f:
        f.write("")
        
    print("Starting %s" % GAME)
    time.sleep(1)
    emulator_job = Thread(target = startemulator, args = ())
    emulator_job.start()
    
    s=socket.socket( )
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"));
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))
    print("Sent connected message to channel %s" % CHAT_CHANNEL)

    while 1:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer=temp.pop( )

        for line in temp:
            x = 0
            out = ""
            line = str.rstrip(line)
            line = str.split(line)

            for index, i in enumerate(line):
                if x == 0:
                    user = line[index]
                    user = user.split('!')[0]
                    user = user[0:12] + ": "
                if x == 3:
                    out += line[index]
                    out = out[1:]
                if x >= 4:
                    out += " " + line[index]
                x = x + 1
            
            # Respond to ping, squelch useless feedback given by twitch, print output and read to list
            if user == "PING: ":
                s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
            elif user == ":tmi.twitch.tv: ":
                pass
            elif user == ":tmi.twitch.: ":
                pass
            elif user == ":%s.tmi.twitch.tv: " % NICK:
                pass
            else:
                try:
                    print(user + out)
                except UnicodeEncodeError:
                    print(user)
                
            # Take in output
            if out.lower() == 'up':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('up_arrow')
                addtofile()
            if out.lower() == 'right':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('right_arrow')
                addtofile()
            if out.lower() == 'down':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('down_arrow')
                addtofile()
            if out.lower() == 'left':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('left_arrow')
                addtofile()
            if out.lower() == 'a':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('z')
                addtofile()
            if out.lower() == 'b':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('x')
                addtofile()
            if out.lower() == 'start':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('enter')
                addtofile()
            if out.lower() == 'select':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('backspace')
                addtofile()
                
            # Write to file for stream view
            with open("commands.txt", "w") as f:
                for item in commands:
                    f.write(item + '\n')

# Democracy Game Mode
if mode.lower() == "democracy":
    with open("lastsaid.txt", "w") as f:
        f.write("")

    count_job = Thread(target = democracy, args = ())
    count_job.start()
    #count_job.join()
    
    print("Starting %s" % GAME)
    time.sleep(1)
    emulator_job = Thread(target = startemulator, args = ())
    emulator_job.start()

    s=socket.socket( )
    s.connect((HOST, PORT))
    
    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"));
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))
    print("Sent connected message to channel %s" % CHAT_CHANNEL)

    while 1:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer=temp.pop( )
                
        for line in temp:
            x = 0
            out = ""
            line = str.rstrip(line)
            line = str.split(line)

            for index, i in enumerate(line):
                if x == 0:
                    user = line[index]
                    user = user.split('!')[0]
                    user = user[0:12] + ": "
                if x == 3:
                    out += line[index]
                    out = out[1:]
                if x >= 4:
                    out += " " + line[index]
                x = x + 1
            
            # Respond to ping, squelch useless feedback given by twitch, print output and read to list
            if user == "PING: ":
                s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
            elif user == ":tmi.twitch.tv: ":
                pass
            elif user == ":tmi.twitch.: ":
                pass
            elif user == ":%s.tmi.twitch.tv: " % NICK:
                pass
            else:
                try:
                    print(user + out)
                except UnicodeEncodeError:
                    print(user)
                
            # Take in output
            if out.lower() == 'up':
                addtofile()
            if out.lower() == 'right':
                addtofile()
            if out.lower() == 'down':
                addtofile()
            if out.lower() == 'left':
                addtofile()
            if out.lower() == 'a':
                addtofile()
            if out.lower() == 'b':
                addtofile()
            if out.lower() == 'start':
                addtofile()
            if out.lower() == 'select':
                addtofile()
                
            # Write to file for stream view
            with open("commands.txt", "w") as f:
                for item in commands:
                    f.write(item + '\n')