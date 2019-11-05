<a href="https://www.sparkpost.com"><img src="https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?plan=free-0817?src=Social%20Media&sfdcid=70160000000pqBb&pc=GitHubSignUp&utm_source=github&utm_medium=social-media&utm_campaign=github&utm_content=sign-up) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

# sparkyEvents
[![Build Status](https://travis-ci.org/tuck1s/sparkyEvents.svg?branch=master)](https://travis-ci.org/tuck1s/sparkyEvents)

Simple command-line tool to retrieve SparkPost message events into a .CSV file.


## Easy installation

Firstly ensure you have `python3`, `pip` and `git`.

Next, get the project. Install `pipenv` (`--user` option recommended, [see this article](https://stackoverflow.com/questions/42988977/what-is-the-purpose-pip-install-user)) and use this to install the project dependencies.
```
git clone https://github.com/tuck1s/sparkyEvents.git
cd sparkyEvents
pip install --user pipenv
pipenv install
pipenv shell
```
_Note: In the above commands, you may need to run `pip3` instead of `pip`._

You can now type `./sparkyEvents.py -h` and see usage info:

```
 ./sparkyEvents.py -h
usage: sparkyEvents.py [-h] outfile.csv from_time to_time

Simple command-line tool to retrieve SparkPost message events into a .CSV
file.

positional arguments:
  outfile.csv  output filename (CSV format), must be writeable.
  from_time    Datetime in format of YYYY-MM-DDTHH:MM:ssZ, inclusive.
  to_time      Datetime in format of YYYY-MM-DDTHH:MM:ssZ, exclusive.

optional arguments:
  -h, --help   show this help message and exit

SparkPost API key, host, record event type(s) and properties are specified in sparkpost.ini.
```

## Pre-requisites
Set up the `sparkpost.ini` file as follows.
  
```
[SparkPost]
Authorization = <YOUR API KEY>
Host = <your Enterprise host>

# Choose which events you want in the output file.  Omit, or leave blank, for all event types
Events = bounce,delivery,spam_complaint,out_of_band,policy_rejection,click,open,generation_failure,generation_rejection,list_unsubscribe,link_unsubscribe

# Choose which attributes you want in the output file
Properties = timestamp,type,
 bounce_class,campaign_id,customer_id,delv_method,device_token,dr_latency,error_code,event_id,
 fbtype,friendly_from,geo_ip,ip_address,ip_pool,mailfrom,message_id,msg_from,msg_size,num_retries,
 queue_time,raw_rcpt_to,
 raw_reason,rcpt_meta,rcpt_subs,rcpt_tags,rcpt_to,rcpt_type,reason,
 remote_addr,report_by,report_to,routing_domain, sending_ip,
 sms_coding,sms_dst,sms_dst_npi,sms_dst_ton,sms_remoteids,sms_segments,sms_src,sms_src_npi,sms_src_ton,sms_text,
 stat_state,stat_type,subaccount_id,subject,
 target_link_name,target_link_url,template_id,template_version,transmission_id,user_agent,user_str
```

Replace `<YOUR API KEY>` with your specific, private API key. 

`Host` is only needed for SparkPost Enterprise service usage; you can omit for [sparkpost.com](https://www.sparkpost.com/).

`Events` is a list, as per [SparkPost Event Types](https://developers.sparkpost.com/api/message-events.html#message-events-message-events-get); omit to select all.

`Properties` can be any of the [SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/). Definition can be split over lines 
using indentation, as per [Python .ini file structure](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure).

`Timezone` is no longer an .ini file option. Instead, specify timezone offset in your `from_time` and `to_time`.

## Examples

`from_time` is *inclusive* and `to_time` is *exclusive* (see [API definition](https://developers.sparkpost.com/api/events/#events-get-search-for-message-events)), so the following example fetches exactly one hour's worth of events:

`./sparkyEvents.py out3.csv 2019-11-05T08:00:00Z 2019-11-05T09:00:00Z`
```
Time ranges to search are in timezone UTC
SparkPost events from 2019-11-05 08:00:00+00:00 to 2019-11-05 09:00:00+00:00, writing to out3.csv
Events:      injection,bounce,delivery,spam_complaint,out_of_band,policy_rejection,click,open,generation_failure,generation_rejection,list_unsubscribe,link_unsubscribe
Properties:  ['timestamp', 'subaccount_id', 'friendly_from', 'raw_rcpt_to', 'subject']
Total events to fetch:  82248
:
:
```

Timezone follows ISO8601 format, is of the form `Z` (meaning UTC) or `HH:MM`.  fetches the same data as the first example, but using India timezone (5½ hours ahead of UTC)

`./sparkyEvents.py out3.csv 2019-11-05T13:30:00+05:30 2019-11-05T14:30:00+05:30`

```
Time ranges to search are in timezone UTC+05:30
SparkPost events from 2019-11-05 13:30:00+05:30 to 2019-11-05 14:30:00+05:30, writing to out3.csv
Events:      injection,bounce,delivery,spam_complaint,out_of_band,policy_rejection,click,open,generation_failure,generation_rejection,list_unsubscribe,link_unsubscribe
Properties:  ['timestamp', 'subaccount_id', 'friendly_from', 'raw_rcpt_to', 'subject']
Total events to fetch:  82248
```

Here is a search for the same data, but requesting in US Eastern time:

`./sparkyEvents.py out3.csv 2019-11-05T03:00:00-05:00 2019-11-05T04:00:00-05:00`

If the from_time and to_time timezones differ, you'll see a warning but the search proceeds:

` ./sparkyEvents.py out3.csv 2019-11-05T08:00:00Z 2019-11-05T14:30:00+05:30`

```
Warning: from_time and to_time are in different timezones UTC and UTC+05:30 - continuing
```

## See Also
[SparkPost Developer Hub](https://developers.sparkpost.com/)

[SparkPost Event Types](https://developers.sparkpost.com/api/events/#header-event-types)

[SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/)

