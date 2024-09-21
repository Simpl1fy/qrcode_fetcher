import cv2
import numpy as np
import time
import tkinter as tk
from flask import Flask, send_file
import threading
from PIL import ImageGrab
import logging
import multiprocessing

# Global Variables
app = Flask(__name__)
current_qr_image = None
qr_image_path = 'qr_code.png'

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Log everything from DEBUG level and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

# Tkinter window for qr code scanning
def create_translucent_window():
    root = tk.Tk()
    root.title('QR code scanner')

    logging.info("Created translucent window for QR scanning")

    # Setting the window to be translucent and size of the window
    root.wm_geometry("800x600+100+100")
    root.attributes("-alpha", 0.3)
    root.configure(bg="pink")

    root.resizable(True, True)

    def start_move(event):
        root.x = event.x
        root.y = event.y

    def stop_move(event):
        root.x = None
        root.y = None

    def on_motion(event):
        if root.x is not None and root.y is not None:
            deltax = event.x - root.x
            deltay = event.y - root.y
            root.geometry(f"+{root.winfo_x() + deltax}+{root.winfo_y() + deltay}")

    root.bind("<Button-1>", start_move)
    root.bind("<B1-Motion>", on_motion)
    root.bind("<ButtonRelease-1>", stop_move)

    return root

# Capture the specific region inside the translucent window
def capture_window_area(root):
    # Get the window's position and size
    x = root.winfo_x()
    y = root.winfo_y()
    w = root.winfo_width()
    h = root.winfo_height()

    logging.debug(f"Capturing window area excluding title bar: (x={x}, y={y}, w={w}, h={h})")

    
    screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def detect_qr_code(frame):
    # Initialize the QR code detector
    detector = cv2.QRCodeDetector()
    # Detect and decode the QR code from the frame
    data, bbox, _ = detector.detectAndDecode(frame)
    if bbox is not None:
        logging.info("QR code detected")

        # get bounding of the qr code
        bbox = np.int32(bbox).reshape(-1, 2)  # Convert to integer
        x_min = min(bbox[:, 0])
        x_max = max(bbox[:, 0])
        y_min = min(bbox[:, 1])
        y_max = max(bbox[:, 1])

        # crop the qr code
        qr_image = frame[y_min:y_max, x_min:x_max]

        return True, qr_image
    else:
        logging.debug("No QR code detected in frame")
    return False, None

def qr_code_monitor(root):
    global current_qr_image
    while True:
        frame = capture_window_area(root)  # Capture the specific window region
        found, qr_image = detect_qr_code(frame)  # Detect QR code
        if found:
            logging.info("QR code detected, making window transparent")
            root.attributes('-alpha', 0)
            time.sleep(0.1)
            frame = capture_window_area(root)
            current_qr_image = qr_image  # Update the latest QR code image
            cv2.imwrite(qr_image_path, qr_image)  # Save the QR image
            logging.info(f"QR code saved to {qr_image_path}")
            root.attributes('-alpha', 0.3)
        else:
            logging.debug("No QR code detected")
        time.sleep(0.5)  # Adjust the interval for continuous capture

@app.route('/')
def show_qr_code():
    if current_qr_image is not None:
        logging.info("Serving the QR code image")
        return send_file(qr_image_path, mimetype='image/png')  # Send the saved QR image
    else:
        logging.warning("No QR code found when requested")
        return "No QR code found!"

def start_flask():
    logging.info("Starting Flask server at http://localhost:5000")
    app.run(host='localhost', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    # Create the translucent window using Tkinter
    root = create_translucent_window()

    # Start the QR code detection in a separate thread
    qr_thread = threading.Thread(target=qr_code_monitor, args=(root,))
    qr_thread.daemon = True
    qr_thread.start()

    # Start the Flask server in a separate thread
    flask_process = multiprocessing.Process(target=start_flask)
    flask_process.daemon = True
    flask_process.start()

    # Start the Tkinter event loop (runs on the main thread)
    root.mainloop()

    flask_process.join()
    qr_thread.join()