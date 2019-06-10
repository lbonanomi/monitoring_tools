#!/bin/python2.7

import sys
sys.path.append('/usr/lib/python2.6/site-packages')

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
import requests
import signal
import json
import time
import re

# Hush the complaints about SSL MITM
#
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#
# Timeout handler
#

# Define timeout handler
def handler(signum, frame):
    raise Exception("exec_timeout")

# Associate timeout handler with SIGALRM
signal.signal(signal.SIGALRM, handler)


def getter(url, timeout_value=3.0, **kwargs):
    signal.alarm(int(timeout_value))

    start_time = time.time()

    try:
        kwargs['auth']

        try:
            views = requests.get(url, auth=kwargs['auth'], verify=False, timeout=timeout_value)

        except Exception as e:
            if (re.search('Connection refused', str(e))):
                raise Exception("connection_refused")
            elif (re.search('Read timed out', str(e))):
                raise Exception("net_timeout")
            elif (re.search('exec_timeout', str(e))):
                raise Exception("exec_timeout")
            else:
                print "IDUNNO: " + str(e)
                return([ e ], 777, 777)

    except Exception:
        try:
            views = requests.get(url, verify=False, timeout=timeout_value)

        except Exception as e:
            if (re.search('Connection refused', str(e))):
                raise Exception("connection_refused")
            elif (re.search('Read timed out', str(e))):
                raise Exception("timeout")
            elif (re.search('exec_timeout', str(e))):
                raise Exception("exec_timeout")
            else:
                print "IDUNNO: " + str(e)
                return([ e ], 777, 777)
    end_time = time.time()

    # Stats
    #

    request_time = (end_time - start_time)

    status = views.status_code

    try:
        return (views.json(), request_time, status)

    except Exception as e:
        return(views.content, request_time, status)

###

try:
    try:
        timeout_value = config[service][url]['timeout'] + '.0'
    except Exception:
        timeout_value = 3.0

    timeout_value = float(timeout_value)

    try:
        # Look for credentials first, and then run a check
        #

        plain_auth = HTTPBasicAuth(config[service][url]['username'], config[service][url]['password'])
        (response_text, response_time, status) = getter(url, timeout_value, auth=plain_auth)

    except Exception as e:
        # Run an anonymous check if no username/password defined
        #

        (response_text, response_time, status) = getter(url, timeout_value)

    # Update Grafana with raw code

    if sys.stdout.isatty():
        print "Sending " + str(status)

except Exception as e:
    # Update Grafana with contrived error code
