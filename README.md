# Monitoring Tools

> All along the watchtower...  
> -Jimi Hendrix  


[ssh_active.py](ssh_active.py): A tool for checking SSH connectivity. To cut noise hosts are not considered "down" until they have failed to connect 3 times. "Down" hosts will generate follow-up alerts 2/3rds less frequently to try and reduce alarm apathy. Check-state is maintained in a [whisper](https://github.com/graphite-project/whisper) database.  

*Script pivoted to accept hostname as argument*.  

[Jira Pulse](jira_pulse): Simple monitoring for a fleet of JIRA instances. Look for connectivity and confirm basic functionality and response times with REST calls. Connection timeouts and too-slow responses trigger SMS cascades through Twilio, all responses are clocked against Employer's grafana in the production run. 


[Jira Selenium Checks](jira-selenium): Demonstration of Selenium and Google Chromium to test the health of a Jira instance. This is predicated on [Fabric](http://www.fabfile.org) ***Version 1***
