import route53tools
import os

# Check on pending status change in AWS
if route53tools.updater.update_pending():
    exit()

print('no change lock. Attemping to run script')

# Load and verify config
route53tools.loadconfig()

# Load the cached IP
cachedip = route53tools.cachedip.get()

# Grab the external IP
externalip = route53tools.externalip.get()

# Grab and compare the DNS IP
dnsip = route53tools.dnsip.get()

# TODO: while dns is propagating, this DNS IP check comes back without a host. I need to check AWS records for correct ip at hostname. 
# This will protect against spamming AWS for record upsert requests.

if externalip == dnsip:

    if cachedip == externalip:

        route53tools.logger.log("IPs match " + externalip)
        exit()

    else:

        # cache mismatch
        route53tools.logger.log("External IPs match " + externalip + ", but cache needs an update.")
        route53tools.cachedip.update(externalip)
        exit()
else:
    route53tools.updater.update(externalip)