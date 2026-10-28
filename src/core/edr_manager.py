import os
import hashlib
from core.signature_db import SignatureDatabase
from core.updater import fetch_signatures
from scanner.file_scanner import calculate_sha256

class EDRManager:
    def __init__(self):
        self.db = SignatureDatabase() # creating the set


    def setup_demo_environment(self):
        demo_file = "dummy_malware.txt"
        with open(demo_file, "w", encoding="utf-8") as f:
            f.write("EDR_TEST")

    def start(self):
        print("[INFO] Starting EDR Engine...")
        
        signatures_list = fetch_signatures()

        for sig in signatures_list:
            self.db.add_signature(sig)

        self.setup_demo_environment() # hash that exist the demo file as malware - כאן נעצרתי. לא לשכוח לעדכן בגיטהאב! 
        demo_hash = hashlib.sha256(b"EDR_TEST").hexdigest() 
        self.db.add_signature(demo_hash)

        print(f"[INFO] Loaded {len(signatures_list) + 1}  signatures into memory.")
        
        files_to_scan = ["local_cache.json", "dummy_malware.txt"]


        print("\n--- Running Dual Scan Demo ---")
        for file_path in files_to_scan:
            print(f"\n[INFO] Scanning: {file_path}")
            file_hash = calculate_sha256(file_path)
            
            if file_hash:
                print(f"[INFO] Hash: {file_hash}")
                
                if file_hash in self.db.signatures: 
                    print("[ALERT] MALWARE DETECTED! File matches known threat.")
                else:
                    print("[INFO] File is clean. No threats found.")

if __name__ == "__main__":
    manager = EDRManager()
    manager.start()