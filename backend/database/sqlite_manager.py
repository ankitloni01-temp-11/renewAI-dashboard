import sqlite3
import json
import os
from datetime import datetime

class AuditDB:
    def __init__(self, db_path="/home/labuser/VSCODE_training/renewai-demo/backend/database/renewai.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    policy_id TEXT,
                    event_id TEXT,
                    step_number INTEGER,
                    agent_name TEXT,
                    action TEXT,
                    verdict TEXT,
                    timestamp TEXT,
                    full_output TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_policy_id ON audit_trail(policy_id)")
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    name TEXT PRIMARY KEY,
                    prompt_type TEXT,
                    content TEXT,
                    version INTEGER,
                    updated_at TEXT
                )
            """)

    def write_entry(self, entry: dict):
        policy_id = entry.get("policy_id")
        event_id = entry.get("event_id")
        step_number = entry.get("step_number")
        agent_name = entry.get("agent_name")
        action = entry.get("action")
        verdict = entry.get("verdict")
        timestamp = entry.get("timestamp") or datetime.now().isoformat()
        full_output = json.dumps(entry.get("full_output", entry))

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO audit_trail 
                (policy_id, event_id, step_number, agent_name, action, verdict, timestamp, full_output)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (policy_id, event_id, step_number, agent_name, action, verdict, timestamp, full_output))

    def get_trail(self, policy_id: str = None):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            if policy_id:
                cursor = conn.execute("SELECT * FROM audit_trail WHERE policy_id = ? ORDER BY timestamp ASC", (policy_id,))
            else:
                cursor = conn.execute("SELECT * FROM audit_trail ORDER BY timestamp ASC")
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                item["full_output"] = json.loads(item["full_output"])
                results.append(item)
            return results

    def get_prompt(self, name: str):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT content FROM prompts WHERE name = ?", (name,))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_all_prompts(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM prompts ORDER BY name ASC")
            return [dict(row) for row in cursor.fetchall()]

    def update_prompt(self, name: str, content: str):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT version FROM prompts WHERE name = ?", (name,))
            row = cursor.fetchone()
            version = (row[0] + 1) if row else 1
            timestamp = datetime.now().isoformat()
            conn.execute("""
                INSERT OR REPLACE INTO prompts (name, prompt_type, content, version, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (name, 'system', content, version, timestamp))
            return version

# Singleton instance
db = AuditDB()

