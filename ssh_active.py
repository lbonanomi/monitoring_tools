#!/bin/python

"""
Python Fabric to check SSH connectivity
"""

from fabric.api import *
from fabric.exceptions import NetworkError
from email.mime.text import MIMEText

import os
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
env.password = ""


def sendmail(hostname, engineer, alert_text):
    msg = MIMEText("Cannot SSH to host " + hostname + "\n\n" + alert_text)
    msg['Subject'] = "Cannot SSH to host " + hostname
    msg['From'] = 'someone@somewhere.net'
    msg['To'] = engineer

    sendmail_handle = smtplib.SMTP('localhost')
    sendmail_handle.sendmail('someone@somewhere.net', engineer, msg.as_string())
    sendmail_handle.quit()


def alert(hostname, alert_text):
    # This probably won't fit your workflow, but its what my operating cadre inherited.

    with open('email.list') as mailing_list:
        emails = mailing_list.readlines()

    email = [x.split()[0] for x in emails if '@' in x]

    for email_address in email:
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

                ## If this connection was successful AND we are down to a single '1' result, sound an all-clear.

                (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

                if fail_buffer.count(1) == 1 and fail_buffer[0] == 1:
                    alert(env.host_string, "All clear on " + str(e))

                    os.unlink(whisper_db_name)
                    whisper.create(whisper_db_name, retainer, aggregationMethod='last')


                whisper.update(whisper_db_name, 0)
                (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

            except FabricException as e:                    # Catch Fabric errors, like unexpected password prompts
                whisper.update(whisper_db_name, 1)

                (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

                if fail_buffer.count(1) > 5:
                    alert(env.host_string, str(e))


                    # This is a confirmed hard-outage now,
                    #
                    # We have fired an initial alert, now 
                    # triple WhisperDB period to reduce alarm repetition
                    #

                    new_whisper_db_name = whisper_db_dir + 'long_' + env.host_string + '.wsp'

                    new_retainer = [(retainer[0][0] * 3, 6)]

                    whisper.create(new_whisper_db_name, new_retainer, aggregationMethod='last')

                    whisper.update(new_whisper_db_name, 1)

                    os.rename(new_whisper_db_name, whisper_db_name)

    except Exception as e:
        whisper.update(whisper_db_name, 1)

        # Count failures
        (times, fail_buffer) = whisper.fetch(whisper_db_name, 315550800)

        if fail_buffer.count(1) > 5:
            alert(env.host_string, str(e))


            # Change WhisperDB period to reduce alarm repetition
            #

            new_whisper_db_name = whisper_db_dir + 'long_' + env.host_string + '.wsp'

            new_retainer = [(retainer[0][0] * 3, 6)]

            #print "Instancing temp whisperDB " + new_whisper_db_name + " with retention policy " + str(new_retainer)

            whisper.create(new_whisper_db_name, new_retainer, aggregationMethod='last')

            whisper.update(new_whisper_db_name, 1)

            #print "Swapping " + new_whisper_db_name + " over " + whisper_db_name

            os.rename(new_whisper_db_name, whisper_db_name)

