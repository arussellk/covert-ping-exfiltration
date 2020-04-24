from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from packet import Packet

def get_modes(pkts: List[Packet], compromised_src: str) -> List[Optional[Tuple[str,int]]]:
    """
    Process a long sequence of pkts (i.e., the entire transmission)
    to produce a list of the most-likely address/frequency pairs
    that were transmitted on the covert channel.

    [pkt1, pkt2, pkt3, ...] -> [(ip1,3), None, (ip4,5), ...]
    """
    filtered_pkts = filter_pkts(pkts, compromised_src)
    minutes = group_by_minute(filtered_pkts)

    for m in minutes.keys():
        minutes[m] = group_by_addr(minutes[m])
        for addr in minutes[m].keys():
            minutes[m][addr] = count_by_interval(minutes[m][addr])
        minutes[m] = extract_addr_mode(minutes[m])

    return list(minutes.values())

def filter_pkts(pkts: List[Packet], compromised_src: str) -> List[Packet]:
    """Filter pkts to those originating from compromised_src."""
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

def count_by_interval(pkts: List[Packet]) -> Dict[int,int]:
    """
    [pkt1, pkt2, ...] -> { interval: count }

    Examine the pairwise intervals between packets.
    pkt1 pkt2 pkt3 pkt4 pkt5 ...
           |    |    |    |
         pkt1 pkt2 pkt3 pkt4 ...
    """
    intervals = defaultdict(lambda: 0)

    for pkt1,pkt2 in zip(pkts,pkts[1:]):
        interval = pkt2.time - pkt1.time
        intervals[interval] += 1

    return intervals

def extract_addr_mode(minute: Dict[str,Dict[int,int]]) -> Optional[Tuple[str,int]]:
    """
    { ip1: { interval: count },
      ip2: { interval: count } } -> (ip,interval) or None
    """
    ip_to_mode = { ip: extract_mode_from_intervals(intervals) for ip,intervals in minute.items() }
    mode_count = sum(x is not None for x in ip_to_mode.values())
    if mode_count != 1:
        return None

    for ip,mode in ip_to_mode.items():
        if mode is not None:
            return (ip,mode)

def extract_mode_from_intervals(intervals: Dict[int,int]) -> Optional[int]:
    """
    { interval: count } -> interval or None
    """
    # More than half of messages seen should have the same interval.
    threshold = 0.5

    total = sum(intervals.values())
    for interval,count in intervals.items():
        if count/total > threshold:
            return interval

    return None
