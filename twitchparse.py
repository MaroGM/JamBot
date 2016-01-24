
import os
import socket
import random
from threading import Thread

class TwitchParse(object):
    def __init__(self, twitch_host, twitch_port, twitch_auth, twitch_user, twitch_chatchannel):
        self.twitch_host = twitch_host
        self.twitch_port = int(twitch_port)
        self.twitch_auth = twitch_auth
        self.twitch_user = twitch_user
        self.twitch_chatchannel = twitch_chatchannel

        self.votes = { 'up':0, 'down':0, 'left':0, 'right':0, 'center':0 }
        self.readbuffer = ""

    def start(self):
        s = socket.socket()
        s.connect((self.twitch_host, self.twitch_port))

        s.send("PASS %s\r\n" % self.twitch_auth)
        s.send("NICK %s\r\n" % self.twitch_user)
        s.send("USER %s %s bla :%s\r\n" % (self.twitch_user, self.twitch_host, self.twitch_user))
        s.send("JOIN #%s\r\n" % self.twitch_chatchannel)
        s.send("PRIVMSG #%s :Connected\r\n" % self.twitch_chatchannel)
        print("Sent connected message to channel %s" % self.twitch_chatchannel)

        while True:

            self.readbuffer = self.readbuffer + s.recv(1024).decode("UTF-8", errors="ignore")
            self.readbuffer = str(self.readbuffer)
            temp = str.split(self.readbuffer, "\n")
            self.readbuffer=temp.pop( )
                    
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
                    s.send("PONG tmi.twitch.tv\r\n")
                elif user == ":tmi.twitch.tv: ":
                    pass
                elif user == ":tmi.twitch.: ":
                    pass
                elif user == ":%s.tmi.twitch.tv: " % self.twitch_user:
                    pass
                # else:
                #     try:
                #         print(user + out)
                #     except UnicodeEncodeError:
                #         print(user)

                if out.lower() in ('up', 'down', 'left', 'right', 'center'):
                    self.votes[out.lower()] += 1


    def getVotes(self):
        largest = self.votes[max(self.votes, key=self.votes.get)]

        if largest > 0:
            results = []

            for key, value in self.votes.items():
                if value == largest:
                    results.append(key)

            # Take random from highest vote pool
            outcome = random.choice(results)

        else:
            outcome = 'none'

        # Reset votes
        self.votes = { 'up':0, 'down':0, 'left':0, 'right':0, 'center':0 }

        return outcome












