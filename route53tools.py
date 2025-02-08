def loadconfig():
    import configparser

    try:
        global config 
        config = configparser.ConfigParser()
        config.read('config.ini')
    except ValueError:
        exit()

class cachedip:
    def get():
        import os
        try:
            if os.path.exists('.ip'):
                file = open('.ip','r')
                ip = file.read()
                file.close()
                if ip:
                    return ip
                else:
                    return False
            else:
                return False
        except ValueError:
            return False
        
    def update(ip):
        try:
            file = open('.ip', 'w')
            file.write(ip)
            file.close()
            logger.log('Cached new IP: ' + ip)
        except ValueError:
            return False
        
class externalip:
    def get():
        from requests import get

        try:
            ip = get(('https://api.ipify.org')).content.decode('utf8')

            return ip
        except ValueError:
            return False

class dnsip:
    def get():
        import socket

        hostname = config.get("ROUTE53","recordset")

        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except ValueError:
            logger.log("Caution: hostname did not return ip.")
            return False
        
class logger:
    def log(msg):
        import datetime
        
        try:
            now = datetime.datetime.now()
            ts = now.strftime("%Y-%m-%d %H:%M:%S")
            file = open('R53.log', 'a+')
            file.write(str(ts) + ' : ' + msg + '\n')
            file.close()
        except ValueError:
            return False

class notifier:
    def email(recipient, msg):
        try:
            print('Notifying: "' + msg + '" to  ' + recipient)
        except ValueError:
            return False

class updater:
    def update(newip):
        import boto3

        # get the config values
        zoneid = config.get('ROUTE53','zoneid')
        comment = "this is a comment about record set updates"
        recordset = config.get('ROUTE53','recordset')
        type = config.get('ADVANCED','type')
        ttl = config.getint('ADVANCED','ttl')

        # build the payload
        payload = {
            "Comment":comment,
            "Changes":[
                {
                    "Action":"UPSERT",
                    "ResourceRecordSet":{
                        "ResourceRecords":[
                            {
                                "Value":newip
                            }
                        ],
                    "Name":recordset,
                    "Type":type,
                    "TTL":ttl
                    }
                }
            ]
        }

        # make the upsert
        r53 = boto3.client('route53')
        response = r53.change_resource_record_sets(
            HostedZoneId=zoneid,
            ChangeBatch=payload
        )

        # log the result
        logger.log(str(response))

        # return the result
        return response