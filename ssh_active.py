#!/bin/python

"""
Fabric to check SSH connectivity
"""

from fabric.api import *
from fabric.exceptions import NetworkError
from email.mime.text import MIMEText


import os
import requests
import smtplib
import string
import sys
import whisper


with open('/etc/hosts') as listing:
        raw = listing.readlines()
env.hosts = [line.split()[1] for line in raw if 'continuous_build' in line and 'global_zone' not in line]   # Little white lie about the filename


env.parallel = True             # like '-P' for parallel exec
env.pool_size = 10              # like '-z' for pool-sizing
env.timeout = 6                 # SSH timeout in seconds
env.disable_known_hosts = False  


def sendmail(hostname, engineer):
        msg = MIMEText("Cannot SSH to host " + hostname)
        msg['Subject'] = "Cannot SSH to host " + hostname
        msg['From'] = 'someone@somewhere.net'
        msg['To'] = engineer

        sendmail_handle = smtplib.SMTP('localhost')
        sendmail_handle.sendmail('someone@somewhere.net', engineer, msg.as_string())
        sendmail_handle.quit()


def alert(hostname):
        # This probably won't fit your workflow, but its what my operating cadre inherited.

        with open('email.list') as mailing_list:
                emails = mailing_list.readlines()
        email = [x.split()[0] for x in emails if '@' in x]

        for email_address in email:
            sendmail(hostname, email_address)


def uptime():
        """SSH to host, record SSH connectivity in whisperDB"""

        # Whisper
        #

        retainer = [(1800, 6)]          # [(seconds_in_period, slots_in_period)]

        whisper_db_dir = '/var/tmp/whisperDB/'

        whisper_db_name = whisper_db_dir + env.host_string + '.wsp'

        if not os.path.isdir(whisper_db_dir):
                os.mkdir(whisper_db_dir)

        if not os.path.exists(whisper_db_name):
                whisper.create(whisper_db_name, retainer)

            try:
                    with hide('stdout', 'stderr', 'running'):
                            connector = run('uptime')

                    whisper.update(whisper_db_name, 0)

                    (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

            except NetworkError as e:
                    whisper.update(whisper_db_name, 1)

                    # Count failures
                    (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

                    if fail_buffer.count(1) > 4:
                            alert(env.host_string)
