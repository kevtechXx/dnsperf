#DNS Performance Test Script

#Voraussetzungen:
#python 3
#dnspython (pip install dnspython)

#Ausführen:
#python dnsperf.py (oder python <datei>.py)


#DNS-Server IPs (Einfach zur liste hinzufügen falls benötigt):
#1.1.1.1 | Cloudflare DNS
#8.8.8.8 | Google DNS
#9.9.9.9 | Quad9 | Filtert "böse" websites | DNSSEC
#198.101.242.72 | Alternate DNS | mit Adblock
#91.239.100.100 | Censurfridns
#209.59.210.167 | Christoph Hochstätter
#212.82.225.7 | ClaraNet
#8.26.56.26 | Comodo Secure DNS | blockt eventuell websites oder werbung, hab leider nix auf der website gefunden
#84.200.69.80 | DNS.Watch | DNSSEC
#104.236.210.29 | DNSReactor 
#87.118.100.175 | German Privacy Foundation e.V. | Verein löst sich auf, eventuell sind die server bald nicht mehr erreichbar

# ------------ config ------------ #
dnsServer = ["192.168.1.2", "1.1.1.1", "8.8.8.8", "9.9.9.9", "198.101.242.72", "91.239.100.100"] #DNS-Server die getestet werden sollen.

domains = ["google.com", "amazon.com", "facebook.com"] #Domains die von den DNS-Servern aufgelöst werden sollen.

anzahldurchlaeufe = 1 #anzahl von tests
# ------------ config ------------ #

import dns.resolver
import sys
import time

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
        print(i + "   -   "+str(avg*1000)+" ms")
    if anzahldurchlaeufe > 1:
        print("Test "+str(e+1)+" Completed")

minimal = min(times)
for i in range(len(servers)):
    if times[i] == minimal:
        print("\nDu solltest " + servers[i] + " als DNS-Server benutzen.")

print("\nProcess finished")

sys.exit()