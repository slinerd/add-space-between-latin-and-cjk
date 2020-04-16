#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Add space between CJK and Latin characters according to
# https://open.leancloud.cn/copywriting-style-guide.html. Mainly used for
# cleanning up Markdown documents.
#
# SYNOPSIS
#   add-space-between-latin-and-cjk input_folder
#
# CAUTION
#   files in folder are changed in-place.

import sys,os
import functools

def is_latin(c):
    return ord(c) < 256

# Some characters should not have space on either side.
def allow_space(c):
    return not c.isspace() and not (c in '，。；「」：《》『』、[]（）*_')

def add_space_at_boundry(prefix, next_char):
    if len(prefix) == 0:
        return next_char
    if is_latin(prefix[-1]) != is_latin(next_char) \
        and allow_space(next_char) and allow_space(prefix[-1]):
        return prefix + ' ' + next_char
    else:
        return prefix + next_char

def get_files(dir_path):
    files_path = []
    for entry in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, entry)):
            for f in get_files(os.path.join(dir_path, entry)):
                files_path.append(f)
        else:
            files_path.append(os.path.join(dir_path, entry))
    return files_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: A minimum of one argument is required!\n')
        exit()

    if len(sys.argv) > 2:
        print('Warning: only files in %s will be converted!\n' % sys.argv[1])

    for file in get_files(sys.argv[1]):
        
        if not file.endswith('.md'):
            continue
        print('Converting: %s' % file)
        
        with open(file, 'r') as infile:
            instr = infile.read()

        outstr = functools.reduce(add_space_at_boundry, instr, '')

        with open(file, 'w') as outfile:
            outfile.write(outstr)