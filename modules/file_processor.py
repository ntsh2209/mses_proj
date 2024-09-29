import os
import pandas as pd

class FileProcessor:
    def __init__(self, upload_dir='uploads'):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file, filename=None):
        """Saves an uploaded file to the upload directory."""
        if not filename:
            filename = file.filename
        filepath = os.path.join(self.upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(file.read())
        return filepath

    def read_file(self, filepath):
        """Reads a CSV or TXT file into a Pandas DataFrame."""
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith('.txt'):
            return pd.read_csv(filepath, delimiter='\t')
        else:
            raise ValueError('Unsupported file format')

    def save_csv(self, df, output_filename):
        """Saves a Pandas DataFrame to a CSV file."""
        output_path = os.path.join(self.upload_dir, output_filename)
        df.to_csv(output_path, index=False)
        return output_path
