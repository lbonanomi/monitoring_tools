#!/opt/bb/bin/python3.6
"""SSH monitor with alert throttling"""

import os
import paramiko
import whisper

RETAINER = [(300, 3)]                       # [(seconds_in_period, slots_in_period)]
whisper_db_dir = '/var/tmp/whisperDB/'

def waterlevel(db_name):
    """Reduce alert frequency after initial alert, reset on all-clear"""
    (times, fail_buffer) = whisper.fetch(db_name, 315550800)

    if fail_buffer.count(1) > 2:
        # Initial alert
        print("W00p W00p!!")

        # Roll DB-over to alert 1/3 speed
        new_whisper_db_name = db_name + '.wsp2'
        new_retainer = [(RETAINER[0][0] * 3, RETAINER[0][1])]
        whisper.create(new_whisper_db_name, new_retainer, aggregationMethod='last')
        whisper.update(new_whisper_db_name, 1)

        os.rename(new_whisper_db_name, db_name)

    if fail_buffer.count(1) == 0:
        print("Sound all-clear")
        new_whisper_db_name = db_name + '.wsp2'
        whisper.create(new_whisper_db_name, RETAINER, aggregationMethod='last')
        whisper.update(new_whisper_db_name, 0)

def pinger(hostname):
    """Get host ssh-connectivity, record in whisperDB"""

    whisper_db_name = whisper_db_dir + hostname + '.wsp'

    if not os.path.exists(whisper_db_name):
        whisper.create(whisper_db_name, RETAINER, aggregationMethod='last')

    client = paramiko.SSHClient()
    client.load_system_host_keys()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, timeout=10)
        whisper.update(whisper_db_name, 0)

        waterlevel(whisper_db_name)

    except Exception as e:
        if str(e) == "timed out":
            whisper.update(whisper_db_name, 1)

            waterlevel(whisper_db_name)

pinger('bldibm-ob-189')
