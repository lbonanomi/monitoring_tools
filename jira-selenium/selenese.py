#!/bin/python

import os
import sys

import requests
import time

from datetime import datetime, date, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import selenium.common.exceptions


def chrome_driver():
    """Instance Selenium headless Chrome session"""

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-proxy-server")


    if os.path.isfile('/bin/google-chrome'):
        chrome_options.binary_location = '/bin/google-chrome'
    else:
        raise ValueError('No Chrome Browser Binary')


    if os.path.isfile('/usr/local/bin/chromedriver'):
        chromedriver = "/usr/local/bin/chromedriver"
    else:
        raise ValueError('No Chromedriver Binary')


    try:
        driver = webdriver.Chrome(executable_path=os.path.abspath(chromedriver),   chrome_options=chrome_options)
        return(driver, 0)

    except Exception as e:
        raise ValueError('Failed to Instance')
        return(str(e), 1)


def login(driver, url, username, password):
    """Login to Jira with the vendor's web form"""

    try:
        driver.get(url)
    except Exception as e:
        return(1)


    try:
        username_field = driver.find_element_by_id("login-form-username")

    except selenium.common.exceptions.NoSuchElementException:
        polaroid = driver.get_screenshot_as_png()
        with open("/var/tmp/latest_mess.png", 'w') as screencap:
            screencap.write(polaroid)

        raise ValueError('No username field found')

    username_field.clear()
    username_field.send_keys(username)


    try:
        password_field = driver.find_element_by_id("login-form-password")
    except Exception as e:
        polaroid = driver.get_screenshot_as_png()
        with open("/var/tmp/polaroid1.png", 'w') as screencap:
            screencap.write(polaroid)

        raise ValueError(str(e))

    password_field.clear()
    password_field.send_keys(password)


    try:
        login_button = driver.find_element_by_id("login-form-submit")
    except Exception as e:
        raise ValueError('No submit button found')

    login_button.click()

    return(0)


def scrape_dash(driver, url):
    """Find the user's activity stream panel. Note: making some wild assumptions, here."""

    try:
        driver.get(url)
    except Exception as e:
        raise ValueError("Could not get " + url)


    activity_gadget = driver.find_element_by_id("gadget-10003")   # This may not stand...


    polaroid = driver.get_screenshot_as_png()
    with open("/var/tmp/dashboard.png", 'w') as screencap:
        screencap.write(polaroid)


    if activity_gadget.is_displayed():
        print "I see the activity stream for user!"
        return(0)
    else:
        print "No activity stream visible!"
    return(1)


def check_dir_sync(driver, url, username, password):
    """Check LDAP directory's sync state"""

    dire = url + '/secure/admin/user/UserBrowser.jspa'

    try:
        driver.get(dire)
    except Exception as e:
        raise ValueError("Could not get " + url)


    try:
        sudo_password_field = driver.find_element_by_id("login-form-authenticatePassword")

        sudo_password_field.clear()
        sudo_password_field.send_keys(password)

        sudo_button = driver.find_element_by_id("login-form-submit")
        sudo_button.click()

    except selenium.common.exceptions.NoSuchElementException:
        try:
            current_session = driver.find_element_by_class_name("aui-nav-heading")
            print "Session is current"

        except Exception:
            print "Getting a screenshot and dying."


            polaroid = driver.get_screenshot_as_png()
            with open("/var/tmp/no_password.png", 'w') as screencap:
                screencap.write(polaroid)

            return(1)
            raise ValueError("No password field found " + url)


    dire = url + '/plugins/servlet/embedded-crowd/directories/list'
    driver.get(dire)

    betterness = driver.find_element_by_id("directory-list").find_element_by_tag_name("tbody").find_elements_by_class_name("operations-column")

    for hammer in betterness:
        nail = hammer.find_elements_by_tag_name("p")

        for roofing in nail:
            if 'sync' in roofing.text or 'Sync' in roofing.text:

                if ':' in roofing.text:
                    simple_stamp = roofing.text.split()[3:6]
                    simple_object = datetime.strptime(' '.join(simple_stamp), '%m/%d/%y %I:%M %p')

                    now = int(datetime.now().strftime('%s'))
                    then = int(simple_object.strftime('%s'))

                    standoff = now - then

                # Return seconds-since-last-sync, or 0 for sync issues

                elif 'completed successfully' in roofing.text:
                    return(standoff)

                elif 'Synchronisation failed' in roofing.text:
                    print 'Sync is failed. Trombones.'
                    return(0)


def progress_issue(driver, url, username, issue):
    issue_url = url + '/browse/' + issue

    try:
        driver.get(issue_url)
    except Exception as e:
        print "Trombones"


    # In progress
    #

    print "FLAG 1"

    #
    # Action 31 is the default "In Progress" action

    ip_button = driver.find_element_by_id("action_id_31")
    ip_button.click()


    # Bloody Selenium...

    print "FLAG 2"

    workflow_menu = driver.find_element_by_id("opsbar-transitions_more")

    print dir(workflow_menu)

    workflow_menu.click()


    # Done
    #

    done_link = driver.find_element_by_id("action_id_101")
    done_link.click()



def search(driver, url, username, project):
    proj_url =  url + '/issues/?jql=project%20%3D%20' + project + '%20AND%20creator%20%3D%20' + username + '%20ORDER%20BY%20created%20DESC'

    driver.get(proj_url)

    polaroid = driver.get_screenshot_as_png()
    with open("/var/tmp/searching.png", 'w') as screencap:
        screencap.write(polaroid)

    # Grab the first issue to be seen
    #

    for dc in driver.find_elements_by_class_name("issue-list"):
        issues = dc.text.split()
        return(issues[0])


def create_issue(driver, url, project):

    # Land in test project first...
    #

    lz_url = url + '/browse/' + project
    driver.get(lz_url)

    if 'Project not found' in driver.title:
        raise ValueError('No Project')


    # Create an issue
    #

    create_url = url + '/secure/CreateIssue!default.jspa'
    driver.get(create_url)

    project_field = driver.find_element_by_id("project-field")
    project_field.send_keys(project)


    type_field = driver.find_element_by_id("issuetype-field")
    type_field.send_keys("Task\n")

    project_field.send_keys(Keys.ALT, 's')

    summary_field = driver.find_element_by_id("summary")
    summary_field.send_keys("Summary Text")

    summary_field.send_keys(Keys.ALT, 's')

    polaroid = driver.get_screenshot_as_png()
    with open("/var/tmp/polaroid3.png", 'w') as screencap:
        screencap.write(polaroid)
