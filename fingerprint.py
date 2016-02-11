#!/usr/bin/env python

"""
fingerprint.py - Creates a sha-1 checksum from any number of directories
                 and files.

The checksum that is generated is based purely on the contents of the the files
found, processed in ascending order using normalised file paths.

This script does not account for file metadata, like ownership, permissions
and stat information. The value of the checksum will change if any changes      occur
to a file or if a new file is added.
"""

__author___ = "Jason V. Orona"
__copyright__ = "Copyright 2015, Jason v. Orona"
__credits__ = "Jason V. Orona"
__license__ =  "MIT License"
__version__ = 1.0
__maintainer__ = "Jason V. Orona"
__email__ = "jasonorona@gmail.com

# Backwards compatibility for Python 2.4
try:
    import hashlib
    h = hashlib.md5()
except ImportError:
    import md5
    h = md5.new()

import os
import fnmatch

def _exclude(path, exclude_patterns):
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        else:
            return False

def _update_checksum(filepath):
    """
    _update_checksum()

    A private function that updates the checksum
    valude after each iteration.
    """
    try:
        f1 = open(filepath, 'rb')
    except IOError:
        print "Unable to open %s" % (filepath)
        f1.close()
    while 1:
        file_buffer = f1.read(4096)
        if not file_buffer : break
        h.update(file_buffer)
    f1.close()

def fingerprint(directory, exclude_patterns, verbose=0):
    """
    fingerprint()

    Recursively calculates a checksum representing the contents of all files
    found in a sequence o file and/or directory paths.
    """
    for d in directory:
        d = os.path.normpath(d)
        if _exclude(d, exclude_patterns):
            continue
        if not os.path.exists(d):
            return -1
        if os.path.isfile(d):
            filepath = d
            if verbose == 1:
                print "Hashing %s" % (filepath)
            _update_checksum(filepath)
        else:
            rootdir = d
            file_list = sorted([f for (root, dirs, files) in os.walk(rootdir) for f in files])
            for name in file_list:
                if verbose == 1:
                    print 'Hashing %s' % (name)
                filepath = os.path.join(rootdir, name)
                _update_checksum(filepath)

    return h.hexdigest()

def main():
    """
    main()

    Main program block.
    """
    # Define directories that will be computed into the checksum
    paths = [ '/etc',
              '/bin',
              '/boot' ]

    # Define regex string patterns that should be excluded from checksum
    exclude_patterns = [ '*.bak*' ]

    # This does all the work
    # For more verbosity make verbose=1
    chksum = fingerprint(paths, exclude_patterns, verbose=0)
    try:
        print "Checksum processing started..."
        print 'Checksum = %s' % (chksum)
    except IOError:
        print chksum
    return

if __name__ == '__main__':
    main()
