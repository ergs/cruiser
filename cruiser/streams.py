"""Tools for managing streams"""
import sys
import subprocess
from threading import Thread
from queue import Queue, Empty


class NonBlockingStreamReader(object):

    def __init__(self, stream):
        """A non-blocking stream reader

        Parameters
        ----------
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        """

        self._s = stream
        self._q = Queue()

        def _populate_queue(stream, queue):
            """Collect lines from 'stream' and put them in 'queque'."""
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    break

        self._t = Thread(target=_populate_queue,
                         args=(self._s, self._q))
        self._t.daemon = True
        self._t.start() # start collecting lines from the stream

    def readline(self, timeout=None):
        try:
            return self._q.get(block=timeout is not None,
                               timeout=timeout)
        except Empty:
            return None

    def close(self):
        self._t.join()


def stream_output(cmd, stdout=None, stderr=None, timeout=0.001):
    """Runs a suprocess command and streams the output."""
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    p = subprocess.Popen(cmd, universal_newlines=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         )
    out_sr = NonBlockingStreamReader(p.stdout)
    err_sr = NonBlockingStreamReader(p.stderr)
    while p.poll() is None:
        o = out_sr.readline(timeout)
        if o is not None:
            print(o, file=stdout, end='')
        e = err_sr.readline(timeout)
        if e is not None:
            print(e, file=stderr, end='')
    # drain the queues
    o = out_sr.readline(timeout)
    while o is not None:
        print(o, file=stdout, end='')
        o = out_sr.readline(timeout)
    e = err_sr.readline(timeout)
    while e is not None:
        print(e, file=errout, end='')
        e = err_sr.readline(timeout)
    out_sr.close()
    err_sr.close()
