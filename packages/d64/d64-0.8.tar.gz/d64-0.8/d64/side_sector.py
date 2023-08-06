import struct

from .block import Block


class SideSector(Block):
    """Relative file side sector block."""

    @property
    def number(self):
        """Return this side sector block number (0-5)."""
        return self.get(2)

    @property
    def record_len(self):
        """Return record length."""
        return self.get(3)

    @number.setter
    def number(self, number):
        """Modify side sector block number."""
        if number < 0 or number > 5:
            raise ValueError("Invalid side sector index, %d" % number)
        self.set(2, number)

    @record_len.setter
    def record_len(self, rec_len):
        """Modify side sector record length."""
        self.set(3, rec_len)

    def all_side_sectors(self):
        """Return an array of all side sectors."""
        ss_bin = self.get(4, 0x10)
        return [SideSector(self.image, ss_bin[i], ss_bin[i+1]) for i in range(0, 12, 2) if ss_bin[i]]

    def all_data_blocks(self):
        """Return an array of all data blocks in this side sector."""
        links_bin = self.get(0x10, 0x100)
        return [Block(self.image, links_bin[i], links_bin[i+1]) for i in range(0, 0xf0, 2) if links_bin[i]]

    def clear_side_sectors(self):
        """Zero out all side sector links."""
        self.set(4, bytes(12))

    def clear_data_blocks(self):
        """Zero out all data block links."""
        self.set(0x10, bytes(0xf0))

    def add_side_sector(self, other):
        """Append a new side sector to this side sector's list."""
        self.set(4+other.number*2, struct.pack('<BB', other.track, other.sector))
