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
        
class wanip:
    def get():
        from requests import get

        try:
            ip = get(('https://api.ipify.org')).content.decode('utf8')

            return ip
        except ValueError:
            return False

class awsip:
    def get():
        import boto3
        ip = False

        r53 = boto3.client('route53')
        response = r53.list_resource_record_sets(
            HostedZoneId=config['ROUTE53']['zoneid'],
            StartRecordName=config['ROUTE53']['recordset'],
            StartRecordType='A',
        )
        
        for v in response['ResourceRecordSets']:
            if v['Name'] == config['ROUTE53']['recordset'] + '.':
                ip = v['ResourceRecords'][0]['Value']

        return ip
                
class dnsip:
    def get():
        import socket

        hostname = config.get("ROUTE53","recordset")

        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except socket.gaierror as er:
            logger.log("Host not found: " + er.strerror)
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
    def is_update_pending():
        import boto3
        import os

        if os.path.exists('change.pending'):
            f = open('change.pending', 'r')
            id = f.read()
            f.close()

            r53 = boto3.client('route53')
            response = r53.get_change(
                Id=id
            )
            logger.log('Change pending: ' + str(response))
            if response['ChangeInfo']['Status'] == 'INSYNC':
                os.remove('change.pending')
                return False
            
            return True
    
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

        if response['ChangeInfo']['Status'] == 'PENDING':
            # set an update lock by creating a file
            file = open('change.pending', 'a')
            file.write(response['ChangeInfo']['Id'])
            file.close()

        cachedip.update(newip)

        # TODO: add alert mechanism

        # return the result
        return response