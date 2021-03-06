#
# server.py
# Purpose:
#
# To make this concurrent without using ThreadingMixIn, we turned to the source
# code for socketserver: https://github.com/python/cpython/blob/master/Lib/socketserver.py?fbclid=IwAR0ujDLy_1Au6nVBodpbc5uXQxMoJ7kC2v7Idhn79qduA5J499tNV9TzB-I
# We used this code directly instead calling serve_forever() so we could process
# the requests concurrently.
#

from http.server import BaseHTTPRequestHandler
import socketserver
import time
import json
import threading
import selectors
from myQueue import SynchronizedQueue
import navigation as nav
import map

PORT        = 8080
NUM_THREADS = 100

nav_solution = nav.Navigation("example.txt")

if hasattr(selectors, 'PollSelector'):
    _ServerSelector = selectors.PollSelector
else:
    _ServerSelector = selectors.SelectSelector


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """ Callback function for handling a POST HTTP request. 
            Uses shared Navigation object to process navigation logic 
            and writes next turn in JSON format to the socket"""
        fields= self.headers.as_string().split('\n')
        output = {}
        for field in fields:
            kv = field.split(':')
            if len(kv) >= 2:
                output[kv[0]] = kv[1]
        # Get content length so we can read that many bytes from the socket
        post_body = self.rfile.read(int(output['Content-Length']))
        body = json.loads(post_body)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(nav_solution.requestMapUpdate(body), "utf-8"))

def consumer(queue_):
    """ Busy waits for work queue to be non-empty and pulls request off (thread 
        safe) when it is. Calls handle_request which calls the Handler do_POST
        callback """
    while True:
        httpd = queue_.get()
        httpd.handle_request()

def main():
        """ Initialize thread pool and work queue, then listen on 
            PORT for HTTP requests """
        queue_ = SynchronizedQueue()
        threads = [threading.Thread(target=consumer, 
                                    args=[queue_]) for _ in range(NUM_THREADS)]

        for thread in threads:
            thread.start()
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            with _ServerSelector() as selector:
                selector.register(httpd, selectors.EVENT_READ)
                while True:
                    ready = selector.select()
                    if ready:
                        queue_.put(httpd)
                httpd.service_actions()

if __name__ == '__main__':
    main()
