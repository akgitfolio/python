import pyshark
import psutil


def list_network_interfaces():
    interfaces = psutil.net_if_addrs()
    return interfaces


def select_network_interface(interfaces):
    print("Available network interfaces:")
    for i, interface in enumerate(interfaces):
        print(f"{i + 1}. {interface}")

    while True:
        choice = input("Enter the number of the network interface you want to select: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(interfaces):
                return list(interfaces.keys())[choice - 1]
            else:
                print("Invalid input. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def packet_handler(packet):
    try:

        protocol = packet.transport_layer
        src_addr = packet.ip.src
        src_port = packet[protocol].srcport
        dst_addr = packet.ip.dst
        dst_port = packet[protocol].dstport
        print(
            f"Protocol: {protocol}, Source: {src_addr}:{src_port}, Destination: {dst_addr}:{dst_port}"
        )
    except AttributeError:

        pass


def main():
    interfaces = list_network_interfaces()
    if not interfaces:
        print("No network interfaces found.")
    else:
        selected_interface = select_network_interface(interfaces)
        print(f"Selected network interface: {selected_interface}")

        capture = pyshark.LiveCapture(interface=selected_interface)
        print("Starting packet capture. Press Ctrl+C to stop.")
        try:
            capture.apply_on_packets(packet_handler)
        except KeyboardInterrupt:
            print("Packet capture stopped.")


if __name__ == "__main__":
    main()
