from pygame import *
import io
import base64

screen = Surface((1, 1), SRCALPHA)
screen.fill((0, 0, 0, 0))
currentScreen = io.BytesIO(b"")
mousepos = [0, 0]

def _savedisplay():
	global currentScreen
	draw.line(screen, (0, 0, 0), (0, mousepos[1]), (screen.get_width(), mousepos[1]), 1)
	draw.line(screen, (0, 0, 0), (mousepos[0], 0), (mousepos[0], screen.get_height()))
	currentScreen = io.BytesIO(b"")
	image.save(screen, currentScreen, ".png")
_savedisplay()
display.flip = _savedisplay

def _setscrnsize(size, flags = 0):
	global screen
	screen = Surface(size, SRCALPHA)
	screen.fill((0, 0, 0, 0))
	return screen
display.set_mode = _setscrnsize

events = []
keys = [False for x in range(512)]
K_UP = 341
K_LEFT = 332
K_DOWN = 324
K_RIGHT = 338
class CustomMouseDownEvent:
	def __init__(self, pos):
		self.type = MOUSEBUTTONDOWN
		self.pos = (*pos,)
		self.button = 1
class CustomKeyDownEvent:
	def __init__(self, key):
		self.type = KEYDOWN
		self.key = key
class CustomKeyUpEvent:
	def __init__(self, key):
		self.type = KEYUP
		self.key = key
def _getevents():
	global events
	r = [p for p in events]
	events = []
	return r
event.get = _getevents

mouse.get_pressed = lambda : [False];

def _getkeypresses():
	class CustomKeyMap:
		def __getitem__(self, a):
			return keys[a]
	return CustomKeyMap()
key.get_pressed = _getkeypresses

def _getScreenURL():
	currentScreen.seek(0)
	b = base64.b64encode(currentScreen.read())
	return f"data:image/png;base64,{b.decode('UTF-8')}"

mouse.get_pos = lambda : mousepos

# --- SERVER ---

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

hostName = "0.0.0.0"
serverPort = 11233

def read_file(filename):
	f = open(filename, "r")
	t = f.read()
	f.close()
	return t

def bin_read_file(filename):
	f = open(filename, "rb")
	t = f.read()
	f.close()
	return t

def write_file(filename, content):
	f = open(filename, "w")
	f.write(content)
	f.close()

def get(path):
	if path == "/":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": "<html><head><title>Pygame</title><style>*{margin:0px;}</style></head>\n<body>\n\
	<img src onclick='c(event)'>" + """<script>//window.addEventListener("error",(e)=>alert(e.message + " (in " + e.filename + ":" + e.lineno + ")"))</script>
<script>var c = function (e) {
	var x = new XMLHttpRequest();
	x.open("POST", "/click");
	x.send(e.offsetX + "\\n" + e.offsetY);
}\n
var u = function () {
	var x = new XMLHttpRequest();
	x.open("GET", "/getimgurl");
	x.addEventListener("loadend", function () {
		document.querySelector("img").src = x.responseText
	})
	x.send();
}
console.log(setInterval(u, 100));
function getCharCode(c) {
	if (c.length >= 6) return 256 + c[5].charCodeAt();
	return c.charCodeAt();
}
window.addEventListener("keydown", (e) => {
	var x = new XMLHttpRequest();
	x.open("POST", "/keydown");
	x.send(getCharCode(e.key));
})
window.addEventListener("keyup", (e) => {
	var x = new XMLHttpRequest();
	x.open("POST", "/keyup");
	x.send(getCharCode(e.key));
})
</script>
	\n</body></html>"""
		}
	elif path == "/getimgurl":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/plain"
			},
			"content": _getScreenURL()
		}
	else:
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": f"<html><head><title>???</title></head>\n<body>\n\
	<h1>Not Found</h1><p><a href='/' style='color: rgb(0, 0, 238);'>Return home</a></p>\
	\n</body></html>"
		}

def post(path, body):
	global mousepos
	if path == "/click":
		pos = [int(body.decode("UTF-8").split("\n")[0]), int(body.decode("UTF-8").split("\n")[1])]
		mousepos = pos
		events.append(CustomMouseDownEvent(pos))
		return {
			"status": 200,
			"headers": {},
			"content": ""
		}
	elif path == "/keydown":
		k = int(body.decode("UTF-8"))
		keys[k] = True
		events.append(CustomKeyDownEvent(k))
		return {
			"status": 200,
			"headers": {},
			"content": ""
		}
	elif path == "/keyup":
		k = int(body.decode("UTF-8"))
		keys[k] = False
		events.append(CustomKeyUpEvent(k))
		return {
			"status": 200,
			"headers": {},
			"content": ""
		}
	else:
		print(f"Bad POST to {path}")
		return {
			"status": 404,
			"headers": {},
			"content": "404"
		}

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		res = get(self.path)
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		c = res["content"]
		if type(c) == str: c = c.encode("utf-8")
		self.wfile.write(c)
	def do_POST(self):
		res = post(self.path, self.rfile.read(int(self.headers["Content-Length"])))
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		self.wfile.write(res["content"].encode("utf-8"))
	def log_message(self, format: str, *args) -> None:
		return;
		if 400 <= int(args[1]) < 500:
			# Errored request!
			print(u"\u001b[31m", end="")
		print(args[0].split(" ")[0], "request to", args[0].split(" ")[1], "(status code:", args[1] + ")")
		print(u"\u001b[0m", end="")
		# don't output requests

def stopserver():
	global running
	running = False

def async_servermanager():
	global running
	global webServer
	running = True
	webServer = HTTPServer((hostName, serverPort), MyServer)
	webServer.timeout = 1
	print("Server started http://%s:%s" % (hostName, serverPort))
	while running:
		try:
			webServer.handle_request()
		except KeyboardInterrupt:
			running = False
	webServer.server_close()
	print("Server stopped")
	print("Press Enter to exit...")
servermanagerthread = threading.Thread(target=async_servermanager, name="server-manager-thread", args=[])
servermanagerthread.start()
