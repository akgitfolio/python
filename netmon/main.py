from scapy.all import sniff, Scapy_Exception
import pandas as pd
from datetime import datetime
import logging
import netifaces


logging.basicConfig(
    filename="network_monitor.log",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


packets_list = []


def packet_callback(packet):
    packet_details = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "src_ip": packet[0][1].src if packet.haslayer("IP") else None,
        "dst_ip": packet[0][1].dst if packet.haslayer("IP") else None,
        "src_port": (
            packet[0][2].sport
            if packet.haslayer("IP") and packet[2].haslayer("TCP")
            else None
        ),
        "dst_port": (
            packet[0][2].dport
            if packet.haslayer("IP") and packet[2].haslayer("TCP")
            else None
        ),
        "protocol": packet[0][1].proto if packet.haslayer("IP") else None,
        "length": len(packet),
    }
    packets_list.append(packet_details)
    logging.info(f"Packet captured: {packet_details}")


def start_sniffing(interface):
    try:
        sniff(iface=interface, prn=packet_callback, store=False)
    except Scapy_Exception as e:
        logging.error(f"Failed to bind to interface {interface}: {e}")
        print(f"Failed to bind to interface {interface}: {e}")


def save_log(filename="network_log.csv"):
    df = pd.DataFrame(packets_list)
    df.to_csv(filename, index=False)
    print(f"Log saved to {filename}")
    logging.info(f"Log saved to {filename}")


def list_interfaces():
    interfaces = netifaces.interfaces()
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")
    return interfaces


if __name__ == "__main__":
    try:
        interfaces = list_interfaces()
        choice = int(input("Enter the number of the network interface to monitor: "))
        interface = interfaces[choice]
        print(f"Starting network monitor on {interface}...")
        logging.info(f"Starting network monitor on interface {interface}")
        start_sniffing(interface)
    except KeyboardInterrupt:
        print("Stopping network monitor and saving log...")
        logging.info("Stopping network monitor")
        save_log()
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        logging.error("Invalid input. User did not enter a valid number.")
    except IndexError:
        print("Invalid choice. Please select a number from the list.")
        logging.error("Invalid choice. User selected a number outside the list range.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
