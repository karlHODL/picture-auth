from datetime import datetime
from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import logging
import os
from picture import Picture
from user import User

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

camera = cv2.VideoCapture(0)  # Use default camera

def gen_frames():
    while True:
        try:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f'Error in frame generation: {e}')
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        success, frame = camera.read()
        if success:
            cv2.imwrite('example.jpg', frame)
            npub = request.form['npub']
            nsec = request.form['nsec']
            new_user = User(npub, nsec)

            # Create the filename and path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'{timestamp}_{npub}.jpg'
            filepath = os.path.join('captures', filename)

            # Make sure the directory exists
            os.makedirs('captures', exist_ok=True)

            cv2.imwrite(filepath, frame)

            new_img = Picture(new_user.public_key, new_user.private_key, filepath, filepath)
            new_img.add_metadata()
            metadata = new_img.extract_metadata()
            
            # Format the metadata for display
            formatted_metadata = {
                'EXIF Hash': bytes.fromhex(metadata['exif_hash'].decode('ascii')).hex() if metadata['exif_hash'] else 'Not available',
                'XMP Hash': bytes.fromhex(metadata['xmp_hash'].decode('ascii')).hex() if metadata['xmp_hash'] else 'Not available'
            }
            
            return jsonify({
                'message': 'Image captured and processed successfully',
                'filepath': filepath,
                'metadata': formatted_metadata
            })
        else:
            return jsonify({'error': 'Failed to capture image'}), 400
    except Exception as e:
        app.logger.error(f"Error in capture: {e}", exc_info=True)
        return jsonify({'error': 'An error occurred while processing the image'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error
    app.logger.error(f"Unhandled exception: {e}", exc_info=True)
    # Return a custom error page
    return "An unexpected error occurred", 500

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')