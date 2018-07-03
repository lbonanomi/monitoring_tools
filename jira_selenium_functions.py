#!/bin/python

import os
import sys

import re
import time

from datetime import datetime, date, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


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

    username_field = driver.find_element_by_id("login-form-username")

    if username_field.is_displayed():

        try:
            username_field = driver.find_element_by_id("login-form-username")
        except Exception as e:
            raise ValueError('No username field found')

        username_field.clear()
        username_field.send_keys(username)


        try:
            password_field = driver.find_element_by_id("login-form-password")
        except Exception as e:
            raise ValueError('No password field found')

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

    if activity_gadget.is_displayed():
        print "I see the activity stream for user!"
        return(0)
    else:
        print "No activity stream visible!"
    return(1)


def check_dir_sync(driver, url, password):
    """Check LDAP directory's sync state"""

    dire = url + '/secure/admin/user/UserBrowser.jspa'

    try:
        driver.get(dire)
    except Exception as e:
        raise ValueError("Could not get " + url)


    sudo_password_field = driver.find_element_by_id("login-form-authenticatePassword")

    sudo_password_field.clear()
    sudo_password_field.send_keys(password)

    sudo_button = driver.find_element_by_id("login-form-submit")
    sudo_button.click()

    dire = url + '/plugins/servlet/embedded-crowd/directories/list'
    driver.get(dire)


    for piglet in driver.find_element_by_id("directory-list").find_elements_by_tag_name("td"):

        if 'synchronised' in piglet.text:
            status = piglet.text.split().pop()

            simple_stamp = piglet.text.split()[5:8]

            datetime_object = datetime.strptime(' '.join(simple_stamp), '%m/%d/%y %I:%M %p')
            now = int(datetime.now().strftime('%s'))
            then = int(datetime_object.strftime('%s'))

            standoff = now - then
            #print "SYNCED " + str(standoff) + " seconds-ago"
            #print piglet.text

            if piglet.text.split().pop() == "successfully.":
                print "Directory sync good."

                if standoff < 3660:
                    print "Within-the-hour"
                    return(0)
                else:
                    print "Directory arrears"
                    return(0)
            else:
                #print "Directory sync failed"
                return(1)


def progress_issue(driver, key):
    print


def search(driver, key):
    proj_url =  url + '/projects/' + key + '/issues/?jql=project%20%3D%20_$PROJECT-NAME-HERE_AND%20creator%20%3D%20_$ADMIN-USER_%20ORDER%20BY%20created%20DESC'

    driver.get(proj_url)

    polaroid = driver.get_screenshot_as_png()
    with open("/var/tmp/polaroid3.png", 'w') as screencap:
        screencap.write(polaroid)

    # Grab the first issue to be seen
    #

    for dc in driver.find_elements_by_class_name("issue-list"):
        issues = dc.text.split()
        print issues[0]


def create_issue(driver, url):
    create_url = url + '/secure/CreateIssue!default.jspa'
    driver.get(create_url)

    project_field = driver.find_element_by_id("project-field")
    project_field.send_keys("$PROJECT")


    type_field = driver.find_element_by_id("issuetype-field")
    type_field.send_keys("Task\n")


    ## WINNER
    ##
    project_field.send_keys(Keys.ALT, 's')

    summary_field = driver.find_element_by_id("summary")
    summary_field.send_keys("Summary Text")


    summary_field.send_keys(Keys.ALT, 's')

    polaroid = driver.get_screenshot_as_png()
    with open("/var/tmp/polaroid3.png", 'w') as screencap:
        screencap.write(polaroid)
