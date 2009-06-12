#!/usr/bin/env python

import os
import sys
import time
import difflib
import signal
import subprocess

class Script:
    def __init__(self, name):
        self.name = name
        self.path = os.path.abspath(name)
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

    def snapshot(self):
        return ScriptSnapshot(self.name, self.modifiedtime(), self.contents())

    def modifiedtime(self):
        return os.stat(self.path).st_mtime

    def contents(self):
        f = file(self.path)
        try:
            return f.readlines()
        finally:
            f.close()

class ScriptSnapshot:
    def __init__(self, name, modifiedtime, contents):
        self.name = "%s (%s)" % (name, time.asctime(time.localtime(modifiedtime)))
        self.modifiedtime = modifiedtime
        self.contents = contents

    def diff(self, snapshot):
        return "".join(difflib.unified_diff(self.contents, snapshot.contents, fromfile=self.name, tofile=snapshot.name))

def rerun(scriptfile):
    script = Script(scriptfile)
    lastsnapshot = None

    while True:
        if lastsnapshot == None or script.modifiedtime() != lastsnapshot.modifiedtime:
            script.stop()

            snapshot = script.snapshot()
            if lastsnapshot:
                print "\n", lastsnapshot.diff(snapshot)
            lastsnapshot = snapshot

            script.start()
            print "###", snapshot.name, "started ###"

        time.sleep(0.5)

if __name__ == "__main__":
    try:
        rerun(sys.argv[1])
    except KeyboardInterrupt:
        print
