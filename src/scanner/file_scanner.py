import hashlib
import os

def calculate_sha256(file_path):

    if not os.path.isfile(file_path): # checking correctness of path and file 
        print(f"[ERROR] File not found: {file_path}")
        return None

    sha256_hash = hashlib.sha256() # creating object to calculate

    # read content in chunks of 64 KB
    with open(file_path, 'rb') as f: 
        while True:
            chunk = f.read(65536) # reading 64 KB(65536 bits)
            
            if not chunk: # read is finish
                break
                
            sha256_hash.update(chunk) # adding the chunk

    return sha256_hash.hexdigest() # lock the calculate