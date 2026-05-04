import sqlite3
import json
from datetime import datetime
import os

class FluxIdeasDB:
    def __init__(self, db_path="radar_library.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Table for completed dossiers
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dossiers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    problem_name TEXT,
                    blueprint_json TEXT,
                    market_score INTEGER,
                    mockup_url TEXT,
                    risk_json TEXT,
                    full_state_json TEXT,
                    created_at TIMESTAMP
                )
            """)
            
            # Robust Migration: Check for missing columns in existing databases
            cursor.execute("PRAGMA table_info(dossiers)")
            existing_columns = [info[1] for info in cursor.fetchall()]
            
            new_columns = [
                ("market_score", "INTEGER"),
                ("mockup_url", "TEXT"),
                ("risk_json", "TEXT"),
                ("full_state_json", "TEXT")
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in existing_columns:
                    cursor.execute(f"ALTER TABLE dossiers ADD COLUMN {col_name} {col_type}")
            
            conn.commit()

    def save_dossier(self, topic, problem_name, blueprint, market_score, mockup_url=None, risk_assessment=None, full_state=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dossiers (topic, problem_name, blueprint_json, market_score, mockup_url, risk_json, full_state_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (topic, problem_name, json.dumps(blueprint), market_score, mockup_url, json.dumps(risk_assessment), json.dumps(full_state), datetime.now().isoformat()))
            conn.commit()

    def get_all_dossiers(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dossiers ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def delete_dossier(self, dossier_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dossiers WHERE id = ?", (dossier_id,))
            conn.commit()
