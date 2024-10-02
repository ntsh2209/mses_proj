import pandas as pd
import json

def validate_schema(schema_text):
    '''Convert schema from text (JSON) to a dict and validate it'''
    try:
        schema = json.loads(schema_text)
    except ValueError as e:
        return {"error": "Invalid schema format", "details": str(e)}

    return schema

def process_csv_with_schema(csv_file_content, schema_text):
    '''Process the CSV file content against the provided schema'''
    # Parse the schema
    schema = validate_schema(schema_text)
    if "error" in schema:
        return schema

    try:
        # Load CSV content into pandas DataFrame
        from io import StringIO
        csv_data = StringIO(csv_file_content)
        df = pd.read_csv(csv_data)

        # Validate columns based on the schema
        for column, dtype in schema.items():
            if column not in df.columns:
                return {"error": f"Missing column {column} in CSV"}
            if str(df[column].dtype) != dtype:
                return {"error": f"Invalid datatype for column {column}. Expected {dtype}, found {df[column].dtype}"}

        # If validation passes, return the CSV content as JSON
        return {"message": "CSV validated successfully", "data": df.to_dict(orient='records')}

    except Exception as e:
        return {"error": "Failed to process CSV", "details": str(e)}
