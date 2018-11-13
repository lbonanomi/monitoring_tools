# Monitoring Tools

> All along the watchtower...  
> -Jimi Hendrix  


System and application monitoring is like High School: subject to fads, managed by cliques and generally forgotten-about as soon as it is completed. Also like High School, your faithful author is not sitting at the popular clique's lunch table and does not get much attention. So while Employer searches for a magic bullet, here are a few sanity preserving monitor scripts runnable by SysOps with minimal privileges.


[ssh_active.py](ssh_active.py): A python [Fabric](http://www.fabfile.org) file for parsing a host list and checking SSH connectivity. To cut noise hosts are not considered "down" until they have failed to connect 3 times. "Down" hosts will generate follow-up alerts 2/3rds less frequently to try and reduce alarm apathy. Check-state is maintained in a [whisper](https://github.com/graphite-project/whisper) database.  
   
**Please Note:** This script is modelled on a 5 minute cron cycle and it **really** needs a passwordless auth mechanism.


[Jira Pulse](jira_pulse): Simple monitoring for a fleet of JIRA instances. Look for connectivity and confirm basic functionality and response times with REST calls. Connection timeouts and too-slow responses trigger SMS cascades through Twilio, all responses are clocked against Employer's grafana in the production run. 


[Jira Selenium Checks(jira-selenium): Demonstration of Selenium and Google Chromium to test the health of a Jira instance. This is predicated on [Fabric](http://www.fabfile.org) ***Version 1***
