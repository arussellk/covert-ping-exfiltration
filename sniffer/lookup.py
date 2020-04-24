from collections import defaultdict
from typing import List,Tuple,Optional

def modes_to_nibbles(
        modes: List[Optional[Tuple[str,int]]]) -> List[Optional[bytes]]:
    """
    Note that all bytes are <=15.
    The largest nibble is 0b0000_1111 = 0x0f = 15
    """

    return [mode_to_nibble(m) for m in modes]

def mode_to_nibble(mode: Optional[Tuple[str,int]]) -> Optional[bytes]:
    # Lookup tables should be constructed based on your particular network.
    # Addresses should be legitimate addresses in your network.
    # The frequencies should be coprime.
    # The frequencies should fit within your chosen time slice.
    lookup = defaultdict(lambda: None, {
        ('192.168.1.3',  3): b'\x00',
        ('192.168.1.3',  4): b'\x01',
        ('192.168.1.3',  5): b'\x02',
        ('192.168.1.3',  7): b'\x03',

        ('192.168.1.4',  3): b'\x04',
        ('192.168.1.4',  4): b'\x05',
        ('192.168.1.4',  5): b'\x06',
        ('192.168.1.4',  7): b'\x07',

        ('192.168.1.5',  3): b'\x08',
        ('192.168.1.5',  4): b'\x09',
        ('192.168.1.5',  5): b'\x0a',
        ('192.168.1.5',  7): b'\x0b',

        ('192.168.1.10', 3): b'\x0c',
        ('192.168.1.10', 4): b'\x0d',
        ('192.168.1.10', 5): b'\x0e',
        ('192.168.1.10', 7): b'\x0f',
    })

    return lookup[mode]
