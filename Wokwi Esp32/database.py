import json
import os

class LocalDatabase:
    def __init__(self, filename='local_database.json', max_records=50):
        self.filename = filename
        self.max_records = max_records
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        try:
            os.stat(self.filename)
        except OSError:
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def insert(self, record):
        data = self.read_all()
        data.append(record)
        
        if len(data) > self.max_records:
            data = data[-self.max_records:]
            
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print("DB Write Error:", e)
            return False

    def read_all(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def count(self):
        return len(self.read_all())

    def clear(self):
        with open(self.filename, 'w') as f:
            json.dump([], f)