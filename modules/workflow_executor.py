import os
import yaml
import pandas as pd

class WorkflowExecutor:
    def __init__(self, workflow_dir='workflows'):
        self.workflow_dir = workflow_dir
        os.makedirs(self.workflow_dir, exist_ok=True)

    def load_workflow(self, workflow_name):
        """Loads a workflow YAML file from the workflow directory."""
        workflow_path = os.path.join(self.workflow_dir, workflow_name)
        with open(workflow_path, 'r') as file:
            return yaml.safe_load(file)

    def execute_workflow(self, data, workflow):
        """Executes the workflow on the provided data."""
        for step in workflow['steps']:
            operation = step['operation']
            column = step['column']

            if operation == 'multiply':
                multiplier = step['value']
                data[column] = [x * multiplier for x in data[column]]
            elif operation == 'add':
                adder = step['value']
                data[column] = [x + adder for x in data[column]]

        df = pd.DataFrame(data)
        return df
