from flask import Flask
from flask_restx import Api
from controllers.file_controller import file_ns
from controllers.workflow_controller import workflow_ns
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# Configure Swagger documentation
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    app, 
    version="1.0", 
    title="File and Workflow API", 
    description="A simple API for file processing and workflow management.",
    authorizations=authorizations,
    security='apikey',  # Optional: Specify security scheme (like API Key or OAuth2)
    doc="/docs"  # URL for Swagger UI (default is /)
)

# Register Namespaces (Controllers)
api.add_namespace(file_ns, path='/api/v1/files')
api.add_namespace(workflow_ns, path='/api/v1/workflows')

if __name__ == '__main__':
    # Use Gevent's pywsgi server to run the Flask application
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    print("Starting Gevent WSGI Server on http://localhost:5000")
    http_server.serve_forever()
