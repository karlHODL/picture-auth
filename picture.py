"""A class that can represent a jpeg picture."""
import traceback
from PIL import Image
from PIL.ExifTags import TAGS
from utils import encode_key, hash_metadata
from libxmp import XMPFiles, XMPMeta, XMPError

# Define the namespace URI
NS_CUSTOM = 'http://ns.example.com/custom/1.0/'

# Register the custom namespace with a prefix
XMPMeta.register_namespace(NS_CUSTOM, 'custom')

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
        Add EXIF and XMP metadata to an image file and save the file

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

        # Add xmp metatdata
        xmp_file = XMPFiles(file_path=self.new_img_path, open_forupdate=True)
        xmp = xmp_file.get_xmp()
        if xmp is None:
            xmp = XMPMeta()
        
        try:
            xmp.set_property(NS_CUSTOM, 'public_key', self.pub_key)
            xmp.set_property(NS_CUSTOM, 'hashed_private_key', hashed_private_key.encode('utf-8').hex())
            if xmp_file.can_put_xmp(xmp):
                xmp_file.put_xmp(xmp)
            xmp_file.close_file()
        except XMPError as e:
            print(f'An error occurred while writing XMP Metadata: {str(e)}.')

    def extract_metadata(self):
        """
        Extract the added metadata to read it back
        """
        exif_hash = None
        xmp_hash = None

        # Extract EXIF
        img = Image.open(self.new_img_path)
        exif = img.getexif()

        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag_id == 35701:
                    exif_hash = value
                # print(f"{tag}: {value}")  
        
        # Extract XMP
        xmp_file = XMPFiles(file_path=self.new_img_path)
        xmp = xmp_file.get_xmp()
        if xmp is not None:
            try:
                xmp_hash_hex = xmp.get_property(NS_CUSTOM, 'hashed_private_key')
                if xmp_hash_hex:
                    xmp_hash = bytes.fromhex(xmp_hash_hex)
            except XMPError as e:
                print(f'An error occurred while reading XMP metadata: {str(e)}')
                print(f'Error type: {type(e).__name__}')
                print(f'Error details:')
                traceback.print_exc()
        xmp_file.close_file()
        
        return {
            'exif_hash': exif_hash,
            'xmp_hash': xmp_hash
        }  