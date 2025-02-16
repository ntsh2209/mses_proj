from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse
import pandas as pd
import os
from validators import validate_data  # Ensure you have a validators.py for validation logic

app = Flask(__name__)
api = Api(app, version="1.0", title="Data Validation API", description="API for validating data files based on dynamic rules")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ns = api.namespace("validation", description="Data Validation Operations")

# Request parser for JSON input
parser = reqparse.RequestParser()
parser.add_argument("data", type=dict, required=True, location="json", help="JSON object containing file path, sheet name, and validation rules")

@ns.route("/validate")
class ValidateFile(Resource):
    @ns.expect(parser)
    def post(self):
        """Validate the uploaded Excel file based on user-defined rules"""
        args = parser.parse_args()
        data = args["data"]

        file_path = data.get("file_path")
        sheet_name = data.get("sheet_name", None)
        rules = data.get("rules", {})

        if not file_path or not os.path.exists(file_path):
            return {"error": "Invalid file path"}, 400

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name) if sheet_name else pd.read_excel(file_path)
        except Exception as e:
            return {"error": f"Failed to read Excel file: {str(e)}"}, 500

        validation_results = validate_data(df, rules)

        return {"validation_results": validation_results}, 200


@ns.route("/sample-rules")
class SampleRules(Resource):
    def get(self):
        """Return a sample set of validation rules"""
        sample_rules = {
            "null_columns": ["age", "email"],
            "sum_constraints": { 
                "salary": 100000,
                "bonus": 5000
            },
            "multiplication_constraints": [["col1", "col2", 500]],
            "range_constraints": { "age": [18, 60] },
            "unique_constraints": ["id"],
            "regex_constraints": { "email": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$" },
            "data_type_constraints": { "age": "numeric", "name": "string" }
        }
        return {"sample_rules": sample_rules}, 200


if __name__ == "__main__":
    app.run(debug=True)
