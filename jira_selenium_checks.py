#!/bin/python

"""
Fabric to check Jira Health
"""


from fabric.api import *
from fabric.exceptions import NetworkError
from selenese import *


url = ''
username = ''
password = ''


#
dashboard_url = url + "/secure/Dashboard.jspa"
login_url = url + "/login.jsp"


@task
def dashboard():
    (driver, status) = chrome_driver()

    if login(driver, login_url, username, password) == 0:
        print "Logged-in to " + url

        scrape_dash(driver, dashboard_url)


@task
def directory_sync():
    (driver, status) = chrome_driver()

    if login(driver, login_url, username, password) == 0:
        print "Logged-in to " + url

        if check_dir_sync(driver, url, password) == 0:
            print "User directory sync up-to-date"
        else:
            print "User directory sync behind"


@task
def issue():
    (driver, status) = chrome_driver()

    if login(driver, login_url, username, password) == 0:
        print "Logged-in to " + url

        if create_issue(driver, url) == 0:
            print "Top-Level"
