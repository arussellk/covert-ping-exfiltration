from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from loader import load_icmp_packets
from packet import Packet

def main():
    pkts = load_icmp_packets('/Users/russell/Desktop/foo.pcapng')
    print(pkts)

def filter_pkts(pkts: List[Packet], compromised_src: str):
    return list(filter(lambda x: x.src == compromised_src, pkts))

def group_by_minute(pkts: List[Packet]) -> Dict[int,List[Packet]]:
    """
    [pkt1, pkt2, ...] -> { min1: [pkt1, ...], min2: [pkt2, ...] }
    """
    minutes = defaultdict(list)

    for pkt in sorted(pkts, key=lambda x: x.time):
        minute_num = pkt.time//60
        minutes[minute_num].append(pkt)

    return minutes

def group_by_addr(pkts: List[Packet]) -> Dict[str,List[Packet]]:
    """
    [pkt1, pkt2, ...] -> { ip1: [pkt1, ...], ip2: [pkt2, ...] }
    """
    addrs_to_pkts = defaultdict(list)

    for pkt in pkts:
        addrs_to_pkts[pkt.dest].append(pkt)

    return addrs_to_pkts

def group_by_interval(pkts: List[Packet]) -> Dict[int,int]:
    """
    [pkt1, pkt2, ...] -> { interval: count }
    """
    pass

def extract_addr_mode(minute: Dict[str,Dict[int,int]]) -> Optional[Tuple[str,int]]:
    """
    { ip: { interval: count } } -> (ip,interval) or None
    """
    pass

if __name__ == '__main__':
    main()
