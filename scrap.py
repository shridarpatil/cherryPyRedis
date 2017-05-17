import requests
import redis
import json, ast
import cherrypy
import collections
from cherrypy.process.plugins import Monitor




def background():
	requests.get("http://127.0.0.1:8080")
	pass
		
def CORS():
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
	pass

class Nifty50(object):

	@cherrypy.expose	
	def index(self):
		print ("Getting data.............")
		
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
		conn = redis.Redis('localhost')
		self.conn = conn
		topGainers = requests.get("https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json").json()

		topLosers = requests.get("https://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json").json()


		conn.hmset("topGainers", self.convert(topGainers))
		conn.hmset("topLosers", self.convert(topLosers))

		return "Data saved Successfully"

	@cherrypy.expose
	def displayData(self):
		conn = redis.Redis('localhost')
		topLosers = conn.hgetall("topLosers")
		topGainers = conn.hgetall("topGainers")
	
		return json.dumps({"topGainers" : topGainers["data"], "topLosers" : topLosers["data"]})
	index.exposed = True

if __name__ == '__main__':

	conf = {
    '': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        'tools.CORS.on': True,
        'tools.response_headers.headers': [("Access-Control-Allow-Origin", "*")],
        }
    }
	
	cherrypy.config.update({
                        'tools.CORS.on': True,
                        #'server.socket_port': 3000  default port is 8080 you can chage default port number here
                       })
	cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
	Monitor(cherrypy.engine, background, frequency=30).subscribe()
	cherrypy.quickstart(Nifty50(), '', conf)