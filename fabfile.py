#!/opt/bb/bin/python

"""
Fabric to check SSH connectivity
"""

from fabric.api import *
from fabric.exceptions import NetworkError
from email.mime.text import MIMEText


import os
import requests
import smtplib
import whisper


with open('/etc/hosts') as listing:
    raw = listing.readlines()
env.hosts = [line.split()[1] for line in raw if 'continuous_build' in line and 'global_zone' not in line]


# Continue on error.
#

class FabricException(Exception):
    pass

env.abort_exception = FabricException


env.parallel = True    # like '-P' for parallel exec
env.pool_size = 10     # like '-z' for pool-sizing
env.timeout = 66       # SSH timeout in seconds

env.disable_known_hosts = True  
env.warn_only = True
env.skip_bad_hosts = True

env.password = ""    # This is funny...


def sendmail(hostname, engineer, alert_text):
    msg = MIMEText("Cannot SSH to host " + hostname + "\n\n" + alert_text)
    msg['Subject'] = "Cannot SSH to host " + hostname
    msg['From'] = 'lbonanomi2@bloomberg.net'
    msg['To'] = engineer

    sendmail_handle = smtplib.SMTP('localhost')
    sendmail_handle.sendmail('lbonanomi2@bloomberg.net', engineer, msg.as_string())
    sendmail_handle.quit()


def alert(hostname, alert_text):
    # This probably won't fit your workflow, but its what my operating cadre inherited.

    with open('email.list') as mailing_list:
        emails = mailing_list.readlines()
    email = [x.split()[0] for x in emails if '@' in x]

    for email_address in email:
        print "FOUND " + email_address

        sendmail(hostname, email_address, alert_text)

@task(alias='ssh_check')
def uptime():
    """SSH to host, record SSH connectivity in whisperDB"""

    retainer = [(300, 6)]      # [(seconds_in_period, slots_in_period)]

    whisper_db_dir = '/var/tmp/whisperDB/'

    whisper_db_name = whisper_db_dir + env.host_string + '.wsp'

    if not os.path.isdir(whisper_db_dir):
        os.mkdir(whisper_db_dir)

    if not os.path.exists(whisper_db_name):
        whisper.create(whisper_db_name, retainer, aggregationMethod='last')

    try:
        with hide('stdout', 'stderr', 'running'):
            try:
                connector = run('uptime')

            except FabricException as e:                # Catch Fabric errors, like unexpected password prompts
                whisper.update(whisper_db_name, 1)

                (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)
                if fail_buffer.count(1) > 1:
                    alert(env.host_string, str(e))


        ## If this connection was successful AND we are down to a single '1' result, sound an all-clear.

        (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

        if fail_buffer.count(1) == 1 and fail_buffer[0] == 1:
            alert(env.host_string, "All clear on " + str(e))

        whisper.update(whisper_db_name, 0)

        (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

    except Exception as e:
        whisper.update(whisper_db_name, 1)

        (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

        if fail_buffer.count(1) > 1:
            alert(env.host_string, str(e))

