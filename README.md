# Monitoring Tools

> All along the watchtower...  
> -Jimi Hendrix  

[ssh_active.py](ssh_active.py): A python [Fabric](http://www.fabfile.org) file for parsing a host list and checking SSH connectivity. To cut noise hosts are not considered "down" until they have failed to connect at-least 4 of the last 6 checks. Check-state is maintained in a [whisper](https://github.com/graphite-project/whisper) database.


[Jira Pulse](jira_pulse): Simple monitoring for a fleet of JIRA instances. Look for connectivity and confirm basic functionality and response times with REST calls. Connection timeouts and too-slow responses trigger SMS cascades through Twilio, all responses are clocked against Employer's grafana. 
