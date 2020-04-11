import pyshark
from typing import List

from packet import Packet

def load_icmp_packets(pcap_path: str) -> List[Packet]:
    # Summary objects are faster to work with and contain
    # the information we need.
    cap = pyshark.FileCapture(pcap_path,
            display_filter='icmp',
            only_summaries=True)

    cap.load_packets() # Eagerly load all packets so that len works.

    return [Packet.from_PacketSummary(ps) for ps in cap]
