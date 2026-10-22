from core.signature_db import SignatureDatabase
from core.updater import fetch_signatures

class EDRManager:
    def __init__(self):
        self.db = SignatureDatabase() # creating the set
        
    def start(self):
        print("[INFO] Starting EDR Engine...")
        
        signatures_list = fetch_signatures()
        
        count = 0
        for sig in signatures_list:
            self.db.add_signature(sig)
            count += 1
            
        print(f"[INFO] Loaded {count} signatures into memory.")

if __name__ == "__main__":
    manager = EDRManager()
    manager.start()