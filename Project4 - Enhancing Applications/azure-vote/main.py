from flask import Flask, request, render_template
import os
import random
import redis
import socket
import sys
import logging
from datetime import datetime

# App Insights
# TODO: Import required libraries for App Insights
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.log_exporter import AzureEventHandler
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module
from opencensus.trace import config_integration
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

# For metrics
stats = stats_module.stats
view_manager = stats.view_manager

inst_key = 'InstrumentationKey=f5aa29d6-f564-4ca2-b477-1c6956ff22a0;IngestionEndpoint=https://westus-0.in.applicationinsights.azure.com/'

# Logging
config_integration.trace_integrations(['logging'])
config_integration.trace_integrations(['requests'])
# Standard Logging
logger = logging.getLogger(__name__) 
handler = AzureLogHandler(connection_string=inst_key)
handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
logger.addHandler(handler)
logger.addHandler(AzureEventHandler(connection_string=inst_key)) #custom events
logger.setLevel(logging.INFO) #set the logging level
# logger.info("logger set up successfully")
# logger.info("app_insights_instrumentation_key = {}".format(inst_key)) 
print("logger set up successfully")
print("app_insights_instrumentation_key = {}".format(inst_key))# TODO: Setup logger

# Metrics
exporter = metrics_exporter.new_metrics_exporter(
    enable_standard_metrics=True,
    connection_string=inst_key) # TODO: Setup exporter
view_manager.register_exporter(exporter)
# logger.info("metrics set up successfully")
print("metrics set up successfully")

# Tracing
tracer = Tracer(
    exporter=AzureExporter(
        connection_string=inst_key),
        sampler=ProbabilitySampler(1.0),
)# TODO: Setup tracer

# logger.info("tracer set up successfully")
print("tracer set up successfully")

app = Flask(__name__)

# Requests
middleware = FlaskMiddleware(
 app,
 exporter=AzureExporter(connection_string=inst_key),
 sampler=ProbabilitySampler(rate=1.0)
)# TODO: Setup flask middleware
# logger.info("requests set up successfully")
# logger.warning("**********setup completed**********")
print("requests set up successfully")
print("**********setup completed**********")

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

#if we want to run on vmss the following should be uncommented and the Redis configuration should be commented out
#as it is, it's set up for cluster run
# Redis Connection
#r = redis.Redis()

# Redis configurations
redis_server = os.environ['REDIS']

# Redis Connection to another container
try:
    if "REDIS_PWD" in os.environ:
        r = redis.StrictRedis(host=redis_server,
                        port=6379,
                        password=os.environ['REDIS_PWD'])
    else:
        r = redis.Redis(redis_server)
    r.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis
if not r.get(button1): r.set(button1,0)
if not r.get(button2): r.set(button2,0)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        vote1 = r.get(button1).decode('utf-8')
        # TODO: use tracer object to trace cat vote
        with tracer.span(name="Voted Cat") as span:
            print("Voted Cat")
        vote2 = r.get(button2).decode('utf-8')
        # TODO: use tracer object to trace dog vote
        with tracer.span(name="Voted Dog") as span:
            print("Voted Dog")

        # Return index with values
        return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':

            # Empty table and return results
            r.set(button1,0)
            r.set(button2,0)
            vote1 = r.get(button1).decode('utf-8')
            properties = {'custom_dimensions': {'Cats': vote1}}
            # TODO: use logger object to log cat vote
            logger.info('Cats', extra=properties)

            vote2 = r.get(button2).decode('utf-8')
            properties = {'custom_dimensions': {'Dogs': vote2}}
            # TODO: use logger object to log dog vote
            logger.warning('Dogs', extra=properties)

            return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

        else:

            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote,1)

            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            properties = {'custom_dimensions': {'Cats': vote1}}
            # TODO: use logger object to log cat vote
            logger.info('Cats', extra=properties)
            vote2 = r.get(button2).decode('utf-8')
            properties = {'custom_dimensions': {'Dogs': vote2}}
            # TODO: use logger object to log dog vote
            logger.warning('Dogs', extra=properties)

            # Return results
            return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

if __name__ == "__main__":
    # comment line below when deploying to VMSS
    # app.run() # local
    # uncomment the line below before deployment to VMSS
    app.run(host='0.0.0.0', threaded=True, debug=True) # remote