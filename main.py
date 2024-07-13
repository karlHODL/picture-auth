import hashlib
import os 
from dotenv import load_dotenv

load_dotenv()

#establish secret key
#take the hash of that key

public_key = "npub1234"
secret_key = os.getenv("SECRET_KEY")
encoded_secret_key = secret_key.encode("utf-8")
print(encoded_secret_key)
print(type(encoded_secret_key))

hashed_secret_key = hashlib.sha256(encoded_secret_key).hexdigest()
print(hashed_secret_key)