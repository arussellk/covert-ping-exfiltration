from typing import List,Tuple,Optional
import random
from loader import load_icmp_packets
from extractor import get_modes
from lookup import modes_to_nibbles

num_trials = 100

def main():
    pkts = load_icmp_packets('../pcap_samples/full_sequence.pcap')
    print(f'Loaded {len(pkts)} ICMP packets.')

    for drop_rate in [0, 0.1, 0.2, 0.3, 0.4, 0.5]:

        losses = []
        for _ in range(num_trials):
            remaining_pkts = drop(pkts, drop_rate)

            modes: List[Optional[Tuple[str,int]]]
            modes = get_modes(remaining_pkts, '192.168.1.2')
            #print(f'Extracted {len(modes)} modes.')
            #print(modes)

            nibbles = modes_to_nibbles(modes)
            #print(f'Mapped to nibbles.')
            #print(nibbles)

            losses.append(nibbles.count(None))

            # Did we extract different values?

        print(f'Drop rate: {drop_rate}')
        print(f'Average loss: {sum(losses)/len(losses)} of {len(modes)} pkts')

def drop(lst, drop_rate):
    """
    Simulates a poor network connection by randomly dropping
    a number of packets from lst.

    0 <= drop_rate <= 1
    """
    drop_count = round(len(lst)*drop_rate)
    drop_indices = random.sample(range(len(lst)), drop_count)
    return [x for (i,x) in enumerate(lst) if i not in drop_indices]

if __name__ == '__main__':
    main()
