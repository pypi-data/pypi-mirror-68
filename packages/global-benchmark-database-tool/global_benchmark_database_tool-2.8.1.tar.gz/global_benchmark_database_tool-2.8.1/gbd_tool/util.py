# Global Benchmark Database (GBD)
# Copyright (C) 2019 Markus Iser, Luca Springer, Karlsruhe Institute of Technology (KIT)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import bz2
import gzip
import lzma
import io

__all__ = ['eprint', 'read_hashes', 'confirm', 'open_cnf_file']


def open_cnf_file(filename, mode):
    """
    Opens a CNF file (this is badly guarded, by file-extension only)
    """
    if filename.endswith('.cnf.gz'):
        return io.BufferedReader(gzip.open(filename, mode), io.DEFAULT_BUFFER_SIZE * 8)
    elif filename.endswith('.cnf.bz2'):
        return io.BufferedReader(bz2.open(filename, mode), io.DEFAULT_BUFFER_SIZE * 8)
    elif filename.endswith('.cnf.lzma'):
        return io.BufferedReader(lzma.open(filename, mode), io.DEFAULT_BUFFER_SIZE * 8)
    elif filename.endswith('.cnf'):
        return io.BufferedReader(open(filename, mode), io.DEFAULT_BUFFER_SIZE * 8)
    else:
        raise Exception("Unknown File Extension. Use .cnf, .cnf.bz2, .cnf.lzma, or .cnf.gz")


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def read_hashes():
    hashes = set()
    try:
        while True:
            line = sys.stdin.readline()
            if len(line.strip()) == 0:
                return hashes
            hashes.add(line.strip())
    except KeyboardInterrupt:
        return hashes
    return hashes


def confirm(prompt='Confirm', resp=False):
    """
    prompts for yes or no response from the user. Returns True for yes and False for no.
    'resp' should be set to the default value assumed by the caller when user simply types ENTER.
    """
    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False
