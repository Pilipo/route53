import route53tools

# Load and verify config
route53tools.loadconfig()

# Load the cached IP
cachedip = route53tools.cachedip.get()

# Grab the external IP
externalip = route53tools.externalip.get()

# Compare: mismatch assumes external IP has recently changed, so skip to update
if externalip == cachedip:
    
    # Grab and compare the DNS IP
    dnsip = route53tools.dnsip.get()

    # match assumes no work to do, so bail out
    if dnsip == externalip:
        route53tools.logger.log("IPs all match. Exiting.")
        exit()

recordset = route53tools.updater.buildrecordset()
status = True # route53tools.updater.upsertrecordset(recordset)

if status:
    # Update cache after pushing recordset
    route53tools.cachedip.update(externalip)