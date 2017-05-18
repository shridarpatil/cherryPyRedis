import requests
import redis
import json
import cherrypy
import collections
import cherrypy.process.plugins
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket


conn = redis.Redis('localhost')
def background():
	requests.get("http://127.0.0.1:3000")
	pass

wd = cherrypy.process.plugins.BackgroundTask(300, background)
wd.start()

class niftyWebSocketPlugin(WebSocketPlugin):
  def __init__(self, bus):
    WebSocketPlugin.__init__(self, bus)
    self.clients = {}

  def start(self):
    WebSocketPlugin.start(self)
    self.bus.subscribe('add-client', self.add_client)

  def stop(self):
    WebSocketPlugin.stop(self)
    self.bus.unsubscribe('add-client', self.add_client)

  def add_client(self, name, websocket):
    self.clients[name] = websocket

def CORS():
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
	pass


class niftySocketHandler(WebSocket):
    def opened(self):
        cherrypy.engine.publish('add-client', self.username, self)

class Nifty50(object):

	@cherrypy.expose	
	def index(self):		
		status = self.getData()
		return status

	def convert(self, data):
		if isinstance(data, basestring):
				return str(data)
		elif isinstance(data, collections.Mapping):
				return dict(map(self.convert, data.iteritems()))
		elif isinstance(data, collections.Iterable):
				return type(data)(map(self.convert, data))
		else:
			return data

	def getData(self):
		
		
		topGainers = requests.get("https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json").json()

		topLosers = requests.get("https://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json").json()


		conn.hmset("topGainers", self.convert(topGainers))
		conn.hmset("topLosers", self.convert(topLosers))

		cherrypy.engine.publish('websocket-broadcast', json.dumps({"topGainers" : topGainers["data"], "topLosers" : topLosers["data"]}))

		return "Data saved Successfully"

	@cherrypy.expose
	def displayData(self):
		
		topLosers = conn.hgetall("topLosers")
		topGainers = conn.hgetall("topGainers")
	
		return json.dumps({"topGainers" : topGainers["data"], "topLosers" : topLosers["data"]})

	@cherrypy.expose
	def ws(self, username):
			cherrypy.request.ws_handler.username = username
			cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))
	index.exposed = True

if __name__ == '__main__':

	conf = {
    '': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        'tools.CORS.on': True,
        'tools.response_headers.headers': [("Access-Control-Allow-Origin", "*")],
        },
    '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': niftySocketHandler,
            'tools.websocket.protocols': ['zerodha']
            },
    }
	
	cherrypy.config.update({
                        'tools.CORS.on': True,
												'server.socket_host':'0.0.0.0',
                        'server.socket_port': 3000, # default port is 8080 you can chage default port number here
                       })
	cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
	niftyWebSocketPlugin(cherrypy.engine).subscribe()
	cherrypy.tools.websocket = WebSocketTool()
	cherrypy.quickstart(Nifty50(), '', conf)
