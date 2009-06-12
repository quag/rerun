#!/usr/bin/env python

import os
import sys
import time
import difflib
import signal
import subprocess

def kill(process):
    try:
        process.terminate()
    except:
        # Fall back for pre-2.6, but only works on Unix platforms
        os.kill(process.pid, signal.SIGTERM)

def readlines(path):
    f = file(path)
    lines = f.readlines()
    f.close
    return lines

def diffname(name, timestamp):
    return time.asctime(time.localtime(timestamp)) + " " + name

if __name__ == "__main__":
    try:
        script = sys.argv[1]
        scriptpath = os.path.abspath(script)

        process = None
        lastrun = 0
        lastcontents = None

        while True:
            lastmodified = os.stat(script).st_mtime

            if lastmodified > lastrun:

                if process:
                    kill(process)

                contents = readlines(script)

                if lastcontents:
                    print
                    print "".join(difflib.unified_diff(lastcontents, contents, fromfile=diffname(script, lastrun), tofile=diffname(script, lastmodified)))

                lastcontents = contents

                process = subprocess.Popen(scriptpath)

                print "###", script, "started ###"

                lastrun = lastmodified

            time.sleep(0.5)
    except KeyboardInterrupt:
        print
