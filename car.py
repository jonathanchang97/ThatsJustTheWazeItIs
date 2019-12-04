import requests
import sys
import json
import time
import os
from gtts import gTTS

class Car:
    def __init__ (self, curr, dest, server, port=8080):
        self.prev = ""
        self.curr = curr
        self.dest = dest
        self.url = server
        self.port = port


    def loop(self):
        printAndSay(f"Beginning journey from {self.curr} to {self.dest}")

        while True:
            res = json.loads(requests.post(self.url, json = {"prev" : self.prev, "curr": self.curr, "dest": self.dest}).text)

            if not res["road"]:
                break
            else:
                printAndSay(f"Turn onto {res['road']}")
                printAndSay(f"Current expected remaining time left to {self.dest}: {res['total_wait']}")
                self.prev = self.curr
                self.curr = res['next']
                time.sleep(res['wait_time'])

        printAndSay("You have arrived at your destination")
        self.wait_time = 0


    def printAndSayAndSay(self, string):         
        tts = gTTS(text=string, lang='en')
        tts.save("speech.mp3")
        os.system("ffplay -nodisp -autoexit -volume 100 -loglevel quiet speech.mp3")
        print(string)
    

def main(argv):
    argc = len(argv)
    curr, dest, server = "", "", ""
    if argc == 4:
        curr = argv[1]
        dest = argv[2]
        server = argv[3]
    car = Car(curr, dest, server)
    car.loop()


if __name__ == "__main__":
    main(sys.argv)
