#!/usr/bin/env python

import os
import sys
import time
import shutil
import difflib
import signal
import subprocess

def printDiff(file1, file2):
    f1 = file(file1)
    f2 = file(file2)

    print "".join(difflib.unified_diff(f1.readlines(), f2.readlines()))

    f1.close()
    f2.close()

def kill(process):
    try:
        process.terminate()
    except:
        # Fall back for pre-2.6, but only works on Unix platforms
        os.kill(process.pid, signal.SIGTERM)

if __name__ == "__main__":
    try:
        script = os.path.abspath(sys.argv[1])
        backup = script + "~"

        process = None
        lastrun = 0

        while True:
            lastmodified = os.stat(script).st_mtime

            if lastmodified > lastrun:
                lastrun = lastmodified

                if process:
                    kill(process)
                    printDiff(backup, script)

                shutil.copyfile(script, backup)

                process = subprocess.Popen(script)

                print "###", script, "started ###"

            time.sleep(0.5)
    except KeyboardInterrupt:
        print
