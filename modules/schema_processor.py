import yaml

class SchemaProcessor:
    def __init__(self, schema_file):
        self.schema = self.load_schema(schema_file)

    def load_schema(self, schema_file):
        """Loads a YAML schema file."""
        return yaml.safe_load(schema_file)

    def apply_schema(self, df):
        """Applies the schema to a Pandas DataFrame by renaming columns and applying data types."""
        for col in self.schema['columns']:
            old_name = col['old_name']
            new_name = col['new_name']
            dtype = col['dtype']

            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
                df[new_name] = df[new_name].astype(dtype)
        return df
