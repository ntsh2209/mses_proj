from flask import Flask
from flask_restx import Api
from controller import ns as csv_ns
from workflow_controller import ns as workflow_ns
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# Initialize the Flask-RESTx API
api = Api(app, 
          version='1.0', 
          title='CSV and Workflow API', 
          description='API to process CSV files and handle workflows',
          doc='/swagger'  # Swagger UI at http://localhost:5000/swagger
         )

# Add namespaces
api.add_namespace(csv_ns, path='/csv')
api.add_namespace(workflow_ns, path='/workflow')

if __name__ == '__main__':
    # Run with Gevent WSGI Server
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
