import tkinter as tk
import pyautogui
import ctypes

# Enable click-through for the window
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOPMOST = 0x00000008

def make_click_through(hwnd):
    style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST)

# Create transparent overlay window
root = tk.Tk()
root.attributes("-topmost", True)  # Always on top
root.attributes("-fullscreen", True)  # Fullscreen
root.attributes("-transparentcolor", "black")  # Transparent color

# Make the window click-through
root.update()
hwnd = ctypes.windll.user32.GetForegroundWindow()
make_click_through(hwnd)

# Add a UI element (example: FPS Counter)
label = tk.Label(root, text="Overlay UI", font=("Arial", 20), fg="white", bg="black")
label.place(relx=0.5, rely=0.1, anchor="center")

root.mainloop()
