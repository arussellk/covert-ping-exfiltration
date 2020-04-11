from loader import load_icmp_packets

def main():
    pkts = load_icmp_packets('/Users/russell/Desktop/foo.pcapng')
    print(pkts)

if __name__ == '__main__':
    main()
