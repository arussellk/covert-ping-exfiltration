from typing import List,Tuple,Optional
from loader import load_icmp_packets
from extractor import get_modes
from lookup import modes_to_nibbles

def main():
    pkts = load_icmp_packets('../pcap_samples/ICMP_test1.pcap')
    print(pkts)

    modes: List[Optional[Tuple[str,int]]]
    modes = get_modes(pkts, '192.168.1.2')
    print(modes)

    nibbles = modes_to_nibbles(modes)
    print(nibbles)

if __name__ == '__main__':
    main()
