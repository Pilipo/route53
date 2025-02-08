# route53
Dynamically updates route53 A records to point to your home IP based on a scheduled cron job.

## Setup

1. **Verify Python**
    + ```Python -V```
1. **Setup AWS CLI Tools** ( _http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html_ )
    + Setup an AWS account and get Security Credentials
    + From command line, execute: ```apt install awscli```
    + From command line, execute: ```aws configure``` (_You will need ID, Key, and Region from AWS_)
        + It is strongly recommended that you set up an IAM user that is limited to route53 record updates. Further, it is strongly recommended that you do your reading on properly securing access to AWS resources as best practices change often.
1. **Copy and Configure ```config.ini```**
    + Rename ```config.ini.sample``` to ```config.ini```
    + Update the ZONEID (from Route53) and RECORDSET (the subdomain this script will be updating) variables in ```config.ini``` to your Route53 values