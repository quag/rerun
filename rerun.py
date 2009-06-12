#!/usr/bin/env python

import os
import sys
import time
import difflib
import signal
import subprocess

class Script:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.process = None

    def start(self):
        self.process = subprocess.Popen(self.path)

    def stop(self):
        if self.process:
            try:
                self.process.terminate()
            except:
                # Fall back for pre-2.6, but only works on Unix platforms
                os.kill(self.process.pid, signal.SIGTERM)
            self.process = None

    def contents(self):
        f = file(self.path)
        lines = f.readlines()
        f.close
        return lines

def _snapshot(name, timestamp):
    return "%s (%s)" % (name, time.asctime(time.localtime(timestamp)))

def rerun(scriptfile):
    try:
        script = Script(scriptfile)
        lastrun = 0
        lastcontents = None

        while True:
            lastmodified = os.stat(scriptfile).st_mtime

            if lastmodified > lastrun:
                script.stop()
                contents = script.contents()

                if lastcontents:
                    print
                    print "".join(difflib.unified_diff(lastcontents, contents, fromfile=_snapshot(scriptfile, lastrun), tofile=_snapshot(scriptfile, lastmodified)))

                lastcontents = contents

                script.start()

                print "###", _snapshot(scriptfile, lastmodified), "started ###"

                lastrun = lastmodified

            time.sleep(0.5)
    except KeyboardInterrupt:
        print

if __name__ == "__main__":
    rerun(sys.argv[1])
