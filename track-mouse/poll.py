import pyautogui
import time


log_file = "mouse_coordinates.log"


def log_mouse_coordinates():
    with open(log_file, "w") as file:
        file.write("Timestamp,X,Y\n")
        while True:
            x, y = pyautogui.position()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            content = f"{timestamp},{x},{y}\n"
            print(content)
            file.write(content)
            time.sleep(1)


if __name__ == "__main__":
    try:
        print("Logging mouse coordinates. Press Ctrl+C to stop.")
        log_mouse_coordinates()
    except KeyboardInterrupt:
        print("Logging stopped.")
