import os
import sys
import time
import threading

from collections import defaultdict

from data import Buffer                  
      

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
        # TODO this doesn't work with unix sockets, 
        #  nor does it work with fifos, since seek doesn't work on them
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
    """Given a config object which may define multiple canoes, run
    all of them, however that means.
    """
    def mk_cball(canoes):
        def cb(line, buffer):
            for c in canoes:
                c.send(line, buffer)
        return cb

    things = defaultdict(list)

    for fname, canoes in conf.watching:
        things[fname] += canoes

    for fname, canoes in things.iteritems():
        wf = WatchedFile(fname, 1024) # TODO: buffer length should be configured
        cb = mk_cball(canoes)
        t = threading.Thread(target=wf.watch, args=(cb,))
        t.daemon = True
        t.start()

    while threading.active_count() > 0:
        time.sleep(.1)
