import socket
import struct
import pcapy
import dpkt
from dnslib import DNSRecord


interface = "eth0"
filter = "udp port 53"


def process_dns_packet(packet):
    eth_header_length = 14
    ip_header_length = 20

    eth_header = packet[:eth_header_length]
    ip_header = packet[eth_header_length : eth_header_length + ip_header_length]

    ip_version_and_length = struct.unpack("!B", ip_header[0:1])[0]

    ip_header_length = (ip_version_and_length & 0x0F) * 4

    udp_header = packet[
        eth_header_length + ip_header_length : eth_header_length + ip_header_length + 8
    ]

    dns_payload = packet[eth_header_length + ip_header_length + 8 :]

    dns_record = DNSRecord.parse(dns_payload)

    if dns_record.header.qr == dns_record.header.QR_QUERY:
        print(f"DNS Query: {dns_record.q.qname}")
    elif dns_record.header.qr == dns_record.header.QR_RESPONSE:
        print(f"DNS Response: {dns_record.q.qname} -> {dns_record.a}")


def packet_callback(header, data):
    process_dns_packet(data)


def start_capture(interface, filter):
    cap = pcapy.open_live(interface, 65536, True, 100)
    cap.setfilter(filter)
    print("Starting packet capture on interface:", interface)
    try:
        while True:
            cap.dispatch(1, packet_callback)
    except KeyboardInterrupt:
        print("Capture stopped.")


if __name__ == "__main__":
    start_capture(interface, filter)
