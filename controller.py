import pandas as pd
import json
import yaml
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from flask import request, jsonify
from io import StringIO

# Create a new namespace for CSV-related routes
ns = Namespace('csv', description='Operations related to CSV processing')

# Define the input model for Swagger (file + schema)
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='CSV file to upload')
upload_parser.add_argument('schema', type=str, required=True, help='Schema in JSON format')

# Define the input model for modifying CSV using a YAML file
yaml_parser = ns.parser()
yaml_parser.add_argument('file', location='files', type=FileStorage, required=True, help='CSV file to upload')
yaml_parser.add_argument('schema', location='files', type=FileStorage, required=True, help='YAML schema file to upload')

# Define the expected response structure for Swagger
csv_response_model = ns.model('CSVResponse', {
    'message': fields.String(description='Status message'),
    'data': fields.List(fields.Raw, description='Processed CSV data'),
    'error': fields.String(description='Error message, if any'),
    'details': fields.String(description='Details about errors, if applicable')
})

# Define routes and endpoints for CSV processing
@ns.route('/upload')
class CSVUpload(Resource):
    @ns.expect(upload_parser)
    @ns.response(200, 'CSV successfully processed', csv_response_model)
    @ns.response(400, 'Invalid input data', csv_response_model)
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

@ns.route('/modify-with-yaml')
class CSVModifyWithYAML(Resource):
    @ns.expect(yaml_parser)
    @ns.response(200, 'CSV successfully modified', csv_response_model)
    @ns.response(400, 'Invalid input data', csv_response_model)
    def post(self):
        '''Modify CSV using a provided YAML schema'''
        args = yaml_parser.parse_args()
        csv_file = args['file']
        yaml_schema_file = args['schema']

        if not yaml_schema_file or not csv_file:
            return {"error": "YAML schema and CSV file are required."}, 400

        # Read the CSV content
        csv_content = csv_file.read().decode('utf-8')
        try:
            df = pd.read_csv(StringIO(csv_content))
        except Exception as e:
            return {"error": "Failed to read CSV", "details": str(e)}

        # Read the YAML schema content
        try:
            yaml_content = yaml.safe_load(yaml_schema_file.read())
        except yaml.YAMLError as e:
            return {"error": "Failed to read YAML schema", "details": str(e)}

        # Modify the CSV based on the YAML schema
        result = modify_csv_with_yaml(df, yaml_content)
        if 'error' in result:
            return jsonify(result), 400

        return jsonify({"message": "CSV successfully modified", "data": result})

# Helper function to process the schema and modify the CSV accordingly
def modify_csv_with_yaml(df, yaml_schema):
    try:
        # Example: renaming columns based on the schema
        if 'rename_columns' in yaml_schema:
            rename_mapping = yaml_schema['rename_columns']
            df.rename(columns=rename_mapping, inplace=True)

        # Example: dropping columns based on the schema
        if 'drop_columns' in yaml_schema:
            columns_to_drop = yaml_schema['drop_columns']
            df.drop(columns=columns_to_drop, inplace=True)

        # Example: filling missing values based on the schema
        if 'fill_na' in yaml_schema:
            fill_values = yaml_schema['fill_na']
            df.fillna(value=fill_values, inplace=True)

        # If modification passes, return modified data
        return df.to_dict(orient='records')
    
    except Exception as e:
        return {"error": "Failed to modify CSV", "details": str(e)}

# Logic to handle schema validation
def process_csv_with_schema(csv_file_content, schema_text):
    '''Process the CSV file content against the provided schema'''
    try:
        schema = json.loads(schema_text)
    except ValueError as e:
        return {"error": "Invalid schema format", "details": str(e)}

    try:
        csv_data = StringIO(csv_file_content)
        df = pd.read_csv(csv_data)
    except Exception as e:
        return {"error": "Failed to process CSV", "details": str(e)}

    for column, dtype in schema.items():
        if column not in df.columns:
            return {"error": f"Missing column {column} in CSV"}
        if str(df[column].dtype) != dtype:
            return {"error": f"Invalid datatype for column {column}. Expected {dtype}, found {df[column].dtype}"}

    return {"message": "CSV validated successfully", "data": df.to_dict(orient='records')}
