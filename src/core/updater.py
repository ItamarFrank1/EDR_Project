
import requests
import json
import os
from core.api_secrets import API_KEY # from TreatFox

API_URL = "https://threatfox-api.abuse.ch/api/v1/" # site of signatures
CACHE_FILE = "local_cache.json" # for getting the last file when offline

def fetch_signatures():
    try:
        payload = {"query": "get_iocs", "days": 1} # set the query

        headers = { # creating dict of the Auth-key, according to TreatFox's requirments
            "Auth-Key": API_KEY
        }
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10) # requesting signatures from the site when online
        
        response.raise_for_status() # throw error if the status is not 200(for example 500)

        raw_data = response.json() #convert the data to pyhton dictionary
        signatures_data = []

        if raw_data.get("query_status") == "ok":
            for item in raw_data.get("data", []):
                sig = item.get("ioc") # get the actual signature for each item under the key "ioc"
                if sig: # if sig doesn't None or empty
                    signatures_data.append(sig) 

        with open(CACHE_FILE, 'w') as backup_file: # if succeeded, we will save the data to our file
            json.dump(signatures_data, backup_file)
        
        print("[INFO] Successfully fetched real signatures from ThreatFox API.")
        return signatures_data

    except requests.exceptions.RequestException as e:
        print(f"[WARNING] API fetch failed: {e}. Falling back to local cache...")

        if os.path.exists(CACHE_FILE): # check if the backup file exist, before read from it
            with open(CACHE_FILE, 'r') as backup_file:
                signatures_data = json.load(backup_file)
            print("[INFO] Successfully loaded signatures from local cache.")
            return signatures_data
        else:
            print("[ERROR] No internet and no local cache found. EDR is running blind!")
            return []