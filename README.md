# Monitoring Tools

> All along the watchtower...  
> -Jimi Hendrix  


System and application monitoring is like High School: subject to fads, managed by cliques and generally forgotten-about as soon as it is completed. Also like High School, your faithful author is not sitting at the popular clique's lunch table and does not get much attention. So while Employer searches for a magic bullet, here are a few sanity preserving monitor scripts runnable by SysOps with minimal privileges.


[ssh_active.py](ssh_active.py): A python [Fabric](http://www.fabfile.org) file for parsing a host list and checking SSH connectivity. To cut noise hosts are not considered "down" until they have failed to connect at-least 4 of the last 6 checks. Check-state is maintained in a [whisper](https://github.com/graphite-project/whisper) database.


[Jira Pulse](jira_pulse): Simple monitoring for a fleet of JIRA instances. Look for connectivity and confirm basic functionality and response times with REST calls. Connection timeouts and too-slow responses trigger SMS cascades through Twilio, all responses are clocked against Employer's grafana in the production run. 


[jira_selenium_monitoring](https://github.com/lbonanomi/monitoring_tools/blob/jira_selenium/jira_selenium_monitoring): Interactive Jira checks with python [Fabric](https://github.com/fabric/fabric) and [Selenium](https://github.com/SeleniumHQ/selenium). This is a different monitoring approach to [Jira Pulse](jira_pulse), Selenium monitoring better-reflects user experience by attempting to log in and generate tickets and progress Jira issues. Use case: the application proxy was switched from 'first' to 'roundrobin'.
