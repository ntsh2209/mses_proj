from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from flask import request, jsonify
from io import StringIO
import pandas as pd

# Create a new namespace for workflow-related routes
ns = Namespace('workflow', description='Operations related to workflow processing')

# Define the input model for Swagger (workflow type + file)
workflow_parser = ns.parser()
workflow_parser.add_argument('file', location='files', type=FileStorage, required=True, help='CSV file to upload')
workflow_parser.add_argument('workflow_type', type=str, required=True, help='Type of workflow to apply')

# Define the expected response structure for Swagger
workflow_response_model = ns.model('WorkflowResponse', {
    'message': fields.String(description='Status message'),
    'data': fields.List(fields.Raw, description='Processed CSV data'),
    'error': fields.String(description='Error message, if any'),
    'details': fields.String(description='Details about errors, if applicable')
})

# Define routes and endpoints for workflow processing
@ns.route('/process')
class CSVWorkflow(Resource):
    @ns.expect(workflow_parser)
    @ns.response(200, 'Workflow successfully applied', workflow_response_model)
    @ns.response(400, 'Invalid input data', workflow_response_model)
    def post(self):
        '''Upload CSV and apply workflow'''
        args = workflow_parser.parse_args()
        csv_file = args['file']
        workflow_type = args['workflow_type']

        if not workflow_type or not csv_file:
            return {"error": "Workflow type and CSV file are required."}, 400

        # Process CSV based on workflow type
        csv_content = csv_file.read().decode('utf-8')  # Read CSV file contents
        result = process_csv_workflow(csv_content, workflow_type)
        return jsonify(result)

# Logic to handle different workflows
def process_csv_workflow(csv_file_content, workflow_type):
    '''Process CSV based on the workflow type'''
    try:
        csv_data = StringIO(csv_file_content)
        df = pd.read_csv(csv_data)
    except Exception as e:
        return {"error": "Failed to process CSV", "details": str(e)}

    if workflow_type == "filter_by_age":
        if 'age' not in df.columns:
            return {"error": "Column 'age' is missing in CSV"}
        filtered_df = df[df['age'] > 30]
        return {"message": "Workflow 'filter_by_age' applied successfully", "data": filtered_df.to_dict(orient='records')}

    elif workflow_type == "sort_by_name":
        if 'name' not in df.columns:
            return {"error": "Column 'name' is missing in CSV"}
        sorted_df = df.sort_values(by='name')
        return {"message": "Workflow 'sort_by_name' applied successfully", "data": sorted_df.to_dict(orient='records')}

    else:
        return {"error": f"Unknown workflow type: {workflow_type}"}
