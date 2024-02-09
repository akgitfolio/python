import pcapy
import socket
from collections import defaultdict
import matplotlib.pyplot as plt
import time


interface = "eth0"
filter = "ip"


bandwidth_usage = defaultdict(int)


def process_packet(header, data):
    eth_length = 14
    ip_header = data[eth_length : eth_length + 20]
    iph = struct.unpack("!BBHHHBBH4s4s", ip_header)
    version_ihl = iph[0]
    ihl = version_ihl & 0xF
    iph_length = ihl * 4

    src_ip = socket.inet_ntoa(iph[8])
    dst_ip = socket.inet_ntoa(iph[9])

    bandwidth_usage[src_ip] += len(data)
    bandwidth_usage[dst_ip] += len(data)


def packet_callback(header, data):
    process_packet(header, data)


def start_capture(interface, filter):
    cap = pcapy.open_live(interface, 65536, True, 100)
    cap.setfilter(filter)
    print("Starting packet capture on interface:", interface)
    try:
        while True:
            cap.dispatch(1, packet_callback)
    except KeyboardInterrupt:
        print("Capture stopped.")


def plot_bandwidth_usage():
    ips = list(bandwidth_usage.keys())
    usage = list(bandwidth_usage.values())
    plt.bar(ips, usage)
    plt.xlabel("IP Address")
    plt.ylabel("Bandwidth Usage (bytes)")
    plt.title("Bandwidth Usage per IP Address")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    start_capture(interface, filter)
