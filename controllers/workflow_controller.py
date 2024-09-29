from flask_restx import Namespace, Resource, fields
from flask import request
from services.workflow_service import WorkflowService

# Define the namespace
workflow_ns = Namespace('workflows', description="Operations related to workflows")

# Input/output models for Swagger documentation
workflow_model = workflow_ns.model('Workflow', {
    'workflow_type': fields.String(required=True, description="Type of workflow to execute")
})

workflow_response = workflow_ns.model('WorkflowResponse', {
    'message': fields.String,
    'output_file': fields.String
})

# Workflow Service
workflow_service = WorkflowService()

@workflow_ns.route('/')
class WorkflowExecutor(Resource):
    @workflow_ns.expect(workflow_model)  # Automatically generates Swagger form for input
    @workflow_ns.marshal_with(workflow_response)  # Automatically documents the response structure
    def post(self):
        """Execute a workflow with the provided data"""
        workflow_type = request.json.get('workflow_type')
        data_file = request.files['data']

        # Call the service to execute the workflow
        response = workflow_service.execute_workflow(data_file, workflow_type)
        return response
