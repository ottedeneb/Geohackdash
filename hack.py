from pynput import mouse, keyboard
import time
import json

class MouseClickTracker:
    def __init__(self):
        self.last_click_time = None
        self.press_time = None
        self.listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.data = []
        self.recording = False
    
    def on_click(self, x, y, button, pressed):
        if self.recording and button == mouse.Button.left:
            if pressed:
                self.press_time = time.time()
            elif self.press_time is not None:
                release_time = time.time()
                hold_duration = release_time - self.press_time
                print(f"Tasto sinistro rilasciato dopo {hold_duration:.3f} secondi")
                
                interval = None
                if self.last_click_time is not None:
                    interval = self.press_time - self.last_click_time
                    print(f"Intervallo tra click: {interval:.3f} secondi")
                
                self.last_click_time = release_time
                
                
                click_data = {
                    "hold_duration": hold_duration,
                    "interval": interval
                }
                self.data.append(click_data)
                self.save_to_json()
                
                self.press_time = None
    
    def on_key_press(self, key):
        if key == keyboard.KeyCode.from_char('r'):
            self.recording = not self.recording
            state = "avviata" if self.recording else "fermata"
            print(f"Registrazione {state}.")
    
    def save_to_json(self):
        with open("click_data.json", "w") as f:
            json.dump(self.data, f, indent=4)

    def run(self):
        with self.listener, self.keyboard_listener:
            self.listener.join()
            self.keyboard_listener.join()

if __name__ == "__main__":
    tracker = MouseClickTracker()
    tracker.run()
