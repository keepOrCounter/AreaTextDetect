import pynput

def on_press(key):
    print(key)


with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()