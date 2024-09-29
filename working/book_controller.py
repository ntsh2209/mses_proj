from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage  # Import FileStorage for file handling
import csv
import io

# Define the namespace for the books API
books_ns = Namespace('books', description="Operations related to book management")

# Define the book model (for Swagger and internal representation)
book_model = books_ns.model('Book', {
    'id': fields.Integer(description='Book ID'),
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author')
})

# Define input for POST (file upload)
file_parser = books_ns.parser()
file_parser.add_argument('file', type=FileStorage, location='files', required=True, help='CSV file containing book data')  # Correctly using FileStorage type for file uploads

# In-memory storage for books
books = []
book_id_counter = 1  # To generate book IDs automatically


@books_ns.route('/')
class BookList(Resource):
    @books_ns.marshal_list_with(book_model)
    def get(self):
        """Retrieve the list of books"""
        return books

    @books_ns.expect(file_parser)  # Expecting a file input in form-data (multipart/form-data)
    def post(self):
        """
        Upload a CSV file containing books, parse the file, and add the books to the list.
        Each book should have a title and author.
        """
        global book_id_counter
        
        # Parse the incoming request for files
        args = file_parser.parse_args()
        csv_file = args['file']  # Access the uploaded file
        
        if not csv_file:
            return {'message': 'No CSV file provided'}, 400
        
        # Read and parse the CSV file
        csv_content = csv_file.read().decode('utf-8')  # Read and decode the file content
        csv_reader = csv.DictReader(io.StringIO(csv_content))  # Parse the CSV content
        
        # Validate and add books to the list
        new_books = []
        for row in csv_reader:
            title = row.get('title')
            author = row.get('author')

            if title and author:
                # Add the new book to the in-memory list with an auto-incremented ID
                new_book = {
                    'id': book_id_counter,
                    'title': title,
                    'author': author
                }
                books.append(new_book)
                new_books.append(new_book)
                book_id_counter += 1
            else:
                return {'message': f'Missing title or author in row: {row}'}, 400
        
        return {'message': 'Books uploaded successfully', 'books': new_books}, 201
