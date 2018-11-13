#!/bin/python

"""
Fabric to check Jira health with Selenium and Google Chrome
"""


from fabric.api import *
from fabric.exceptions import NetworkError
from selenese import *


username = '$ADMIN_USER'
password = '$ADMIN_PASS'
project = '$PROJECT_KEY'


@task
def dashboard():
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


def issue():
    url = 'https://' + env.host_string

    login_url = 'https://' + env.host_string + "/login.jsp"

    (driver, status) = chrome_driver()

    try:
        login(driver, login_url, username, password)
        create_issue(driver, url, project)

    except ValueError as e:
        print "E: " + str(e)


@task
def issue_search():
    url = 'https://' + env.host_string

    login_url = 'https://' + env.host_string + "/login.jsp"

    (driver, status) = chrome_driver()

    try:
        login(driver, login_url, username, password)
        create_issue(driver, url, project)
    except ValueError as e:
        print "E: " + str(e)


    try:
        issue = search(driver, url, username, project)

        print issue

    except ValueError as e:
        print "E: " + str(e)


@task
def issue_exerciser():
    url = 'https://' + env.host_string

    login_url = 'https://' + env.host_string + "/login.jsp"

    (driver, status) = chrome_driver()

    try:
        login(driver, login_url, username, password)

        issue = search(driver, url, username, project)

        print "Moving " + issue + " around"

        progress_issue(driver, url, username, issue)


    except ValueError as e:
        print "E: " + str(e)
