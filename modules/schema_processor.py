import os
import yaml

class SchemaProcessor:
    def __init__(self, schema_dir='schemas'):
        self.schema_dir = schema_dir
        os.makedirs(self.schema_dir, exist_ok=True)

    def load_schema(self, schema_name):
        """Loads a schema YAML file from the schema directory."""
        schema_path = os.path.join(self.schema_dir, schema_name)
        with open(schema_path, 'r') as file:
            return yaml.safe_load(file)

    def apply_schema(self, df, schema):
        """Applies the schema to a Pandas DataFrame by renaming columns and applying data types."""
        for col in schema['columns']:
            old_name = col['old_name']
            new_name = col['new_name']
            dtype = col['dtype']

            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
                df[new_name] = df[new_name].astype(dtype)
        return df

    def list_schemas(self):
        """Lists all available schema files."""
        return [file for file in os.listdir(self.schema_dir) if file.endswith('.yaml')]
