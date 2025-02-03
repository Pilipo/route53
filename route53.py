from requests import get
import ipaddress

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True;
    except ValueError:
        return False;

# Start logs and IP records

# Grab the external IP
ip = get('https://api.ipify.org').content.decode('utf8')
print("Hello world!")
print('My public IP address is: {}'.format(ip))

# Check if the external IP is valid
if is_valid_ip(ip):
    print('IP is valid!')

    # Grab the IP provided by DNS

    # Check if IP has changed by comparing cached IP, current IP, and DNS record

    # NOT changed, log date and IP; ELSE continue

    # Update route53 recordset 

    # Log the change and send alert (email, text, whatever)

    # Overwrite IP cache with new IP

else:
    # NOT valid, log result and bail out
    print('IP is not valid! This will be logged')