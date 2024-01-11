import dpkt
import socket
import pcapy


class TCPStream:
    def __init__(self, src_ip, dst_ip, src_port, dst_port):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.data = b""

    def add_packet(self, packet):
        self.data += packet.data


class TCPStreamAssembler:
    def __init__(self):
        self.streams = {}

    def process_packet(self, eth_frame):
        eth_type = eth_frame.type
        if eth_type == dpkt.ethernet.ETH_TYPE_IP:
            ip_packet = eth_frame.data
            if isinstance(ip_packet.data, dpkt.tcp.TCP):
                tcp_packet = ip_packet.data
                src_ip = socket.inet_ntoa(ip_packet.src)
                dst_ip = socket.inet_ntoa(ip_packet.dst)
                src_port = tcp_packet.sport
                dst_port = tcp_packet.dport
                key = (src_ip, dst_ip, src_port, dst_port)
                if key not in self.streams:
                    self.streams[key] = TCPStream(src_ip, dst_ip, src_port, dst_port)
                self.streams[key].add_packet(tcp_packet)


def packet_callback(header, data):
    eth_frame = dpkt.ethernet.Ethernet(data)
    tcp_assembler.process_packet(eth_frame)


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
    tcp_assembler = TCPStreamAssembler()
    interface = "eth0"
    filter = "tcp"
    start_capture(interface, filter)
