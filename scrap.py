import requests
import redis
import json
import cherrypy

import threading
import time

def background():
	
 
# Wait for 5 seconds

	while  True:

		time.sleep(300)
		print "Getting Data"
		
		requests.get("http://127.0.0.1:8080")
		
threading.Thread(target=background).start()


class HelloWorld(object):
		@cherrypy.expose	
		def index(self):
				
				status = self.getData()
				return status


		def getData(self):
				conn = redis.Redis('localhost')
				self.conn = conn
				topGainers = requests.get("https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json")

				topLosers = requests.get("https://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json")

				

				
				topLosers = json.loads(topLosers.text)
				topGainers = json.loads(topGainers.text)

				conn.hmset("topGainers", topGainers)

				conn.hmset("topLosers", topLosers)

				return "Data saved Successfully"
		@cherrypy.expose
		def displayData(self):
				conn = redis.Redis('localhost')
				topLosers = conn.hgetall("topLosers")
				topGainers = conn.hgetall("topGainers")

				print topGainers

				return json.dumps({"topGainers" : topGainers['data'], "topLosers":topLosers['data']})
		index.exposed = True
if __name__ == '__main__':
	cherrypy.quickstart(HelloWorld())





