from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import os

# Import the modular classes
from modules.file_processor import FileProcessor
from modules.schema_processor import SchemaProcessor
from modules.workflow_executor import WorkflowExecutor

app = Flask(__name__)

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Flask API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

file_processor = FileProcessor()

# API 1: Upload CSV/TXT, select schema YAML and produce new CSV
@app.route('/process_file', methods=['POST'])
def process_file():
    try:
        file = request.files['file']
        schema_file = request.files['schema']
        
        # Save uploaded file
        filepath = file_processor.save_file(file)

        # Load and apply schema
        schema_processor = SchemaProcessor(schema_file)
        df = file_processor.read_file(filepath)
        processed_df = schema_processor.apply_schema(df)

        # Save the processed file
        output_file = file_processor.save_csv(processed_df, f'processed_{file.filename}')

        return jsonify({'message': 'File processed successfully', 'output_file': output_file}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API 2: Run a workflow from a YAML file and produce output CSV
@app.route('/run_workflow', methods=['POST'])
def run_workflow():
    try:
        workflow_file = request.files['workflow']
        data_file = request.files['data']

        # Execute the workflow
        workflow_executor = WorkflowExecutor(workflow_file, data_file)
        processed_df = workflow_executor.execute_workflow()

        # Save the workflow output to a CSV
        output_file = file_processor.save_csv(processed_df, 'workflow_output.csv')

        return jsonify({'message': 'Workflow executed successfully', 'output_file': output_file}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
