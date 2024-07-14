import hashlib
import os 
from dotenv import load_dotenv
from PIL import Image
from PIL.ExifTags import TAGS

load_dotenv()


def add_metadata(input_path, output_path, public_key):
    """
    Add metadata to an image file and save the file

    Parameters:
    input_path (string) - path to the image file
    output_path (string) - path to write the output file
    public_key (string) - public key to embed into file
    """
    private_key = os.getenv("SECRET_KEY")
    encoded_private_key = encode_key(private_key)
    hashed_private_key = hash_metadata(encoded_private_key)
    print(type(hashed_private_key))

    # Open the image file
    img = Image.open(input_path)

    # Create exif data
    exif_data = img.getexif() if img.getexif() else Image.Exif()

    exif_data[35700] = public_key
    exif_data[35701] = hashed_private_key.encode("utf-8")

    # Add the exif data to the image
    img.save(output_path, exif=exif_data)


def encode_key(key):
    encoded_key = key.encode("utf-8")
    return encoded_key

def hash_metadata(metadata):
    hashed_data = hashlib.sha256(metadata).hexdigest()
    return hashed_data

def extract_metadata(file):
    """
    Extract the added metadata to read it back
    """
    img = Image.open(file)
    exif = img.getexif()

    if exif:
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            print(f"{tag}: {value}")

public_key = "npub1234"

print()
file_path = "example.jpg"
add_metadata(file_path, "example_metadata.jpg", public_key)
extract_metadata("example_metadata.jpg")

secret_key = os.getenv("SECRET_KEY")
hashed_secret_key = hashlib.sha256(secret_key.encode("utf-8")).hexdigest().encode("utf-8")
print(type(hashed_secret_key))
print(f'Verification hash: {hashed_secret_key}')