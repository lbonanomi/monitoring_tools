#!/bin/python

import os
import sys

from selenese import chrome_driver, login, scrape_dash, search, check_dir_sync


username = ""    #Fill these in.
password = ""


url = sys.argv[1]
login_page = url + "/login.jsp"
dashboard_page = url + "/secure/Dashboard.jspa"


try:
    (driver, driver_status) = chrome_driver()

except Exception as e:
    print str(e)
    sys.exit(9)


try:
    url = sys.argv[1]
except Exception:
    print sys.argv[0] + " URL"
    sys.exit(2)


if login(driver, login_page, username, password) == 0:
    print "Driver instanced"
else:
    print "Could not instance driver"
    sys.exit(2)


# Log-in, look for a common dashboard widget
#

if scrape_dash(driver, dashboard_page) == 0:
    print "Scraped dashboard, login seems okay!"
else:
    print "Could not get " + username + "'s dashboard, cannot continue"
    sys.exit(1)


# Check state of user directories
#

if check_dir_sync(driver, url, password) == 0:
    print "Synced-up"
else:
    print "Directory Sync has failed"


#
#

#create_issue()


#print "Searching..."
#search('RDSISRE')

driver.quit()
