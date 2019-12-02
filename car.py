import requests
import sys
import json
import time
import os
from gtts import gTTS

class Car:
    def __init__ (self, curr, dest, server, port=8080):
        self.curr = curr
        self.dest = dest
        self.url = server
        self.port = port
        self.wait_time = 0
    
    def loop(self):
        print(f"Beginning journey from {self.curr} to {self.dest}")
        while True:
            time.sleep(self.wait_time) 
            res = json.loads(requests.post(self.url, json = {"curr": self.curr, "dest": self.dest}).text)
            if self.dest == res["curr"]:
                break
            if res["dir"] == "straight":
                tts = gTTS(text=f"Continue straight on {self.curr}", lang='en')
                tts.save("speech.mp3")
                os.system("mpg123 speech.mp3")
            else:
                tts = gTTS(text=f"Turn on {self.curr}", lang='en')
                tts.save("speech.mp3")
                os.system("mpg123 speech.mp3")
            self.curr = res['curr']
            self.wait_time = res['wait_time']

        print("You have arrived at your destination")


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
