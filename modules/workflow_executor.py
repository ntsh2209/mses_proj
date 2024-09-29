import yaml
import pandas as pd

class WorkflowExecutor:
    def __init__(self, workflow_file, data_file):
        self.workflow = self.load_workflow(workflow_file)
        self.data = self.load_data(data_file)

    def load_workflow(self, workflow_file):
        """Loads a workflow YAML file."""
        return yaml.safe_load(workflow_file)

    def load_data(self, data_file):
        """Loads data from a YAML file into a dictionary."""
        return yaml.safe_load(data_file)

    def execute_workflow(self):
        """Executes the workflow steps on the data."""
        for step in self.workflow['steps']:
            operation = step['operation']
            column = step['column']
            
            if operation == 'multiply':
                multiplier = step['value']
                self.data[column] = [x * multiplier for x in self.data[column]]
            elif operation == 'add':
                adder = step['value']
                self.data[column] = [x + adder for x in self.data[column]]
            # Add more operations as needed

        # Convert the processed data to a DataFrame
        df = pd.DataFrame(self.data)
        return df
