from werkzeug.wrappers import Request, Response
from modules.schema_processor import SchemaProcessor
import json

class SchemaController:
    def __init__(self):
        self.schema_processor = SchemaProcessor()

    def list_schemas(self, request):
        schemas = self.schema_processor.list_schemas()
        response_data = {'schemas': schemas}
        return Response(json.dumps(response_data), content_type='application/json', status=200)
