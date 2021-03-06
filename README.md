# threatstack-to-s3
Takes a Threat Stack web hook request and archives the alert to S3.

**NOTE: This code is provided as an example and without support for creating services that use Threat Stack webhooks to perform actions within an environment.**

## Setup
Setup will need to be performed for both this service and in Threat Stack.

Set the following environmental variables:
```
$ export TS_AWS_S3_BUCKET=<S3 bucket name>
$ export TS_AWS_S3_PREFIX=<key/directory prefix for storing data (optional)>
$ export THREATSTACK_API_KEY=<Threat Stack API key>
```

Create and initialize Python virtualenv using virtualenvwrapper
```
mkvirtualenv threatstack-to-s3
pip install -r requirements.txt
```

__NOTE:__ If Running on OS X you will need extra packages to work around issues with Python and SSL. OS X usage should be for development only.
```
pip install -r requirements.osx.txt
```

To launch the service:
```
gunicorn -c gunicorn.conf.py threatstack-to-s3
```

If performing debugging you may wish to run the app directly instead of via Gunicorn:
```
python threatstack-to-s3.py
```

The host running this service needs the following AWS IAM policy for S3 bucket access where *s3_bucket* is the name of the bucket set by TS_AWS_S3_BUCKET:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::<s3_bucket>"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:DeleteObject",
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<s3_bucket>/*"
            ]
        }
    ]
}
```

## S3 Layout
This service ingests a Threat Stack webhook document, stores each alert from the webhook, retrieves the detailed alert data from Threat Stack, and stores that information too.  Webhook data is stored by date.  Alert data is stored by alert ID.
```
aws s3 ls --recursive s3://<bucket>
2017-01-17 16:40:14      10367 alerts/58/7c/587c0159a907346eccb84004
2017-01-17 16:40:11       9590 alerts/58/7c/587c036efc22b55ac0b72837
2017-01-17 16:40:14        269 webhooks/2017/01/15/23/10/587c0159a907346eccb84004
2017-01-17 16:40:11        259 webhooks/2017/01/15/23/19/587c036efc22b55ac0b72837
```

## API
### POST https://_host_/api/v1/s3/alert
Post a JSON doc from Threat Stack and archive it to S3.  JSON doc will be in the following format.  __NOTE__: A webhook may contain multiple alerts but this service will store each one individually.
```
{
  "alerts": [
    {
      "id": "<alert ID>",
      "title": "<alert title / description>",
      "created_at": <time in milliseconds from epoch UTC>,
      "severity": <severity value>,
      "organization_id": "<alphanumeric organization ID>",
      "server_or_region": "<name of host in Threat Stack platform>",
      "source": "<source type>"
    }
  [
}
```
### GET https://_host_/api/v1/s3/alert
When provided both `start` and `end` form data in iso8601 format return the list of alerts data from that date range.

### GET https://_host_/api/v1/s3/alert/_alert_id_
Return the alert data for the given alert ID.

