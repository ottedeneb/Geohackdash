from pynput import keyboard
import time
import json

def load_click_data():
    try:
        with open("click_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Nessun file JSON trovato.")
        return []

def replay_clicks():
    click_data = load_click_data()
    if not click_data:
        return
    
    keyboard_controller = keyboard.Controller()
    stop_replay = False
    
    def on_key_press(key):
        nonlocal stop_replay
        if key == keyboard.KeyCode.from_char('o'):
            stop_replay = True
            return False
    
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    keyboard_listener.start()
    
    print("Riproduzione avviata... (premi 'O' per interrompere)")
    
    for i, click in enumerate(click_data):
        if stop_replay:
            print("Riproduzione interrotta.")
            break
        
        if i > 0:
            time.sleep(click.get("interval", 0))
        
        keyboard_controller.press(keyboard.Key.space)
        time.sleep(click["hold_duration"])
        keyboard_controller.release(keyboard.Key.space)
        print(f"Riprodotto click con durata {click['hold_duration']} secondi")
    
    print("Riproduzione completata.")
    keyboard_listener.stop()

def on_press(key):
    if key == keyboard.KeyCode.from_char('p'):
        replay_clicks()

print("Premi 'P' per avviare la riproduzione dei click registrati. Premi 'O' per interrompere.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
