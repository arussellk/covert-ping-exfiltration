import pyshark
from typing import List

from packet import Packet

def load_icmp_packets(pcap_path: str) -> List[Packet]:
    # Summary objects are faster to work with and contain
    # the information we need.
    cap = pyshark.FileCapture(pcap_path,
            display_filter='icmp',
            only_summaries=True)

    # Eagerly load all packets so that len(...) and enumeration work.
    cap.load_packets()

    # Assume that the first ICMP packet is time 0.
    offset = float(cap[0].time)

    return [Packet.from_PacketSummary(ps, time_offset=offset) for ps in cap]
