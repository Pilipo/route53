# route53
Dynamically updates route53 A records to point to your home IP based on a scheduled cron job.

## Setup

1. **Setup AWS CLI Tools** ( _http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html_ )
    + Setup an AWS account and get Security Credentials
    + From command line, execute: ```apt install pip```
    + From command line, execute: ```pip install --upgrade --user awscli```
    + From command line, execute: ```aws configure``` (_You will need your ID, Key, and Region from AWS_)
    + From command line, install the composer requirements in the ```php``` directory. (Note: this requires Composer) 
2. **Copy and Configure ```config.sh```**
    + Copy ```sample.config.sh``` and rename to ```config.sh```
    + Update the ZONEID and RECORDSET variables in ```config.sh``` to your Route53 values
3. **Test the Script**
    + Verify that ```route53.sh``` is executable 
    + Execute ```./route53.sh```
    + Inspect the ```.ip``` and ```.log``` files to verify success
4. **Set the Cron**
    + Execute ```crontab -e``` 
    + Add ```0       *       *       *       *       /home/pi/Scripts/route53/route53.sh``` to the end. (_this refreshes once an hour_)