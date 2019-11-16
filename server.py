from http.server import BaseHTTPRequestHandler
import socketserver
import time
import json

PORT        = 8080
NUM_THREADS = 100

MAP = {} # TODO: replace with map class object

def requestMapUpdate(request):
	print("in requestMapUpdate")
	time.sleep(10)
	return json.dumps({"curr": "Packard Ave", "dir" : "left", "wait_time" : 7})


class GetHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		print("got post!!")
		fields= self.headers.as_string().split('\n')
		output = {}
		for field in fields: 
			kv = field.split(':')
			if len(kv) >= 2:
				output[kv[0]] = kv[1]

		post_body = self.rfile.read(int(output['Content-Length']))
		body = json.loads(post_body)
		self.wfile.write(bytes(requestMapUpdate(body), "utf-8"))
		return self.send_response(200)

def main():
	with socketserver.TCPServer(("", PORT), GetHandler) as httpd:
		print("serving at port", PORT)
		httpd.serve_forever()


if __name__ == '__main__':
	main()