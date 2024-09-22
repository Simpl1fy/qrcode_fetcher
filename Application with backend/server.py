from flask import Flask, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", transports=['websocket'])

# CORS(app, origins=['http://localhost:3000']) # This is allow all origin
# CORS(app, origins=["*"]) # More explicit way
# for socket io as well
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET', 'POST'])
def home():
    return "This is flask backend", 200

@app.route('/getimage', methods=['GET'])
def getImage():
    image_path = 'dist/qr_code.png'
    if(os.path.exists(image_path)):
        return send_file(image_path, mimetype='image/png')
    else:
        return 'No image available', 404
    
def monitor_image():
    print("Starting image monitor")
    last_modified_time = None
    image_path = 'dist/qr_code.png'
    while True:
        try:
            if os.path.exists(image_path):
                modified_time = os.path.getmtime(image_path)
                if last_modified_time is None or modified_time > last_modified_time:
                    last_modified_time = modified_time
                    socketio.emit('qr_code_updated', {'message': 'QR code updated'})
            socketio.sleep(1)
        except Exception as e:
            print(f"Error in monitor_image: {e}")
    

if __name__ == "__main__":
    print("Running flask server in port 5000")
    socketio.start_background_task(monitor_image)
    socketio.run(app, port=5000, debug=True)