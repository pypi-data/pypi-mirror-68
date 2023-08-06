
import os

environment = os.environ

PROTOCOL = environment['PROTOCOL'] if 'PROTOCOL' in environment else "http://"
PORTDISCOVER = int(environment['PORTDISCOVER']) if 'PORTDISCOVER' in environment else 5210
HOSTDISCOVER = environment['HOSTDISCOVER'] if 'HOSTDISCOVER' in environment else "http://localhost:{}/eureka/apps".format(PORTDISCOVER)
SERVICENAME = environment['SERVICENAME'] if 'SERVICENAME' in environment else "<Service Name>"
HOSTINSTANCE = environment['HOSTINSTANCE'] if 'HOSTINSTANCE' in environment else ''.join(open("/etc/hostname", "r").readlines()).split()[0]
PORTINSTANCE = environment['PORTINSTANCE'] if 'PORTINSTANCE' in environment else PORTDISCOVER
HEARTBEATDISCOVER = environment['HEARTBEATDISCOVER'] if 'HEARTBEATDISCOVER' in environment else 30
