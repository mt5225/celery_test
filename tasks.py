from __future__ import absolute_import
from celery_test.celery import app
import subprocess
from pysnmp.entity.rfc3413.oneliner import cmdgen
import requests
import spur
import spur.ssh


@app.task
def add(x, y):
    return x+y


@app.task
def commandlineAdapter(*args):
    return subprocess.check_output(args[0].split())


@app.task
def snmpGetAdapter(*args):
    ip = args[0]
    community = args[1]
    oidString = args[2].split('.')
    oidNumber = [int(x) for x in oidString]
    oidValue = tuple(oidNumber)
    generator = cmdgen.CommandGenerator()
    # 1 means version SNMP v2c
    comm_data = cmdgen.CommunityData('server', community, 1)
    transport = cmdgen.UdpTransportTarget((ip, 161))
    real_fun = getattr(generator, 'nextCmd')
    res = (errorIndication, errorStatus, errorIndex, varBinds)\
        = real_fun(comm_data, transport, oidValue)
    if not errorIndication is None or errorStatus is True:
        return "Error: %s %s %s %s" % res
    else:
        return "%s" % varBinds


@app.task
def wsAdapter(*args):
    url = args[0]
    myResponse = requests.get(url)
    if(myResponse.ok):
        return myResponse.content
    else:
        return myResponse.raise_for_status()


@app.task
def sshAdapter(*args):
    hostname = args[0]
    port = args[1]
    username = args[2]
    password = args[3]
    commamd = args[4].split()
    shell = spur.SshShell(
        hostname=hostname,
        port=int(port),
        username=username,
        password=password,
        missing_host_key=spur.ssh.MissingHostKey.accept
    )
    with shell:
        result = shell.run(commamd)
        return result.output
