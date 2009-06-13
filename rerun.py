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
                self.process.wait()
            except:
                # Fall back for pre-2.6, but only works on Unix platforms
                os.kill(self.process.pid, signal.SIGTERM)
                os.waitpid(self.process.pid, 0)
            self.process = None

    def running(self):
        return self.process != None and self.process.poll() == None

    def poll(self):
        if self.process == None:
            return None
        else:
            returncode = self.process.poll()
            if returncode != None:
                self.process = None

            return returncode

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
            if script.running():
                script.stop()
                print "### %s stopped ###" % snapshot.name

            snapshot = script.snapshot()
            if lastsnapshot:
                print "\n", lastsnapshot.diff(snapshot)
            lastsnapshot = snapshot

            script.start()
            print "### %s started ###" % snapshot.name
            time.sleep(0.1)

        returncode = script.poll()
        if returncode != None:
            print "### %s finished (exit status: %s) ###" % (snapshot.name, returncode)

        time.sleep(0.5)

if __name__ == "__main__":
    try:
        rerun(sys.argv[1])
    except KeyboardInterrupt:
        print
