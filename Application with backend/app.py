import cv2
import numpy as np
import time
import tkinter as tk
from PIL import ImageGrab
import logging
import threading

qr_image_path = 'qr_code.png'  # Filepath where the image is saved

def create_translucent_window():
    root = tk.Tk()
    root.title('QR code scanner')
    root.wm_geometry("300x300+100+100")
    root.attributes("-alpha", 0.3)
    root.configure(bg="pink")
    return root

def capture_window_area(root):
    x = root.winfo_x()
    y = root.winfo_y()
    w = root.winfo_width()
    h = root.winfo_height()

    screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def detect_qr_code(frame):
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(frame)
    if bbox is not None:
        bbox = np.int32(bbox).reshape(-1, 2)
        x_min = min(bbox[:, 0])
        x_max = max(bbox[:, 0])
        y_min = min(bbox[:, 1])
        y_max = max(bbox[:, 1])
        qr_image = frame[y_min:y_max, x_min:x_max]
        return True, qr_image
    return False, None

def qr_code_monitor(root):
    while True:
        frame = capture_window_area(root)
        found, qr_image = detect_qr_code(frame)
        if found:
            logging.info("QR code detected")
            # Convert to black and white
            gray_qr_image = cv2.cvtColor(qr_image, cv2.COLOR_BGR2GRAY)
            _, bw_qr_image = cv2.threshold(gray_qr_image, 127, 255, cv2.THRESH_BINARY)
            cv2.imwrite(qr_image_path, bw_qr_image)  # Save the image as black and white
            logging.info(f"QR code saved to {qr_image_path}")
        time.sleep(2)  # Poll every 2 seconds

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    root = create_translucent_window()
    
    qr_code_monitor_thread = threading.Thread(target=qr_code_monitor, args=(root,))
    qr_code_monitor_thread.daemon = True
    qr_code_monitor_thread.start()
    root.mainloop()
