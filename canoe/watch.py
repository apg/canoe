#!/usr/bin/env python

import os
import sys
import time

from canoe.data import Buffer                  
      
class WatchedFile(object):
    
    def __init__(self, fname, bufn=0):
        self.filename = fname
        self.fd = open(fname, 'r')
        self.st = os.stat(fname)
        self.buf = Buffer(bufn)
        self.ends_nl = False

    def _reopen(self):
        self.fd.close()
        self.fd = open(fname, 'r')

    def _chunk(self, chk, cb=None):
        lines = chk.split('\n')
        l = len(lines)
        if l > 0:
            last_line = None
            for i in xrange(l):
                if i == 0 and not self.ends_nl:
                    last_line = self.buf.alter(lambda x: \
                                                   (x or '') + lines[0])
                elif i == (l - 1):
                    last_line = lines[-1]
                    if last_line.endswith('\n'):
                        self.ends_nl = True
                else:
                    last_line = lines[i]

                self.buf.push(last_line)
                if cb:
                    cb(last_line, self.buf)

    def watch(self, cb=None):
        # TODO fill the buffer with bufn lines
        self.fd.seek(0, 2)

        lastTell = -1

        while True:
            a = self.fd.read()
            if self.filename:
                tell = self.fd.tell()
            else:
                tell += len(a)

            if tell > lastTell:
                self._chunk(a, cb)
                print a,

            lastTell = tell

            if self.filename:
                st = os.stat(self.filename)
                if st.st_dev != self.st.st_dev or \
                        st.st_ino != self.st.st_ino or \
                        st.st_nlink != self.st.st_nlink:
                    self.fd.close()
                    self._reopen()
                    lastTell = -1
                time.sleep(.1)


def start_watch(conf):
    


if __name__ == '__main__':
    def cb(line, buf):
        if line.startswith('root'):
            print '\x1b[1;34m%s\x1b[0;m' % line

    if len(sys.argv) > 1:
        wf = WatchedFile(sys.argv[1])
        wf.watch(cb)
