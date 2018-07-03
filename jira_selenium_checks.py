#!/bin/python

"""
Fabric to check Jira Health
"""


from fabric.api import *
from fabric.exceptions import NetworkError
from jira_selenium_functions import *


print env.host_string

username = ''
password = ''


@task
def dashboard():
    url = 'https://' + env.host_string
    
    login_url = 'https://' + env.host_string + "/login.jsp"
    dashboard_url = 'https://' + env.host_string + "/secure/Dashboard.jspa"

    (driver, status) = chrome_driver()

    try:
        login(driver, login_url, username, password)
        scrape_dash(driver, dashboard_url)

    except ValueError as e:
        if str(e) == 'No username field found':
            print "Could not find login page for https://" + env.host_string


@task
def directory_sync():
    url = 'https://' + env.host_string

    login_url = 'https://' + env.host_string + "/login.jsp"
    dashboard_url = 'https://' + env.host_string + "/secure/Dashboard.jspa"

    (driver, status) = chrome_driver()

    try:
        login(driver, login_url, username, password)
        check_dir_sync(driver, url, username, password)
        print "User directory sync up-to-date"

    except ValueError as e:
        print "E: " + str(e)


@task
def issue():
    url = 'https://' + env.host_string

    login_url = 'https://' + env.host_string + "/login.jsp"

    project = 'FEED_ME_A_PROJECT_KEY!!'

    (driver, status) = chrome_driver()

    try:
        login(driver, login_url, username, password)
        create_issue(driver, url, project)

    except ValueError as e:
        print "E: " + str(e)

@task
def issuesearch():
    url = 'https://' + env.host_string

    login_url = 'https://' + env.host_string + "/login.jsp"

    project = 'FEED_ME_A_PROJECT_KEY!!'

    (driver, status) = chrome_driver()

    try:
        login(driver, login_url, username, password)
        search(driver, url, username, project)

    except ValueError as e:
        print "E: " + str(e)
