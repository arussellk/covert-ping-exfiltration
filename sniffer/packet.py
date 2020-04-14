from __future__ import annotations

import pyshark
from pyshark.packet.packet_summary import PacketSummary

class Packet:
    def __init__(self, src: str, dest: str, time: int):
        """
        time is in seconds
        """
        self.src = src
        self.dest = dest
        self.time = time

    @staticmethod
    def from_PacketSummary(ps: PacketSummary) -> Packet:
        time = round(float(ps.time))
        return Packet(ps.source, ps.destination, time)

    def __eq__(self, other):
        return (self.src == other.src and
                self.dest == other.dest and
                self.time == other.time)

    def __str__(self):
        return f'Packet(src={self.src},dest={self.dest},time={self.time})'

    def __repr__(self):
        return self.__str__()
