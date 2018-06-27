#!/bin/python

"""Fabric to check SSH connectivity"""

# Fabric task-runner to check SSH connectivity. 
#
# If a host fails SSH connect-checks 6 times in 30 minutes
# fire the (placeholder) 'alert' function. WhisperDB will
# stores value

from fabric.api import *

import os
import string
import sys
import whisper


with open('host_list.tmp') as listing:
    env.hosts = map(string.strip, listing.readlines())

    
env.parallel = True     # like '-P' for parallel exec
env.pool_size = 10      # like '-z' for pool-sizing
env.timeout = 60        # SSH timeout in seconds


def alert(hostname):
    """Alerting mechanism"""
    print "Launch alerts for " + hostname + "\n"


def connect_check():
    retainer = [(1800, 6)]      # [(seconds_in_period, slots_in_period)]

    whisper_db_dir = '/var/tmp/whisperDB/'

    whisper_db_name = whisper_db_dir + env.host_string + '.wsp'

    if not os.path.isdir(whisper_db_dir):
        os.mkdir(whisper_db_dir)

    if not os.path.exists(whisper_db_name):
        whisper.create(whisper_db_name, retainer)

    with hide('stdout', 'stderr', 'running'):
       connector = run('uptime')

    if connector.succeeded:
        whisper.update(whisper_db_name, 0)

        (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

    if connector.failed:
        print "Gorked connecting-to: " + env.host_string

        whisper.update(whisper_db_name, 1)

        # Count failures
        (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

        if fail_buffer.count(1) > 6:
            alert(env.host_string)  
