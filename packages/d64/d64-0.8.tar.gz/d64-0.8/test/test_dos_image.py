import unittest

from unittest.mock import patch, Mock

from d64.dos_image import DOSImage

from test.mock_block import MockBlock


class TestDOSImageRead(unittest.TestCase):

    def setUp(self):
        self.dir_data = b'\x12\x01A\x00\x15\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x15' \
                        b'\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x04\x80\x02\n\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0el\xfb\x07\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01' \
                        b'\x00\x02\x00\x12\xff\xff\x03\x12\xff\xff\x03\x12\xff\xff\x03\x12\xff\xff\x03\x11\xff' \
                        b'\xff\x01\x11\xff\xff\x01\x11\xff\xff\x01\x11\xff\xff\x01\x11\xff\xff\x01GAMES TAPE\xa0' \
                        b'\xa0\xa0\xa0\xa0\xa0\xa0\xa0GT\xa02A\xa0\xa0\xa0\xa0\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.image = DOSImage(None)
        self.image.dir_block = MockBlock()

    def test_read_dos_version(self):
        self.image.dir_block.data = self.dir_data
        self.assertEqual(self.image.dos_version, ord('2'))

    def test_read_name(self):
        self.image.dir_block.data = self.dir_data
        self.assertEqual(self.image.name, b'GAMES TAPE')

    def test_read_id(self):
        self.image.dir_block.data = self.dir_data
        self.assertEqual(self.image.id, b'GT')

    def test_dos_type(self):
        self.image.dir_block.data = self.dir_data
        self.assertEqual(self.image.dos_type, (ord('A'), ord('A')))


class TestDOSImageWrite(unittest.TestCase):

    def setUp(self):
        self.image = DOSImage(None)
        self.image.dir_block = MockBlock()

    def test_write_dos_version(self):
        self.image.dos_version = 0x64
        self.assertEqual(self.image.dos_version, 0x64)

    def test_write_name(self):
        self.image.dir_block.data = bytearray(256)
        self.image.name = b'EXAMPLE'
        self.assertEqual(self.image.name, b'EXAMPLE')
        self.image.name = b'VERY LONG EXAMPLE'
        self.assertEqual(self.image.name, b'VERY LONG EXAMPL')

    def test_write_id(self):
        self.image.dir_block.data = bytearray(256)
        self.image.id = b'EX'
        self.assertEqual(self.image.id, b'EX')
        with self.assertRaises(ValueError):
            self.image.id = b'LONG'

    def test_write_dos_type(self):
        self.image.dir_block.data = bytearray(256)
        self.image.dos_type = (0x77, 0x88)
        self.assertEqual(self.image.dos_type, (0x77, 0x88))
        with self.assertRaises(ValueError):
            self.image.dos_type = b'1'


class MockImage(DOSImage):
    DIR_TRACK = 18
    DIR_INTERLEAVE = 3

    def __init__(self, filename):
        super().__init__(filename)
        self._alloc_first_block_return = None
        self._alloc_next_block_return = None
        self.bam = Mock()
        self.free_called = 0

    def alloc_first_block(self):
        return self._alloc_first_block_return

    def alloc_next_block(self, _, __, ___):
        return self._alloc_next_block_return

    def free_block(self, _):
        self.free_called += 1


class TestDirEntry(unittest.TestCase):
    def setUp(self):
        self.free_dir_entry = bytes(64)
        self.in_use_dir_entry = b'\x00\xff\x82\x0A\x14\x46\x49\x47\x48\x54\x45\x52\x20\x52\x41\x49' \
                                b'\x44\xA0\xA0\xA0\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xE7\x01'

    def test_deleted_entry_exists(self):
        image = MockImage(None)
        image._alloc_first_block_return = MockBlock(image, 31, 6)
        MockBlock.BLOCK_FILL = self.free_dir_entry * 8
        with patch('d64.dos_image.Block', new=MockBlock):
            entry = image.get_free_entry()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.block.track, 18)
        self.assertEqual(entry.block.sector, 1)
        self.assertTrue(entry.is_deleted)
        self.assertEqual(entry.size, 1)
        self.assertEqual(entry.start_ts, (31, 6))

    def test_from_new_block(self):
        image = MockImage(None)
        image._alloc_first_block_return = MockBlock(image, 27, 4)
        MockBlock.BLOCK_FILL = self.in_use_dir_entry * 8
        image._alloc_next_block_return = MockBlock(image, 18, 4)
        with patch('d64.dos_image.Block', new=MockBlock):
            entry = image.get_free_entry()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.block.track, 18)
        self.assertEqual(entry.block.sector, 4)
        self.assertTrue(entry.is_deleted)
        self.assertEqual(entry.size, 1)
        self.assertEqual(entry.start_ts, (27, 4))

    def test_no_free_first(self):
        image = MockImage(None)
        image._alloc_first_block_return = None
        with patch('d64.dos_image.Block', new=MockBlock):
            entry = image.get_free_entry()
        self.assertIsNone(entry)

    def test_no_free_next(self):
        image = MockImage(None)
        MockBlock.BLOCK_FILL = self.in_use_dir_entry * 8
        image._alloc_first_block_return = MockBlock(image, 31, 6)
        image._alloc_next_block_return = None
        with patch('d64.dos_image.Block', new=MockBlock):
            entry = image.get_free_entry()
        self.assertIsNone(entry)
        self.assertEqual(image.free_called, 1)


if __name__ == '__main__':
    unittest.main()
