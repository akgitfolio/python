from scapy.all import sniff, get_if_list, IP, TCP, UDP, Ether, Raw
import psutil
import re
import binascii
import struct
import codecs


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


def inspect_payload(payload):

    patterns = [b"\x90\x90\x90\x90", b"GET /malicious", b"bad_signature"]

    for pattern in patterns:
        if re.search(pattern, payload):
            print(f"Malicious pattern detected: {pattern}")
            return True
    return False


def parse_byte_string(byte_string):

    hex_representation = binascii.hexlify(byte_string)
    print(f"Hexadecimal Representation: {hex_representation}")

    try:
        unpacked_data = struct.unpack("4B", byte_string)
        print(f"Unpacked Data: {unpacked_data}")
    except struct.error as e:
        print("Unpacking failed:", e)

    try:
        utf8_decoded = byte_string.decode("utf-8")
        print(f"UTF-8 Decoded: {utf8_decoded}")
    except UnicodeDecodeError as e:
        print("UTF-8 Decoding failed:", e)

    try:
        ascii_decoded = byte_string.decode("ascii")
        print(f"ASCII Decoded: {ascii_decoded}")
    except UnicodeDecodeError as e:
        print("ASCII Decoding failed:", e)

    try:
        codecs_decoded = codecs.decode(byte_string, "utf-8")
        print(f"Codecs Decoded: {codecs_decoded}")
    except UnicodeDecodeError as e:
        print("Codecs Decoding failed:", e)


def packet_handler(packet):
    try:

        if Ether in packet:
            eth_layer = packet[Ether]
            print(
                f"Ethernet Frame: Source MAC: {eth_layer.src}, Destination MAC: {eth_layer.dst}"
            )

        if IP in packet:
            ip_layer = packet[IP]
            print(
                f"IP Packet: Source IP: {ip_layer.src}, Destination IP: {ip_layer.dst}, Protocol: {ip_layer.proto}"
            )

        if TCP in packet:
            tcp_layer = packet[TCP]
            print(
                f"TCP Segment: Source Port: {tcp_layer.sport}, Destination Port: {tcp_layer.dport}"
            )

        if UDP in packet:
            udp_layer = packet[UDP]
            print(
                f"UDP Datagram: Source Port: {udp_layer.sport}, Destination Port: {udp_layer.dport}"
            )

        print(f"Packet Size: {len(packet)} bytes")

        if Raw in packet:
            payload = bytes(packet[Raw].load)
            print(f"Payload: {payload}")
            if inspect_payload(payload):
                print("Malicious activity detected in packet payload!")

            parse_byte_string(payload)

    except AttributeError as e:

        print(f"Error parsing packet: {e}")


def main():
    interfaces = list_network_interfaces()
    if not interfaces:
        print("No network interfaces found.")
    else:
        selected_interface = select_network_interface(interfaces)
        print(f"Selected network interface: {selected_interface}")

        print("Starting packet capture. Press Ctrl+C to stop.")
        try:
            sniff(iface=selected_interface, prn=packet_handler, store=False)
        except KeyboardInterrupt:
            print("Packet capture stopped.")


if __name__ == "__main__":
    main()
