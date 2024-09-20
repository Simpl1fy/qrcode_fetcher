# imports
import cv2
import numpy as np
import pyautogui
import time
import tkinter as tk
from flask import Flask, send_file
import threading
from PIL import ImageGrab

# Global Variables
app = Flask(__name__)
current_qr_image = None

# Tkinter window for qr code scanning
def create_translucent_window():
    root = tk.Tk()
    root.title('QR code scanner')

    # Setting the window to be translucent and size of the window
    root.geometry(400, 400)
    root.attributes("-alpha 0.3")
    root.configure(bg="pink")

    root.overrideredirect(True)

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

    return root

