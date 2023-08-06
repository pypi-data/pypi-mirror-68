import unittest

from contextlib import suppress
from pathlib import Path

import d64.scripts.d64_fsck

from d64.block import Block
from d64.d64_image import D64Image

import binary


class TestD64_fsck(unittest.TestCase):

    def setUp(self):
        self.base_path = Path(__file__).parent / 'data' / 'test.d64'
        self.test_path = Path('/tmp/test_bad.d64')
        self.base_bin = binary.load_binary(self.base_path)
        d64.scripts.d64_fsck.QUIET = True
        d64.scripts.d64_fsck.FIX = True
        d64.scripts.d64_fsck.YES = True

    def tearDown(self):
        with suppress(FileNotFoundError):
            self.test_path.unlink()

    def test_clean(self):
        d64.scripts.d64_fsck.FIX = False
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.base_path), 0)

    def test_dos_version(self):
        patch = [{'at': 91557, 'from': b'2', 'to': b'7'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(image.dos_version, ord('2'))
        finally:
            image.close()

    def test_dos_format(self):
        patch = [{'at': 91558, 'from': b'A', 'to': b'C'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(image.dos_type, (ord('A'), ord('A')))
        finally:
            image.close()

    def test_dir_link(self):
        patch = [{'at': 91392, 'from': b'\x12', 'to': b'\x00'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(repr(image.dir_block), '<Block 18:0 (18:1)>')
        finally:
            image.close()

    def test_bam_entry_diff(self):
        patch = [{'at': 91416, 'from': b'\x15', 'to': b'\x16'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(image.bam.get_entry(6), (21, '111111111111111111111000'))
        finally:
            image.close()

    def test_bam_18_00_not_alloc(self):
        patch = [{'at': 91464, 'from': b'\x0el', 'to': b'\x0fm'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(image.bam.get_entry(18), (14, '001101101101111111100000'))
        finally:
            image.close()

    def test_dir_18_01_not_alloc(self):
        patch = [{'at': 91464, 'from': b'\x0el', 'to': b'\x0fn'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(image.bam.get_entry(18), (14, '001101101101111111100000'))
        finally:
            image.close()

    def test_dir_loop(self):
        patch = [{'at': 93185, 'from': b'\n', 'to': b'\x01'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(len([e for e in image.iterdir()]), 24)
        finally:
            image.close()

    def test_dir_bad_link(self):
        patch = [{'at': 93185, 'from': b'\n', 'to': b'\xc7'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(len([e for e in image.iterdir()]), 24)
        finally:
            image.close()

    def test_dir_end_len(self):
        patch = [{'at': 93953, 'from': b'\xff', 'to': b'\x87'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(Block(image, 18, 10).data_size, 0xfe)
        finally:
            image.close()

    def test_ent_bad_type(self):
        patch = [{'at': 92482, 'from': b'\x82', 'to': b'\x87'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertEqual(image.path('SMALL10').entry.file_type, 'PRG')
        finally:
            image.close()

    def test_ent_bad_1st(self):
        patch = [{'at': 92483, 'from': b'\x11', 'to': b'I'}]
        binary.patch(self.base_bin, patch, self.test_path)
        self.assertEqual(d64.scripts.d64_fsck.check_image(self.test_path), 0)
        image = D64Image(self.test_path)
        try:
            image.open('rb')
            self.assertFalse(image.path('SMALL10').exists())
        finally:
            image.close()
