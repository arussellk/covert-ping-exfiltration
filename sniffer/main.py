from loader import load_icmp_packets
from extractor import get_modes

def main():
    pkts = load_icmp_packets('../pcap_samples/ICMP_test1.pcap')
    print(pkts)

    modes = get_modes(pkts, '192.168.1.2')
    print(modes)

if __name__ == '__main__':
    main()
