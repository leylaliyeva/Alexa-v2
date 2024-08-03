from flask import Flask, request
import KEGemini
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest, start_http_server, Summary, Counter, Histogram

app = Flask(__name__)
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Number of requests processed')
ERROR_COUNT = Counter('error_count', 'Number of errors encountered')
REQUEST_IN_PROGRESS = Gauge('requests_in_progress', 'Number of requests in progress')

@app.route("/",methods=["POST"])
@REQUEST_TIME.time()
def slash():
  js = request.get_json()
  t = js.get("text")
  if t != None:
    u = KEGemini.ke(t) 
    if u != None:
      return {"text":u},200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

@app.route("/metrics", methods=["GET"])
def metrics():
    registry = CollectorRegistry()
    registry.register(REQUEST_TIME)
    registry.register(REQUEST_COUNT)
    registry.register(ERROR_COUNT)
    registry.register(REQUEST_IN_PROGRESS)
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
  app.run(host="localhost",port=3005)
