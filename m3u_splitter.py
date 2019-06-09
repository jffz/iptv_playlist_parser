# -*- coding: utf-8 -*-

import os
import re
import logging

log = logging.getLogger(os.path.basename(__file__))
logging.basicConfig(level="INFO")

"""
A Script to split m3u IPTV files
"""

INFILE = "playlist.m3u"
whitelist = ['fr', 'sport']
blacklist = ['africa']

DELIMITER = "•●"
OUTFILE = os.path.join(os.path.dirname(__file__), "splitted.m3u")


def parse_m3u(file):
    grp_name = 'default'
    categories = {}
    channels = []

    with open(file, 'r', encoding="utf8") as f:
        lines = f.readlines()

    for line in lines:
        if DELIMITER in line:  # Check if the line is a start of a group

            # Add matching channels to categories before flush
            log.info(f"Category found: \"{grp_name}\"")
            categories[grp_name] = channels

            # Retrieve group name
            grp_field = line.split(',')[1]
            grp_rex = re.findall(r"[\w_/ ]*", grp_field)
            grp_name = ''.join(grp_rex).strip().replace(' ', '_').replace('/', '-').lower()
            channels = []  # flush channels list

        channels.append(line)

    # Apply blacklist / whitelist
    wl_passed = {k: v for k, v in categories.items() if any(s in k for s in whitelist)}
    final = {k: v for k, v in wl_passed.items() if all(s not in k for s in blacklist)}

    # Save file
    with open(OUTFILE, 'w+', encoding="utf8") as out:
        out.write(lines[0]) # Add first line to list

        # Write cleaned channels
        for k, v in final.items():
            log.info(f"Saving category: \"{k}\"")
            for channel in v:
                out.write(channel)


if __name__ == "__main__":
    parse_m3u(INFILE)
