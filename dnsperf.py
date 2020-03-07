#DNS Performance Test Script
#Version not finished ; Diese version ist noch nicht fertig


#Voraussetzungen:
#python 3
#dnspython (pip install dnspython)
#colorama (pip install colorama)

#Ausführen:
#python dnsperf.py (oder python <datei>.py)


# ------------ config ------------ #
domains = ["google.com", "amazon.com", "facebook.com"] #Domains die von den DNS-Servern aufgelöst werden sollen.

anzahldurchlaeufe = 1 #anzahl von tests
# ------------ config ------------ #

import dns.resolver
import sys
import time
import argparse
import colorama

colorama.init()
print(colorama.Fore.GREEN)

parser = argparse.ArgumentParser(description="DNS-Server performance test script")
parser.add_argument("dns_servers", type=str, help="DNS-Servers with : seperated (for example 8.8.8.8:9.9.9.9:1.1.1.1 ...)")
parser.add_argument("--domains", type=str, help="Domains to test, with : seperated (for example google.com:youtube.com:amazon.com ...")
args = parser.parse_args()

serverString = args.dns_servers
dnsServer = serverString.split(":")
if args.domains != None:
    domains = args.domains.split(":")

for i in dnsServer:
    for j in domains:
        try:
            DNSResolver = dns.resolver.Resolver()
            DNSResolver.nameservers = [i]
            DNSResolver.query(j)
        except Exception:
            print(colorama.Back.RED+"DNS Server timeout. Exiting program..."+colorama.Style.RESET_ALL)
            sys.exit()
        

times = []
servers = []

for e in range(anzahldurchlaeufe):
    for i in dnsServer:
        for j in domains:
            avg = 0
            try:
                resolv = dns.resolver.Resolver()
                resolv.nameservers = [i]
                start = time.time()
                res = resolv.query(j)
                stop = time.time()
                avg = avg + (stop-start)
            except Exception as e:
                avg = avg + 1000
        avg = avg / len(domains)
        times.append(avg)
        servers.append(i)
        print(i + "   -   "+str(avg))
    if anzahldurchlaeufe > 1:
        print("Test "+str(e+1)+" Completed")

minimal = min(times)
for i in range(len(servers)):
    if times[i] == minimal:
        print("\nDu solltest " + servers[i] + " als DNS-Server bunutzen.")

print("\nProcess finished")

sys.exit()