import socket
import threading
from queue import Queue

target = "127.0.0.1"
num_threads = 50
port_range = (1, 9000)


def scan_ports(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port}: Open")
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")


def worker():
    while True:
        port = port_queue.get()
        scan_ports(port)
        port_queue.task_done()


port_queue = Queue()
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


for port in range(port_range[0], port_range[1] + 1):
    port_queue.put(port)


port_queue.join()
