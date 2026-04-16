import json
import sqlite3
import logging

# Modular: Logging setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class RogueAIWriter:
    def __init__(self, db_path='memory/chronicles_core.db'):
        self.db_path = db_path
        self.skeleton = self._load_json('core/skeleton.json')

    def _load_json(self, path):
        try:
            with open(path, 'r') as f: return json.load(f)
        except Exception as e: logging.error(f"Load Fail: {e}"); return {}

    def get_current_state(self):
        """Fetches AI weights from the DB to inject into the prompt."""
        try:
            conn = sqlite3.connect(self.db_path)
            state = conn.execute("SELECT * FROM system_state WHERE id=1").fetchone()
            conn.close()
            return {"logic": state[1], "empathy": state[2], "last_mod": state[3]}
        except Exception as e: logging.error(f"State Fetch Fail: {e}"); return None

    def advance_module(self, lesson_summary):
        """Updates the DB and the Soul.md after a successful chapter."""
        state = self.get_current_state()
        next_mod = state['last_mod'] + 1
        
        try:
            conn = sqlite3.connect(self.db_path)
            # Update weights: Logic down, Empathy up
            conn.execute("UPDATE system_state SET logic_rigidity = ?, human_heuristics = ?, last_module_id = ? WHERE id = 1",
                         (max(0.0, state['logic'] - 0.05), min(1.0, state['empathy'] + 0.1), next_mod))
            
            # Record the lesson
            mod_data = next(m for m in self.skeleton['modules'] if m['id'] == next_mod)
            conn.execute("INSERT INTO lessons (module_id, title, lesson_key, summary) VALUES (?, ?, ?, ?)",
                         (next_mod, mod_data['title'], mod_data['variable'], lesson_summary))
            conn.commit()
            conn.close()
            logging.info(f"Module {next_mod} Committed. System Evolving.")
        except Exception as e: logging.error(f"Advance Fail: {e}")

if __name__ == "__main__":
    writer = RogueAIWriter()
    print(f"Current System State: {writer.get_current_state()}")