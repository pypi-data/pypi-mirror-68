import unittest

from unittest.mock import patch

from d64.side_sector import SideSector

from test.mock_block import MockBlock

SideSector.__bases__ = (MockBlock, )


class TestSideSectorRead(unittest.TestCase):

    def setUp(self):
        self.side = SideSector(None, None, None)

    def test_read_number(self):
        self.side.data[2] = 4
        self.assertEqual(self.side.number, 4)

    def test_read_rec_len(self):
        self.side.data[3] = 190
        self.assertEqual(self.side.record_len, 190)

    def test_read_all_ss(self):
        self.side.data[4:0x10] = b'\x05\x11\x05\x07\x05\x09'+b'\x00'*6
        all_ss = self.side.all_side_sectors()
        self.assertEqual(len(all_ss), 3)
        self.assertEqual(all_ss[1].track, 5)
        self.assertEqual(all_ss[1].sector, 7)

    def test_read_all_data(self):
        self.side.data[0x10:0x100] = b'\x18\x13\x18\x08'+b'\x00'*238
        with patch('d64.side_sector.Block', new=MockBlock):
            all_data = self.side.all_data_blocks()
        self.assertEqual(len(all_data), 2)


class TestSideSectorWrite(unittest.TestCase):

    def setUp(self):
        self.side = SideSector(None, None, None)

    def test_write_number(self):
        self.side.number = 3
        self.assertEqual(self.side.number, 3)
        with self.assertRaises(ValueError):
            self.side.number = 11

    def test_write_rec_len(self):
        self.side.record_len = 125
        self.assertEqual(self.side.record_len, 125)

    def test_write_clear_side_sectors(self):
        self.side.data[4:0x10] = b'\xee\x22' * 6
        self.side.clear_side_sectors()
        self.assertEqual(len(self.side.all_side_sectors()), 0)

    def test_write_clear_data_blocks(self):
        self.side.data[0x10:0x100] = b'\x55\xcc' * 120
        self.side.clear_data_blocks()
        self.assertEqual(len(self.side.all_data_blocks()), 0)

    def test_write_add_side_sector(self):
        self.side.data[4:0x10] = b'\x22\x11' * 3 + bytes(6)
        new_ss = SideSector(None, 5, 11)
        new_ss.number = 3
        self.side.add_side_sector(new_ss)
        self.assertEqual([(ss.track, ss.sector) for ss in self.side.all_side_sectors()], [(34, 17), (34, 17), (34, 17), (5, 11)])
