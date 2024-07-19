import hashlib
import os 
from dotenv import load_dotenv
from picture import Picture

load_dotenv()

public_key = "npub1234"
private_key = os.getenv("SECRET_KEY")
file_path = "example.jpg"
new_file_path = "example_metadata.jpg"
new_img = Picture(public_key, private_key, file_path, new_file_path)

# Add the metadata
new_img.add_metadata()

# Extract the metadata
metadata = new_img.extract_metadata()
extracted_exif_hash = metadata['exif_hash']
extracted_xmp_hash = metadata['xmp_hash']

# Verify extracted data matches the hash of the secret key
hashed_secret_key = hashlib.sha256(private_key.encode("utf-8")).hexdigest().encode("utf-8")
print(f'EXIF hash matches: {hashed_secret_key == extracted_exif_hash}')
print(f'XMP hash matches: {hashed_secret_key == extracted_xmp_hash}')
print(f'Extracted XMP hash: {extracted_xmp_hash}')
print(f'Hash: {hashed_secret_key}')