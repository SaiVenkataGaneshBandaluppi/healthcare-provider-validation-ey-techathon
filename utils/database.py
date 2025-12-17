import sqlite3
import json
from datetime import datetime
from typing import List, Dict

class Database:
    """Simple SQLite database for provider records"""
    
    def __init__(self, db_path: str = "providers.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS providers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                npi TEXT UNIQUE,
                name TEXT,
                phone TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                specialty TEXT,
                validation_status TEXT,
                confidence_score REAL,
                created_at TEXT,
                updated_at TEXT,
                audit_log TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_provider(self, provider_data: Dict) -> bool:
        """Save or update provider record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT OR REPLACE INTO providers 
                (npi, name, phone, address, city, state, zip, specialty, 
                 validation_status, confidence_score, created_at, updated_at, audit_log)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                provider_data.get('npi'),
                provider_data.get('name'),
                provider_data.get('phone'),
                provider_data.get('address'),
                provider_data.get('city'),
                provider_data.get('state'),
                provider_data.get('zip'),
                provider_data.get('specialty'),
                provider_data.get('validation_status', 'pending'),
                provider_data.get('confidence_score', 0.0),
                now,
                now,
                json.dumps(provider_data.get('audit_log', []))
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def get_all_providers(self) -> List[Dict]:
        """Get all provider records"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM providers ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        
        providers = [dict(row) for row in rows]
        conn.close()
        
        return providers