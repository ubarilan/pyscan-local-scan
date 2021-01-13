#!/usr/bin/python3
import os
import sys
import subprocess
import threading
from termcolor import colored
import pyfiglet
ascii_banner = pyfiglet.figlet_format("PYSCAN")

print(colored(ascii_banner, 'green'))
def getStringFromBraces(string):
	return string.replace('(', '').replace(')','')

def drawHost(hostString):
	args = hostString.split(" ")
	print(colored(getStringFromBraces(args[0]), 'red'), colored('[', 'blue'), colored(getStringFromBraces(args[1]), 'green'), colored(']', 'blue'))
	
print("Starting arp scan...", end='\r')
arpResult = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8 ')
print("Finished arp scan...", end='\r')
ips = list(map(lambda e: e.split(")")[0], arpResult.split("(")))[1::]
connections = arpResult.split("\n")
hosts = list(map(lambda e: e.split(" ")[0].replace('?', 'unknown')+' '+getStringFromBraces(e.split(" ")[1]), arpResult.split("\n")[:-1:] ))
reachable_ips = []
not_reachable_ips = []
ips_checked = 0
reachable_hosts = []

def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total 
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    finished = ''
    ending = ''
    if percent == 100:
    	ending = '\n'
    	finished = 'finished!'
    sys.stdout.write(f'\rProgress: [%s%s] %d %% [{current}/{total}] {finished}{ending}' % (arrow, spaces, percent))
    sys.stdout.flush()

progressBar(ips_checked, len(ips))

def check_reachable_ips(ip, number):
	global reachable_ips, not_reachable_ips, ips_checked, ips
	HOST_UP  =  not 'returncode=2' in str(subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE))
	if HOST_UP:
		reachable_ips.append(ip)
		reachable_hosts.append(number)
	else:
		not_reachable_ips.append(ip)
	ips_checked += 1
	progressBar(ips_checked, len(ips))


def ipList(hostIndexes):
	if len(hostIndexes) == 0:
		return 'No devices found'
	for i in range(len(hostIndexes)):
		drawHost(hosts[i])


try:
	for i, ip in enumerate(ips):
		x = threading.Thread(target=check_reachable_ips, args=(ip, i))
		x.start()
	while ips_checked != len(ips):
		pass

except KeyboardInterrupt:
	print(colored('[-]', 'red'), 'Stopping scan...')
	sys.exit()

print(f'\nDevices found on your network ({len(reachable_ips)} of {ips_checked}):')
ipList(reachable_hosts)

sys.stdout.flush()