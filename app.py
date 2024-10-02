from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage
from gevent.pywsgi import WSGIServer
from controller import process_csv_with_schema

app = Flask(__name__)

# Initialize the Flask-RESTx API and enable Swagger documentation
api = Api(app, 
          version='1.0', 
          title='CSV Processor API', 
          description='A simple API to process CSV files with a schema validation',
          doc='/swagger'  # You can access Swagger UI at http://localhost:5000/swagger
         )

# Define the namespace for grouping resources
ns = api.namespace('csv', description='Operations related to CSV processing')

# Define the input model for Swagger (file + schema)
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='CSV file to upload')
upload_parser.add_argument('schema', type=str, required=True, help='Schema in JSON format')

# Define the expected response structure
csv_response_model = api.model('CSVResponse', {
    'message': fields.String(description='Status message'),
    'data': fields.List(fields.Raw, description='Processed CSV data'),
    'error': fields.String(description='Error message, if any'),
    'details': fields.String(description='Details about errors, if applicable')
})

# Define routes and endpoints
@ns.route('/upload')
class CSVUpload(Resource):
    @api.expect(upload_parser)
    @api.response(200, 'CSV successfully processed', csv_response_model)
    @api.response(400, 'Invalid input data', csv_response_model)
    def post(self):
        '''Upload CSV with a validation schema'''
        args = upload_parser.parse_args()
        csv_file = args['file']
        schema_text = args['schema']

        if not schema_text or not csv_file:
            return {"error": "Schema and CSV file are required."}, 400

        # Process CSV and schema
        csv_content = csv_file.read().decode('utf-8')  # Read CSV file contents
        result = process_csv_with_schema(csv_content, schema_text)
        return jsonify(result)

if __name__ == '__main__':
    # Run with Gevent WSGI Server
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
