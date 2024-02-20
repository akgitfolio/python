from pynput import mouse, keyboard
import time
import logging


log_file = "mouse_keyboard_events.log"
logging.basicConfig(
    filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s"
)


def on_move(x, y):
    logging.info(f"Pointer moved to ({x}, {y})")
    print(f"Pointer moved to ({x}, {y})")


def on_click(x, y, button, pressed):
    if pressed:
        logging.info(f"Mouse clicked at ({x}, {y}) with {button}")
        print(f"Mouse clicked at ({x}, {y}) with {button}")
    else:
        logging.info(f"Mouse released at ({x}, {y}) with {button}")
        print(f"Mouse released at ({x}, {y}) with {button}")

    if not pressed and button == mouse.Button.right:
        return False


def on_scroll(x, y, dx, dy):
    logging.info(f"Scrolled {'down' if dy < 0 else 'up'} at ({x}, {y})")
    print(f"Scrolled {'down' if dy < 0 else 'up'} at ({x}, {y})")


def on_press(key):
    try:
        logging.info(f"Key pressed: {key.char}")
        print(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key pressed: {key}")
        print(f"Special key pressed: {key}")


def on_release(key):
    logging.info(f"Key released: {key}")
    print(f"Key released: {key}")

    if key == keyboard.Key.esc:
        return False


mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)


mouse_listener.start()
keyboard_listener.start()

print("Listening to mouse and keyboard events. Press 'esc' key to stop.")


mouse_listener.join()
keyboard_listener.join()

print("Logging stopped.")
