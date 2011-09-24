#!/usr/bin/env python

import time
import subprocess
import threading
from functools import partial   

VERSION='1.0'

"""Inspired by Jose Nazario PHP sandbox, extended/modified by Lukas Rist"""

def killer(proc, secs):
    time.sleep(secs)
    try:
        proc.kill()
    except OSError:
        pass

def sandbox(script, secs):
    try:
        proc = subprocess.Popen(["php", "sandbox/apd_sandbox.php", "files/" + script], 
                shell = False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
    except Exception as e:
        print "PARENT : error executing the sandbox:"
        print e.message
    stdout_value = ""
    stderr_value = ""
    try:
        threading.Thread(target=partial(killer, proc, secs)).start()
        stdout_value, stderr_value = proc.communicate()
    except Exception as e:
        print "Sandbox communication error:", e.message
    else:
        print "Successfully parsed with sandbox"
    return stdout_value
    
def run(script):
    secs = 10
    return sandbox(script, secs)