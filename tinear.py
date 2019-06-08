#!/bin/python
"""alert concentrating mail handler"""

import base64
import os
import whisper
import sys

RETAINER = [(300, 3)]                       # [(seconds_in_period, slots_in_period)]
FOLLOWUP = [(900, 3)]

def waterlevel(db_name):
    """Reduce alert frequency after initial alert, reset on all-clear"""

    (times, fail_buffer) = whisper.fetch(db_name, 315550800)

    if fail_buffer.count(1) > 2:
        new_whisper_db_name = db_name + '.wsp2'
        whisper.create(new_whisper_db_name, FOLLOWUP, aggregationMethod='last')
        whisper.update(new_whisper_db_name, 1)
        os.rename(new_whisper_db_name, db_name)

        for admin in sys.argv[2:]:
            os.system('mail -s "' + sys.argv[1] + '" ' + admin + '</dev/null')

    if fail_buffer.count(1) == 0:
        if whisper.info(db_name)['archives'][0]['secondsPerPoint'] == FOLLOWUP[0][0]:
            new_whisper_db_name = db_name + '.wsp2'
            whisper.create(new_whisper_db_name, RETAINER, aggregationMethod='last')
            whisper.update(new_whisper_db_name, 0)
            os.rename(new_whisper_db_name, db_name)

            for admin in sys.argv[2:]:
                os.system('mail -s "' + sys.argv[1] + '" ' + admin + '</dev/null')

    return(0)

whisper_db_dir = '/var/tmp/whisperDB/'
whisper_db_name = str(whisper_db_dir + base64.b64encode(sys.argv[1]) + '.wsp')

if not os.path.exists(whisper_db_dir):
    os.path.mkdir(whisper_db_dir)

if not os.path.exists(whisper_db_name):
    whisper.create(whisper_db_name, RETAINER, aggregationMethod='last')

if os.path.basename(sys.argv[0]) == "tinear.ok":
    whisper.update(whisper_db_name, 0)

if os.path.basename(sys.argv[0]) == "tinear.nok":
    whisper.update(whisper_db_name, 1)

waterlevel(whisper_db_name)
