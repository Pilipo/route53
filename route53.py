import route53tools
import os

# Check on pending status change in AWS
if route53tools.updater.is_update_pending():
    exit()

# Load and verify config
route53tools.loadconfig()

cached_ip = route53tools.cachedip.get()
wan_ip = route53tools.wanip.get()
dns_ip = route53tools.dnsip.get()
aws_ip = route53tools.awsip.get()

if cached_ip != wan_ip or cached_ip != aws_ip:
    route53tools.updater.update(wan_ip)
elif cached_ip != dns_ip:
    route53tools.logger.log('AWS matched WAN. Possibly waiting on DNS propagation.')