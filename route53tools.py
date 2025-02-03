import configparser

global config 

def loadconfig():
    try:
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

        try:
            ip = socket.gethostbyname('google.com')
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
    def buildrecordset():
        # Build dns recordset for AWS
        return

    def upsertrecordset():
        # Send dns recordset upsert to AWS
        return