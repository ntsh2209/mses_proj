from flask import Flask
from flask_restx import Api
from book_controller import books_ns  # Import the namespace from your book_controller
from gevent.pywsgi import WSGIServer
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize the Flask-RESTX API without authorization
api = Api(
    app, 
    version="1.0", 
    title="Book Management API", 
    description="An API for managing a list of books, including uploading via CSV and deleting by ID.",
    doc="/docs"  # Swagger UI path
)

# Register the Books namespace
api.add_namespace(books_ns, path='/api/v1/books')

if __name__ == '__main__':
    # Use Gevent's pywsgi server to run the Flask application
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    print("Starting Gevent WSGI Server on http://localhost:5000")
    http_server.serve_forever()
