from flask_restx import Namespace, Resource, fields
from flask import request
from services.file_service import FileService

# Define the namespace
file_ns = Namespace('files', description="Operations related to file processing")

# Input/output models for Swagger documentation
file_upload = file_ns.model('FileUpload', {
    'schema': fields.String(required=True, description="Schema to apply to the file")
})

file_response = file_ns.model('FileResponse', {
    'message': fields.String,
    'output_file': fields.String
})

# File Service
file_service = FileService()

@file_ns.route('/')
class FileProcessor(Resource):
    @file_ns.expect(file_upload)  # Automatically generates Swagger form for input
    @file_ns.marshal_with(file_response)  # Automatically documents the response structure
    def post(self):
        """Upload a file and apply a schema to process it"""
        schema = request.json.get('schema')
        file = request.files['file']

        # Call the service to process the file
        response = file_service.process_file(file, schema)
        return response
