import argparse
import sys

from collections import defaultdict
from pathlib import Path

from d64.d64_image import D64Image
from d64.block import Block
from d64.side_sector import SideSector


IMAGE = None
FIX = False
YES = False
VERBOSE = False
QUIET = False

USED_BLOCKS = defaultdict(set)


class CheckAborted(KeyboardInterrupt):
    pass


def remember_used(track, sector):
    """Note block usage for later reconciliation."""
    global USED_BLOCKS

    USED_BLOCKS[track].add(sector)


def fix_error(text, fixer=None, **kwargs):
    """Report, and optionally repair, an error."""
    print("ERROR: "+text)
    if FIX and fixer:
        if YES:
            return fixer(**kwargs)
        response = input("Fix? ")
        if response.lower() in ('q', 'quit'):
            raise CheckAborted
        if response.lower() in ('y', 'yes'):
            return fixer(**kwargs)
    return 1


def check_misc():
    """Check various DOS fields and report disk name & id."""
    errors = 0

    if not QUIET:
        print("\nChecking DOS information...")
    if IMAGE.dos_version != ord('2'):
        msg = "Unknown DOS version, "+chr(IMAGE.dos_version)
        errors += fix_error(msg, fix_dos_version)
    elif VERBOSE:
        print("DOS version: "+chr(IMAGE.dos_version))

    if IMAGE.dos_type[0] != IMAGE.dos_type[1]:
        msg = "Mismatch in DOS formats, ${:02x} & ${:02x}".format(IMAGE.dos_type[0], IMAGE.dos_type[1])
        errors += fix_error(msg, fix_dos_types)
    elif VERBOSE:
        print("DOS formats match, ${:02x} & ${:02x}".format(IMAGE.dos_type[0], IMAGE.dos_type[1]))

    block = Block(IMAGE, IMAGE.DIR_TRACK, 0)
    bad_link = True
    if not block.is_final:
        try:
            next = block.next_block()
            if next.track == IMAGE.DIR_TRACK and next.sector == 1:
                bad_link = False
        except ValueError:
            # invalid track/sector
            pass
    if bad_link:
        ts = block.get(0, 2)
        msg = "Invalid link to directory block, {:d}:{:d}".format(*ts)
        errors += fix_error(msg, fix_dir_link)
    elif VERBOSE:
        print("Link to directory block OK, {!s}".format(next))

    if not QUIET:
        print("Disk name: {}   Disk id: {}".format(IMAGE.name.decode(), IMAGE.id.decode()))
    if errors == 0 and not QUIET:
        print("OK")

    return errors


def check_bam():
    """Check Block Availability Map."""
    errors = 0

    if not QUIET:
        print("\nChecking Block Availability Map...")
    for track in range(1, IMAGE.MAX_TRACK+1):
        total, bits = IMAGE.bam.get_entry(track)
        counted = bits.count('1')
        if total != counted:
            msg = "Mismatch in track {:d} total and bits, {:d} & {:d} ({})".format(track, total, counted, bits)
            errors += fix_error(msg, fix_bam_entry, track=track)
        if VERBOSE:
            print("Track: {:2d}   Free blocks: {:2d}   Free bits: {}".format(track, total, bits))

    if not IMAGE.bam.is_allocated(IMAGE.DIR_TRACK, 0):
        msg = "Track {}:0 not allocated".format(IMAGE.DIR_TRACK)
        errors += fix_error(msg, fix_unalloc_block, block=Block(IMAGE, IMAGE.DIR_TRACK, 0))
    elif VERBOSE:
        print("Block {}:0 allocated".format(IMAGE.DIR_TRACK))
    remember_used(IMAGE.DIR_TRACK, 0)

    if errors == 0 and not QUIET:
        print("OK")

    return errors


def check_dir_links():
    """Check the chain of blocks in the directory."""
    errors = 0
    block = Block(IMAGE, D64Image.DIR_TRACK, 1)

    while True:
        if not IMAGE.bam.is_allocated(block.track, block.sector):
            msg = "Block {!s} not allocated".format(block)
            errors += fix_error(msg, fix_unalloc_block, block=block)
        elif VERBOSE:
            print("Block {!s} allocated".format(block))
        remember_used(block.track, block.sector)
        if block.is_final:
            if block.data_size != 0xfe:
                msg = "Block {!s} has invalid data size, {:d}".format(block, block.data_size)
                errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
            elif VERBOSE:
                print("Block {!s} checked".format(block))
            # end of chain
            break
        if VERBOSE:
            print("Block {!s} checked".format(block))
        try:
            next_block = block.next_block()
            if next_block.sector in USED_BLOCKS[next_block.track]:
                msg = "Block {!s} links to previous directory block {!s}".format(block, next_block)
                # truncate directory chain
                errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
                break
            block = next_block
        except ValueError:
            ts = block.get(0, 2)
            msg = "Block {!s} has invalid link, {:d}:{:d}".format(block, *ts)
            # truncate directory chain
            errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
            break

    return errors


def check_directory():
    """Check directory integrity."""

    if not QUIET:
        print("\nChecking directory...")
    # first check the integrity of the linked directory blocks
    errors = check_dir_links()

    # next check the basic integrity of each directory entry
    entry = 1
    for path in IMAGE.iterdir():
        raw_ftype = path.entry._file_type()
        if raw_ftype & 7 > 4:
            msg = "Entry {:2d}, invalid file type, ${:02x}".format(entry, raw_ftype)
            errors += fix_error(msg, fix_ftype, entry=path.entry, ftype='PRG')
        elif VERBOSE:
            print("Entry {:2d} has valid file type, ${:02x} ({})".format(entry, raw_ftype, path.entry.file_type))

        try:
            first_block = path.entry.first_block()
            if VERBOSE:
                print("Entry {:2d}, link to first block OK, {!s}".format(entry, first_block))
        except ValueError:
            # invalid track/sector
            ts = path.entry.start_ts
            msg = "Entry {:2d}, invalid link to first data block, {:d}:{:d}".format(entry, *ts)
            # missing file contents, delete the entry
            errors += fix_error(msg, fix_ftype, entry=path.entry, ftype=0)

        ss_track, ss_sector = path.entry.side_sector_ts
        if path.entry.file_type == 'REL':
            if path.entry.record_len == 0:
                msg = "Entry {:2d}, invalid relative file record length, {:d}".format(entry, path.entry.record_len)
                # missing relative file info, delete the entry
                errors += fix_error(msg, fix_ftype, entry=path.entry, ftype=0)
            elif VERBOSE:
                print("Entry {:2d}, relative record length {:d}".format(entry, path.entry.record_len))
        elif path.entry.record_len or ss_track or ss_sector:
            msg = "Entry {:2d}, spurious relative file data, {:d}:{:d} {:d}".format(entry, ss_track, ss_sector, path.entry.record_len)
            errors += fix_error(msg, fix_rel_data, entry=path.entry)
        entry += 1

    if errors == 0 and not QUIET:
        print("OK")

    return errors


def check_side_sectors(path):
    """Check the integrity of side sectors of a relative file."""
    errors = 0
    sector_count = 0
    all_ss_ts = []

    # first check the integrity of the linked side sectors
    try:
        side_sector = SideSector(IMAGE, *path.entry.side_sector_ts)
    except ValueError:
        ss_track, ss_sector = path.entry.side_sector_ts
        msg = "File {!s}, invalid link to side sector, {:d}:{:d}".format(path, ss_track, ss_sector)
        errors += fix_error(msg, fix_rebuild_ss_chain, entry=path.entry)

    while side_sector:
        remember_used(side_sector.track, side_sector.sector)
        if side_sector.number != sector_count:
            msg = "Side sector {:2d}, mismatch in index, {:d}".format(sector_count, side_sector.number)
            errors += fix_error(msg, fix_ss_number, side_sector=side_sector, number=sector_count)
        elif VERBOSE:
            print("File {!s}, link to side sector OK, {!s}".format(path, side_sector))
        if side_sector.record_len != path.entry.record_len:
            msg = "Side sector {:2d}, mismatch in record length, {:d} & {:d} (directory)".format(sector_count, side_sector.record_len, path.entry.record_len)
            errors += fix_error(msg, fix_ss_rec_len, side_sector=side_sector, record_len=path.entry.record_len)
        elif VERBOSE:
            print("File {!s}, side sector record length matches directory".format(path))
        try:
            next_ss = side_sector.next_block()
        except ValueError:
            # invalid track/sector
            ts = side_sector.get(0, 2)
            msg = "Side sector {:2d}, invalid link to side sector, {:d}:{:d}".format(sector_count, *ts)
            errors += fix_error(msg, fix_rebuild_ss_chain, entry=path.entry)
            break
        if (side_sector.track, side_sector.sector) in all_ss_ts:
            msg = "Side sector {:2d}, links to previous side sector {!s}".format(sector_count, next_ss)
            errors += fix_error(msg, fix_rebuild_ss_chain, entry=path.entry)
            break

        all_ss_ts.append((side_sector.track, side_sector.sector))
        sector_count += 1
        if sector_count == 6:
            # truncate side sector chain
            errors += fix_error("Total side sectors exceeds 6", fix_data_size, block=side_sector, size=0xfe)
            break
        side_sector = next_ss

    # next check the peer side sector links are correct
    side_sector = SideSector(IMAGE, *path.entry.side_sector_ts)

    while side_sector:
        this_ss_ts = [(ss.track, ss.sector) for ss in side_sector.all_side_sectors()]
        if this_ss_ts != all_ss_ts:
            msg = "Side sector {:2d}, mismatch in side sector list, {!s} & {!s} (from links)".format(side_sector.number, this_ss_ts, all_ss_ts)
            print(msg)
            errors += fix_error(msg, fix_ss_list, side_sector=side_sector, ss_list=all_ss_ts)
        side_sector = side_sector.next_block()

    # finally check the data block links are correct

    return errors, sector_count


def check_files():
    """Check integrity of all files."""
    errors = 0

    if not QUIET:
        print("\nChecking files...")
    for path in IMAGE.iterdir():
        if not path.entry.closed:
            msg = "File {!s}, unclosed".format(path)
            errors += fix_error(msg, fix_unclosed, entry=path.entry)

        file_blocks = defaultdict(set)

        # known valid, already checked
        block = path.entry.first_block()
        blocks_used = 0

        while block:
            # whole image block usage
            remember_used(block.track, block.sector)
            blocks_used += 1
            if VERBOSE:
                print("File {!s}, link to block OK, {!s}".format(path, block))
            if not IMAGE.bam.is_allocated(block.track, block.sector):
                msg = "File {!s}, block {!s} not allocated".format(path, block)
                errors += fix_error(msg, fix_unalloc_block, block=block)
            elif VERBOSE:
                print("File {!s}, block {!s} allocated".format(path, block))

            try:
                next_block = block.next_block()
            except ValueError:
                # invalid track/sector
                ts = block.get(0, 2)
                msg = "File {!s}, invalid link to block, {:d}:{:d}".format(path, *ts)
                # truncate file
                errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
                break

            if block.sector in file_blocks[block.track]:
                msg = "File {!s}, block {!s} links to previous data block {!s}".format(path, block, next_block)
                # truncate file
                errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
                break
            # this file block usage
            file_blocks[block.track].add(block.sector)
            block = next_block

        if path.entry.file_type == 'REL':
            ss_errors, ss_blocks_used = check_side_sectors(path)
            errors += ss_errors
            blocks_used += ss_blocks_used

        if blocks_used != path.size_blocks:
            msg = "File {!s}, mismatch in blocks used, {:d} & {:d} (actual)".format(path, path.size_blocks, blocks_used)
            errors += fix_error(msg, fix_block_count, entry=path.entry, count=blocks_used)
        elif VERBOSE:
            print("File {!s} uses {:d} blocks".format(path, blocks_used))

    if errors == 0 and not QUIET:
        print("OK")

    return errors


def check_allocation():
    global USED_BLOCKS
    errors = 0

    if not QUIET:
        print("\nChecking block allocation...")
    for track in range(1, IMAGE.MAX_TRACK+1):
        max_sectors = IMAGE.max_sectors(track)
        _, bits = IMAGE.bam.get_entry(track)
        bam_used = {i for i, b in enumerate(bits) if b == '0' and i < max_sectors}
        delta = bam_used-USED_BLOCKS[track]

        if delta:
            delta_s = ', '.join([str(b) for b in delta])
            msg = "Track {:d}, sectors {} marked allocated when unused".format(track, delta_s)
            # generate an updated bitmask for sectors actually used
            fixed_bits = ''.join(['1' if i in delta else b for i, b in enumerate(bits)])
            errors += fix_error(msg, fix_track_alloc, track=track, bits=fixed_bits)
        elif VERBOSE:
            print("Track {:2d} OK".format(track))

    if errors == 0 and not QUIET:
        print("OK")

    return errors


def check_image(image_path):
    """Check the integrity of an image, return the number of uncorrected errors."""
    global IMAGE
    global USED_BLOCKS

    USED_BLOCKS = defaultdict(set)

    IMAGE = D64Image(image_path)
    mode = 'r+b' if FIX else 'rb'
    try:
        IMAGE.open(mode)
        errors = check_misc()
        errors += check_bam()
        errors += check_directory()
        errors += check_files()
        errors += check_allocation()

        if VERBOSE:
            print()
            for line in IMAGE.directory():
                print(line)
    finally:
        IMAGE.close()

    return errors


def fix_dos_version():
    """Fix DOS version field."""
    IMAGE.dos_version = ord('2')
    if VERBOSE:
        print("Setting DOS version to 2")
    return 0


def fix_dos_types():
    """Fix DOS format type fields."""
    IMAGE.dos_type = ((ord('A'), ord('A')))
    if VERBOSE:
        print("Setting DOS formats to 'A'")
    return 0


def fix_dir_link():
    """Fix link to directory block."""
    dir_block = Block(IMAGE, IMAGE.DIR_TRACK, 1)
    block = Block(IMAGE, IMAGE.DIR_TRACK, 0)
    block.set_next_block(dir_block)
    if VERBOSE:
        print("Setting link to {!s}".format(dir_block))
    return 0


def fix_bam_entry(track):
    """Fix track entry in BAM."""
    total, bits = IMAGE.bam.get_entry(track)
    counted = bits.count('1')
    IMAGE.bam.set_entry(track, counted, bits)
    if VERBOSE:
        print("Setting track {:d} to {:d} & {}".format(track, counted, bits))
    return 0


def fix_unalloc_block(block):
    """Allocate an in-use block."""
    IMAGE.bam.set_allocated(block.track, block.sector)
    if VERBOSE:
        print("Allocating block {!s}".format(block))
    return 0


def fix_data_size(block, size):
    """Fix data used in a block."""
    block.data_size = size
    if VERBOSE:
        print("Setting data size of {!s} to {:d}".format(block, size))
    return 0


def fix_ftype(entry, ftype):
    """Fix entry file type."""
    entry.file_type = ftype
    if VERBOSE:
        print("Setting entry file type to "+entry.file_type)
    return 0


def fix_rel_data(entry):
    """Clear relative file fields."""
    entry.side_sector_ts = (0, 0)
    entry.record_len = 0
    if VERBOSE:
        print("Clearing relative file data")
    return 0


def fix_ss_number(side_sector, number):
    """Fix side sector number."""
    side_sector.number = number
    if VERBOSE:
        print("Setting side sector index to {:d}".format(number))
    return 0


def fix_ss_rec_len(side_sector, record_len):
    """Fix side sector record length."""
    side_sector.record_len = record_len
    if VERBOSE:
        print("Setting side sector record length to {:d}".format(record_len))
    return 0


def fix_rebuild_ss_chain(entry):
    # FIXME
    return 1


def fix_ss_list(side_sector, ss_list):
    """Fix list of peer side sectors."""
    side_sector.clear_side_sectors()
    for ss in ss_list:
        side_sector.add_side_sector(ss)
    if VERBOSE:
        print("Setting side sector list to {!s}".format(ss_list))
    return 0


def fix_unclosed(entry):
    """Mark an entry as closed."""
    entry.closed = True
    if VERBOSE:
        print("Setting entry file state as closed")
    return 0


def fix_block_count(entry, count):
    """Fix entry size in blocks."""
    entry.size = count
    if VERBOSE:
        print("Setting block count to {:d}".format(count))
    return 0


def fix_track_alloc(track, bits):
    """Fix BAM entry for a track."""
    IMAGE.bam.set_entry(track, bits.count('1'), bits)
    if VERBOSE:
        print("Setting track {:d} bits to {}".format(track, bits))
    return 0


def main():
    global FIX
    global YES
    global VERBOSE
    global QUIET

    parser = argparse.ArgumentParser(description='Check and fix Commodore disk images.')
    parser.add_argument('image', type=Path, help='image filename')
    parser.add_argument('--fix', '-f', action='store_true', help='Fix errors detected')
    parser.add_argument('--yes', '-y', action='store_true', help='Answer questions with "yes"')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='No output')

    args = parser.parse_args()
    FIX = args.fix
    YES = args.yes
    VERBOSE = args.verbose
    QUIET = args.quiet

    try:
        errors = check_image(args.image)
    except KeyboardInterrupt:
        sys.exit("\nAbort, discarding all changes")

    if errors:
        sys.exit("\n{:d} unfixed errors".format(errors))
