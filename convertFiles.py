#!/usr/bin/env python

from __future__ import print_function
import os
import re
import sys

FILES_WITH_FOOTER = "footer.txt"

INPUT_DIR = "brm"
OUTPUT_DIR = "brm2"

TITLE_RE = re.compile(r'\s*<title>(.+)</title>\s*$')
MAIN_PAGE_RE = re.compile(r'\s*<!-- Main Page')
FOOTER_RE =   re.compile(r'\s*<!-- Footer')
NAV_BTNS_RE = re.compile(r'\s*<!-- Nav Buttons')
END_NAV_BTNS_RE = re.compile(r'\s*</div>')

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)


def check_for_nav_buttons(content):
    found = False
    for line in content:
        nav_btns_mat = NAV_BTNS_RE.match(line)
        if nav_btns_mat:
            found = True
            break
    return found

def filter_nav_buttons(content):
    start, end = None, None
    for i, line in enumerate(content):
        nav_btns_mat = NAV_BTNS_RE.match(line)
        if nav_btns_mat:
            start = i
        if start is not None and end is None:
            end_nav_btns_mat = END_NAV_BTNS_RE.match(line)
            if end_nav_btns_mat:
                end = i
                break
    if start is not None and end is not None:
        before = content[0:start]
        after = content[end+1:]
        btwn = content[start:end+1]
        # print(before[-1])
        # print("\n".join(btwn))
        # print(after[0])
        content = before
        content.extend(after)
    return content

def process_input_file(input_file_name):
    output = None
    content = []
    title = None
    found_main_page = False
    found_footer = False
    found_nav_btns = False
    with open(input_file_name, "r") as fh:
        for line in fh:
            title_mat = TITLE_RE.match(line)
            main_page_mat = MAIN_PAGE_RE.match(line)
            footer_mat = FOOTER_RE.match(line)
            if title_mat:
                title = title_mat.group(1)
                print('found title')
            if main_page_mat:
                found_main_page = True
                print('found main page')
            if footer_mat:
                print('found footer')
                found_footer = True
            if found_main_page and not found_footer:
                content.append(line.rstrip())
            
    if title is None or not found_main_page or not found_footer:
        raise Exception(
            "Error: title: %s found_main_page: %s found_footer: %s" %
            (title, found_main_page, found_footer)
        )
    if check_for_nav_buttons(content):
        print('found nav buttons')
        found_nav_btns = True
        content = filter_nav_buttons(content)
    else:
        print('no nav btns')
        # print(content)
    layout = "default.njk" if found_nav_btns else "no_nav_btns.njk"
    output = """---
layout: %s
title: %s
---
%s
    """ % (layout, title, "\n".join(content))
    return output

with open(FILES_WITH_FOOTER, "r") as file_names:
    for tmp in file_names:
        file_name = tmp.strip()
        input_file = os.path.normpath(os.path.join(INPUT_DIR, file_name))
        output_file = os.path.normpath(os.path.join(OUTPUT_DIR, file_name))
        output_path = os.path.dirname(output_file)
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        print(input_file)
        output = process_input_file(input_file)
        with open(output_file, "w") as ofh:
            ofh.write(output)            
        # break
