import hashlib

def encode_key(key):
    """Encode the private key as bytes so it can be used in hashlib"""
    encoded_key = key.encode("utf-8")
    return encoded_key

def hash_metadata(metadata):
    """SHA256 hash of the private key"""
    hashed_data = hashlib.sha256(metadata).hexdigest()
    return hashed_data