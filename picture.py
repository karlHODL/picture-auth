"""A class that can represent a jpeg picture."""
from PIL import Image
from PIL.ExifTags import TAGS
from utils import encode_key, hash_metadata

class Picture:
    """A representation of a picture"""
    
    def __init__(self, pub_key, private_key, img_path, new_img_path):
        """Initialize attributes of the image."""
        self.pub_key = pub_key
        self.private_key = private_key
        self.img_path = img_path
        self.new_img_path = new_img_path

    def add_metadata(self):
        """
        Add metadata to an image file and save the file

        Parameters:
        public_key (string) - public key to embed into image
        private_key (string) - private key to SHA256 hash then embed into image
        input_path (string) - path to the image file
        output_path (string) - path to write the output file
        """

        # Encode and SHA256 hash private key
        encoded_private_key = encode_key(self.private_key)
        hashed_private_key = hash_metadata(encoded_private_key)

        # Open the image file
        img = Image.open(self.img_path)

        # Create exif data
        exif_data = img.getexif() if img.getexif() else Image.Exif()

        exif_data[35700] = self.pub_key
        exif_data[35701] = hashed_private_key.encode("utf-8")

        # Add the exif data to the image
        img.save(self.new_img_path, exif=exif_data)

    def extract_metadata(self):
        """
        Extract the added metadata to read it back
        """
        img = Image.open(self.new_img_path)
        exif = img.getexif()
        hash = None

        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag_id == 35701:
                    hash = value
                # print(f"{tag}: {value}")  
        return hash  