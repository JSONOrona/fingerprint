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
__copyright__ = "Copyright 2015, Viverae, Inc."
__credits__ = "Jason V. Orona"
__license__ =  "MIT License"
__version__ = 1.0
__maintainer__ = "Jason V. Orona"
__email__ = "jason.orona@viverae.com"
__status__ = "Production"

# Backwards compatibility for Python 2.4
try:
    import hashlib
    h = hashlib.md5()
except ImportError:
    import md5
    h = md5.new()

from os.path import normpath, walk, isdir, isfile, dirname, basename, \
        exists as path_exists, join as path_join
import fnmatch

exclude_patterns = [ '*bak*', '*undeployed*', '*ear*' ]

def _exclude(path, exclude_patterns):
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        else:
            return False

def path_checksum(paths):
    """
    path_checksum()

    Recursively calculates a check sum representing the contents of all files
    found with a sequence of file and/or directory paths.

    Returns a string.
    """
    if not hasattr(paths, '__iter__'):
        raise TypeError('sequence or iterable expected not %r!' % type(paths))

    def _update_checksum(checksum, dirname, filenames):
        '''
        _update_checksum()

        A private function that updates the checksum
        valuse with each newly passed file.

        Returns the filename for auditing and logging purposes.
        '''
        for filename in sorted(filenames):
            path = path_join(dirname, filename)

            if _exclude(path, exclude_patterns):
                print "skipping %s" % (path)
                continue
            else:
                pass
                #print "Passed through is_ignore"

            if isfile(path):
                #print path
                fh = file(path)
                while 1:
                    file_buffer = fh.read(4096)
                    if not file_buffer : break
                    checksum.update(file_buffer)
                fh.close()

    checksum = h

    for path in sorted([normpath(f) for f in paths]):
        if path_exists(path):
            if isdir(path):
                #print  "Entered is directory condition"
                walk(path, _update_checksum, checksum)
            elif isfile(path):
                #print "Entered is file condition"
                _update_checksum(checksum, dirname(path), basename(path))
    return checksum.hexdigest()

def main():
    """
    main()

    Main program block.
    """
    paths = [ '/opt/conf/config.properties',
             # '/opt/jboss/jboss7/bundles',
              #'/opt/jboss/jboss7/modules',
              #'/opt/jboss/jboss7/standalone/lib/',
              '/opt/jboss/jboss7/standalone/deployments/',
              #'/etc/init.d', #causes checksum to change
              '/etc/rc'
            ]
    #paths = [ '.' ]
    chksum = path_checksum(paths)
    try:
        #syslog.openlog(logoption=syslog.LOG_PID)
        print "Checksum processing started..."
        #syslog.syslog(syslog.LOG_INFO, 'Checksum processing started...')
        print 'Checksum #: %s' % (chksum)
        #syslog.syslog(syslog.LOG_INFO, 'Checksum #: %s' % (chksum))
    except IOError:
        print chksum
    return

if __name__ == '__main__':
    main()
