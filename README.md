# Monitoring Tools

> All along the watchtower...  
> -Jimi Hendrix  


System and application monitoring is like High School: subject to fads, managed by cliques and generally forgotten-about as soon as it is completed. Also like High School, your faithful author is not sitting at the popular clique's lunch table and does not get much attention. So while Employer searches for a magic bullet, here are a few sanity preserving monitor scripts runnable 


[ssh_active.py](ssh_active.py): A python [Fabric](http://www.fabfile.org) file for parsing a host list and checking SSH connectivity. To cut noise hosts are not considered "down" until they have failed to connect at-least 4 of the last 6 checks. Check-state is maintained in a [whisper](https://github.com/graphite-project/whisper) database. ***Please be aware that this script still generates much chatter once a problem is detected***, noise-reduction is in-progress.


[Jira Pulse](jira_pulse): Simple monitoring for a fleet of JIRA instances. Look for connectivity and confirm basic functionality and response times with REST calls. Connection timeouts and too-slow responses trigger SMS cascades through Twilio, all responses are clocked against Employer's grafana in the production run. 
