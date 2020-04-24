from typing import List,Tuple,Optional
from collections import Counter
import random
from loader import load_icmp_packets
from extractor import get_modes
from lookup import modes_to_nibbles

def main():
    pkts = load_icmp_packets('../pcap_samples/full_sequence.pcap')
    print(f'Loaded {len(pkts)} ICMP packets.')

    # Make a known-correct nibble sequence for later comparison.
    correct_nibbles = modes_to_nibbles(get_modes(pkts, '192.168.1.2'))

    num_trials = 100
    for drop_rate in [0, 0.02, 0.05, 0.1, 0.2]:

        losses = []
        for _ in range(num_trials):
            remaining_pkts = drop(pkts, drop_rate)

            modes: List[Optional[Tuple[str,int]]]
            modes = get_modes(remaining_pkts, '192.168.1.2')

            nibbles = modes_to_nibbles(modes)

            losses.append(nibbles.count(None))

            # Did we extract different values?
            assert len(correct_nibbles) == len(nibbles)
            num_mismatch = sum(nib != correct for (nib,correct) in zip(nibbles, correct_nibbles) if nib is not None)
            assert num_mismatch == 0

        print(f'Drop rate: {drop_rate}')
        print(f'    Average loss: {sum(losses)/len(losses)} of {len(modes)} nibbles')
        print(f'    {Counter(losses)}')

def drop(lst, drop_rate):
    """
    Simulates a poor network connection by randomly dropping
    a percent of packets from lst.

    0 <= drop_rate <= 1
    """
    drop_count = round(len(lst)*drop_rate)
    drop_indices = random.sample(range(len(lst)), drop_count)
    return [x for (i,x) in enumerate(lst) if i not in drop_indices]

if __name__ == '__main__':
    main()
