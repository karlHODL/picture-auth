import getpass
import hashlib
import os 
from dotenv import load_dotenv
from picture import Picture
from user import User

load_dotenv()

img_num = 0

while True:
    # Collect credentials
    print("Enter credentials. Enter 'q' to exit.")
    npub = input("Enter npub: ")
    if npub == "q":
        break
    nsec = getpass.getpass("Enter nsec: ")
    if nsec == "q":
        break
    new_user = User(npub, nsec)

    # Construct file names and Image object
    file_path = f'example.jpg'
    new_file_path = f'example_metadata_{img_num}.jpg'
    new_img = Picture(new_user.public_key, new_user.private_key, file_path, new_file_path)

    # Add the metadata
    new_img.add_metadata()

    # Extract the metadata
    metadata = new_img.extract_metadata()
    extracted_exif_hash = metadata['exif_hash']
    extracted_xmp_hash = metadata['xmp_hash']

    # Verify extracted data matches the hash of the secret key
    hashed_secret_key = hashlib.sha256(new_user.private_key.encode("utf-8")).hexdigest().encode("utf-8")
    print(f'EXIF hash matches: {hashed_secret_key == extracted_exif_hash}')
    print(f'XMP hash matches: {hashed_secret_key == extracted_xmp_hash}')
    print(f'Extracted XMP hash: {extracted_xmp_hash}')
    print(f'Hash: {hashed_secret_key}')

    # Iterate the image name counter
    img_num += 1