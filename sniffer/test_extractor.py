import unittest

import extractor as ext
from packet import Packet

class MainTest(unittest.TestCase):
    def test_pkt_eq_pkt(self):
        self.assertEqual(Packet('1.1.1.1', '2.2.2.2', 0), Packet('1.1.1.1', '2.2.2.2', 0))

    def test_list_eq_list(self):
        self.assertEqual([Packet('1.1.1.1', '2.2.2.2', 0)], [Packet('1.1.1.1', '2.2.2.2', 0)])

    def test_filter_pkts(self):
        pkt1 = Packet('ip1', 'ip2', 0)
        pkt2 = Packet('ip2', 'ip1', 1)
        self.assertEqual(ext.filter_pkts([pkt1, pkt2], 'ip1'), [pkt1])

    def test_group_by_minute(self):
        pkt1 = Packet('ip1', 'ip2', 0)
        pkt2 = Packet('ip1', 'ip2', 2)
        pkt3 = Packet('ip1', 'ip2', 60)
        pkt4 = Packet('ip1', 'ip2', 185)
        pkts = [pkt1, pkt2, pkt3, pkt4]

        self.assertEqual(ext.group_by_minute(pkts), { 0: [pkt1, pkt2], 1: [pkt3], 3: [pkt4] })

    def test_group_by_addr(self):
        pkt1 = Packet('ip1', 'ip2', 0)
        pkt2 = Packet('ip1', 'ip3', 2)
        pkt3 = Packet('ip1', 'ip3', 4)
        pkt4 = Packet('ip1', 'ip2', 6)
        pkts = [pkt1, pkt2, pkt3, pkt4]

        self.assertEqual(ext.group_by_addr(pkts), { 'ip2': [pkt1, pkt4], 'ip3': [pkt2, pkt3] })

    def test_count_by_interval(self):
        pkt1 = Packet('ip1', 'ip2', 0)
        pkt2 = Packet('ip1', 'ip2', 2)
        pkt3 = Packet('ip1', 'ip2', 5)
        pkt4 = Packet('ip1', 'ip2', 6)
        pkt5 = Packet('ip1', 'ip2', 8)
        pkt6 = Packet('ip1', 'ip2', 10)
        pkts = [pkt1, pkt2, pkt3, pkt4, pkt5, pkt6]

        self.assertEqual(ext.count_by_interval(pkts), { 1: 1, 2: 3, 3: 1 })

    def test_extract_mode_from_intervals_finds_interval(self):
        intervals = { 1: 1, 2: 3, 4: 1 }

        self.assertEqual(ext.extract_mode_from_intervals(intervals), 2)

    def test_extract_mode_from_intervals_finds_none(self):
        intervals = { 1: 2, 2: 3, 4: 1 }

        self.assertIsNone(ext.extract_mode_from_intervals(intervals))

    def test_extract_mode_from_intervals_empty(self):
        self.assertIsNone(ext.extract_mode_from_intervals({}))

    def test_extract_addr_mode_empty(self):
        minute = { 'ip1': { 1: 2, 2: 3, 4: 1 },
                   'ip2': {}}

        self.assertIsNone(ext.extract_addr_mode(minute))

    def test_extract_addr_mode_more_than_one(self):
        minute = { 'ip1': { 1: 2, 2: 4, 4: 1 },
                   'ip2': { 5: 10 }}

        self.assertIsNone(ext.extract_addr_mode(minute))

    def test_extract_addr_mode_one(self):
        minute = { 'ip1': { 1: 2, 2: 4, 4: 1 },
                   'ip2': { 5: 10, 6: 8, 7: 8 }}

        self.assertEqual(ext.extract_addr_mode(minute), ('ip1',2))
