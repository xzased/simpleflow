import gzip
import os
import re
from cdf.log import logger
from cdf.features.links.helpers.masks import follow_mask

from cdf.core.streams.utils import split_file
from cdf.utils.ids import get_part_id


def split_partition(input_file,
                    dest_dir,
                    first_part_size=4,
                    part_size=2):
    """Split a file in several partitions, according to
    `first_part_size` and `part_size`

    Output partitions are gzipped
    """
    current_part = 0
    output_path = os.path.join(dest_dir,
                               os.path.basename(input_file) + '.{}.gz')
    _in = open(input_file, 'rb')
    _out = gzip.open(output_path.format(current_part), 'w')

    for line in split_file(_in):
        # check the part id
        url_id = int(line[0])
        part = get_part_id(url_id, first_part_size, part_size)

        # a new part file is needed
        if part != current_part:
            # this is safe b/c url_id is ordered
            current_part = part
            _out.close()
            _out = gzip.open(output_path.format(current_part), 'w')

        _out.write('\t'.join(line) + '\n')
    _out.close()


def generate_inlink_file(outlink_file, inlink_file):
    """Reverse `urllinks`"""
    outlink = open(outlink_file, 'r')
    buffer = []

    for src, type, mask, dest, ext in split_file(outlink):
        # TODO correct this
        masks = follow_mask(int(mask))
        is_internal = int(dest) > 0
        # we do not crawl pages that blocked by robots.txt
        if is_internal and 'robots' not in masks:
            buffer.append([dest, type, mask, src])
    outlink.close()

    inlink = open(inlink_file, 'w')
    logger.info('Write inlink file %s' % inlink_file)
    # sorted on dest
    for line in sorted(buffer, key=lambda x: int(x[0])):
        inlink.write('\t'.join(line) + '\n')
    inlink.close()


def list_result_files(dir, regexp, full_path=False):
    return [os.path.join(dir, f) if full_path else f
            for f in os.listdir(dir) if re.match(regexp, f)]