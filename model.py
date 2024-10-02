from flask_restx import fields

# This is how the schema model for columns would be defined, just for Swagger documentation
schema_model = {
    'column_name': fields.String(description='The name of the column'),
    'data_type': fields.String(description='Expected data type (e.g., int, float, str)')
}
