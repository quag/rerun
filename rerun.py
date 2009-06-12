#!/usr/bin/env python

import os
import sys
import time
import shutil
import difflib

def printDiff(file1, file2):
    f1 = file(file1)
    f2 = file(file2)

    print "".join(difflib.unified_diff(f1.readlines(), f2.readlines()))

    f1.close()
    f2.close()

if __name__ == "__main__":
    try:
        script = sys.argv[1]
        scriptbackup = script + "~"

        pid = None
        lastrun = 0

        while True:
            mtime = os.stat(script).st_mtime

            if mtime > lastrun:
                if pid:
                    os.kill(pid, 15) # SIGTERM: 15
                    printDiff(scriptbackup, script)

                shutil.copyfile(script, scriptbackup)

                pid = os.spawnl(os.P_NOWAIT, script)
                lastrun = mtime

                print "###", script, "started ###"

            time.sleep(0.5)
    except KeyboardInterrupt:
        print
