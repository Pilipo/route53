import route53tools

# Load and verify config
route53tools.loadconfig()

# Load the cached IP
cachedip = route53tools.cachedip.get()

# Grab the external IP
externalip = route53tools.externalip.get()

# Grab and compare the DNS IP
dnsip = route53tools.dnsip.get()

if externalip == dnsip:

    if cachedip == externalip:

        route53tools.logger.log("IPs match " + externalip)
        exit()

    else:

        # cache mismatch
        route53tools.logger.log("External IPs match " + externalip + ". Cache needs an update.")
        route53tools.cachedip.update(externalip)
        exit()

recordset = route53tools.updater.update(externalip)

route53tools.cachedip.update(externalip)