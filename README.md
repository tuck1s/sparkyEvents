<a href="https://www.sparkpost.com"><img src="https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?plan=free-0817?src=Social%20Media&sfdcid=70160000000pqBb&pc=GitHubSignUp&utm_source=github&utm_medium=social-media&utm_campaign=github&utm_content=sign-up) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

# sparkyEvents
[![Build Status](https://travis-ci.org/tuck1s/sparkyEvents.svg?branch=master)](https://travis-ci.org/tuck1s/sparkyEvents)

Simple command-line tool to retrieve SparkPost message events into a .CSV file.


## Easy installation

Firstly ensure you have `python3`, `pip` and `git`.

Next, get the project. Install `pipenv`, and use this to install the project dependencies.
```
git clone https://github.com/tuck1s/sparkyEvents.git
cd sparkyEvents
pip install pipenv
pipenv install
pipenv shell
```

You can now type `./sparkyEvents.py` and see usage info.

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
 
# Timezone that from_time and to_time queries apply to
Timezone = America/New_York
```
Replace `<YOUR API KEY>` with your specific, private API key. 

`Host` is only needed for SparkPost Enterprise service usage; you can omit for [sparkpost.com](https://www.sparkpost.com/).

`Events` is a list, as per [SparkPost Event Types](https://developers.sparkpost.com/api/message-events.html#message-events-message-events-get); omit to select all.

`Properties` can be any of the [SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/). Definition can be split over lines 
using indentation, as per [Python .ini file structure](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure).

`Timezone` can be configured to suit your locale. It's used by SparkPost to interpret the event time range `from_time` 
and `to_time` that you give in command-line parameters.
## Usage
```
$ ./sparkyEvents.py 

NAME
   ./sparkyEvents.py
   Simple command-line tool to retrieve SparkPost message events into a .CSV file.

SYNOPSIS
  ./sparkyEvents.py outfile.csv from_time to_time

MANDATORY PARAMETERS
    outfile.csv     output filename, must be writeable. Records included are specified in the .ini file.
    from_time
    to_time         Format YYYY-MM-DDTHH:MM
```

`from_time` and `to_time` are inclusive, so for example if you want a full day of events, use time T00:00 to T23:59.
## Example output
```
./sparkyEvents.py outfile.csv 2017-06-04T00:00 2017-06-04T23:59

SparkPost events from 2017-06-04T00:00 to 2017-06-04T23:59 America/New_York to outfile.csv
Events:      <all>
Properties:  ['timestamp', 'type', 'event_id', 'friendly_from', 'mailfrom', 'raw_rcpt_to', 'message_id', 'template_id', 'campaign_id', 'subaccount_id', 'subject', 'bounce_class', 'raw_reason', 'rcpt_meta', 'rcpt_tags']
Total events to fetch:  18537125
Page      1: got  10000 events in 5.958 seconds
Page      2: got  10000 events in 5.682 seconds
Page      3: got  10000 events in 5.438 seconds
Page      4: got  10000 events in 6.347 seconds
:
:
```

## See Also
[SparkPost Developer Hub](https://developers.sparkpost.com/)

[SparkPost Event Types](https://developers.sparkpost.com/api/message-events.html#message-events-message-events-get)

[SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/)

[Getting Started on SparkPost Enterprise](https://support.sparkpost.com/customer/portal/articles/2162798-getting-started-on-sparkpost-enterprise)

