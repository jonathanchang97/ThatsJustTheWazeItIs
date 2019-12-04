import requests
import sys
import json
import time

class Car:
    def __init__ (self, curr, dest, server, port=8080):
        self.prev = ""
        self.curr = curr
        self.dest = dest
        self.url = server
        self.port = port


    def loop(self):
        print(f"Beginning journey from {self.curr} to {self.dest}")

        while True:
            res = json.loads(requests.post(self.url, json = {"prev" : self.prev, "curr": self.curr, "dest": self.dest}).text)

            if not res["road"]:
                break
            else:
                print(f"Turn onto {res['road']}")
                print(f"Current expected remaining time left to {self.dest}: {res['total_wait']}")
                self.prev = self.curr
                self.curr = res['next']
                time.sleep(res['wait_time'])

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
