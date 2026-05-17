"""
CSV file handler for data persistence
"""
import csv
import os
from typing import List, Dict, Any, Optional
from src.utils.constants import Messages
from src.config.settings import Config

class CSVHandler:
    """Handle CSV file operations"""
    
    @staticmethod
    def ensure_file_exists(filepath: str, headers: List[str]):
        """Create file with headers if it doesn't exist"""
        Config.ensure_data_dir()
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
            return

        # Ensure existing files have the proper header row.
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            first_line = f.readline().strip()

        if not first_line or first_line.split(',') != headers:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                content = f.read()

            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                if content:
                    f.write(content)
    
    @staticmethod
    def read_all(filepath: str) -> List[Dict[str, Any]]:
        """Read all records from CSV"""
        if not os.path.exists(filepath):
            return []
        
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    @staticmethod
    def write_all(filepath: str, data: List[Dict[str, Any]], headers: List[str]):
        """Write all records to CSV"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def append(filepath: str, record: Dict[str, Any], headers: List[str]):
        """Append a single record to CSV"""
        CSVHandler.ensure_file_exists(filepath, headers)
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerow(record)
    
    @staticmethod
    def update(filepath: str, record_id: str, updated_record: Dict[str, Any], id_field: str = 'id') -> bool:
        """Update a record by ID"""
        records = CSVHandler.read_all(filepath)
        found = False
        
        for i, record in enumerate(records):
            if record.get(id_field) == record_id:
                records[i] = updated_record
                found = True
                break
        
        if found and records:
            headers = list(records[0].keys())
            CSVHandler.write_all(filepath, records, headers)
        
        return found
    
    @staticmethod
    def delete(filepath: str, record_id: str, id_field: str = 'id') -> bool:
        """Delete a record by ID"""
        records = CSVHandler.read_all(filepath)
        original_count = len(records)
        
        records = [r for r in records if r.get(id_field) != record_id]
        
        if len(records) < original_count and records:
            headers = list(records[0].keys())
            CSVHandler.write_all(filepath, records, headers)
            return True
        elif len(records) < original_count:
            # All records deleted, recreate with headers
            headers = list(Messages.CSV_BOOKS_HEADERS)
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
            return True
        
        return False
    
    @staticmethod
    def find_by_id(filepath: str, record_id: str, id_field: str = 'id') -> Optional[Dict[str, Any]]:
        """Find a record by ID"""
        records = CSVHandler.read_all(filepath)
        for record in records:
            if record.get(id_field) == record_id:
                return record
        return None