from scapy.all import *
import matplotlib.pyplot as plt


def analyze_http(pkt):
    print(pkt)
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        payload = pkt[TCP].payload

        if payload:
            payload_str = str(payload)
            if "GET" in payload_str or "POST" in payload_str:

                url = payload_str.split()[1]
                print("HTTP request:", url)


def capture_packets():
    sniff(prn=analyze_http, filter="tcp port 443", store=0)


def main():
    capture_packets()


if __name__ == "__main__":
    main()
