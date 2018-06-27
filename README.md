# Monitoring Tools

Python [Fabric](http://www.fabfile.org) for basic monitoring.

[ssh_active.py](ssh_active.py) A python Fabric file for parsing a host list and checking SSH connectivity. Hosts are not "down" until they have failed to connect at-least 4 of the last 6 checks. This fabric is cronned to run against $EMPLOYER's (iron) continuous build farm members every 5 minutes.
