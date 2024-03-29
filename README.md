<a href="https://www.sparkpost.com"><img src="https://cdn.sanity.io/images/w7rshig9/production/25bc256b66274cdbafaade72a411b17058348216-496x129.svg?dl=SparkPost_Logo_DefaultDefault.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?plan=free-0817?src=Social%20Media&sfdcid=70160000000pqBb&pc=GitHubSignUp&utm_source=github&utm_medium=social-media&utm_campaign=github&utm_content=sign-up) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

# sparkyEvents (new)
[![Python application](https://github.com/tuck1s/sparkyEvents/actions/workflows/python-app.yml/badge.svg)](https://github.com/tuck1s/sparkyEvents/actions/workflows/python-app.yml)


Command-line tool to retrieve SparkPost message events in `.CSV` format.

## Recent changes

|Version|Date|Description
|--|--|--|
0.2.1|Mar 2021|Add `mailbox_providers` and `mailbox_provider_regions`
0.2.0|Dec 2020|Command-line options changed. Now supports all API event search parameters. Output to file or stdout. Show possible event types / properties from your SparkPost account
0.1.0|Nov 2019|New Events Search API


## Easy installation

Firstly ensure you have `python3`, `pip` and `git`.

Next, get the project. Install `pipenv` (`--user` option recommended, [see this article](https://stackoverflow.com/questions/42988977/what-is-the-purpose-pip-install-user)) and [this article for MacOS](https://stackoverflow.com/questions/60004431/pip-error-when-trying-to-run-pip-command-from-virtualenv-on-macos).

Once you have `pipenv`, you can use it to install the project dependencies.
```
git clone https://github.com/tuck1s/sparkyEvents.git
cd sparkyEvents
pip install --user pipenv
pipenv install
pipenv shell
```
_Note: In the above commands, you may need to run `pip3` instead of `pip`._

`./sparkyEvents.py -h` for usage info. Flags are named as per the events search parameters in the [Events API documentation](https://developers.sparkpost.com/api/events/#events).

## Pre-requisites
Set up the `sparkpost.ini` file as per the example.

Replace `<YOUR API KEY>` with your specific, private API key. The key needs the "**Events Search: Read Only**" permission.

`Host` is only needed for SparkPost EU, or for legacy Enterprise services with specific URLs. You can omit for [sparkpost.com](https://www.sparkpost.com/).

`Properties` can be any of the [SparkPost Event Properties](https://developers.sparkpost.com/api/events/#header-event-types). Definition can be split over lines using indentation, as per [Python .ini file structure](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure).

## Examples

The syntax for specifying time ranges has changed, and takes times in UTC only, in line with the API docs.

`--from` is *inclusive* and `--to` is *exclusive* (see [API definition](https://developers.sparkpost.com/api/events/#events-get-search-for-message-events)).

The following example fetches events for the December 2020 Gmail outage.

```
./sparkyEvents.py -o out6.csv --from 2020-12-14T22:00:00Z --to 2020-12-16T00:00:00Z --events bounce,out_of_band --bounce_classes 10 --reasons gsmtp
Writing to out6.csv
from                     2020-12-14T22:00:00Z
to                       2020-12-16T00:00:00Z
events                   bounce
bounce_classes           10
reasons                  gsmtp
Properties:  ['timestamp', 'raw_rcpt_to', 'subaccount_id']
Total events to fetch:  824
Page      1: got    824 events in 1.290 seconds
```

The progress messages are printed to `stderr` so you can pipe the actual output somewhere, e.g. to [csvkit](https://csvkit.readthedocs.io/) tools.

## Parameters that support keyword searching

Some parameters support keyword searching. For keyword searches with whitespace, enclose your values in quotes, e.g.
```
./sparkyEvents.py out.csv --subjects "cool cats, hot dogs"
```

## Event Properties and Event Types
The following special options do not actually fetch events; they show what's available from your SparkPost service.

```
./sparkyEvents.py --show_properties
```
```
ab_test_id,ab_test_version,amp_enabled,bounce_class,campaign_id,click_tracking,customer_id,delv_method,device_token,display_name,dr_latency,error_code,event_description,event_id,fbtype,friendly_from,geo_ip,initial_pixel,injection_time,ip_address,ip_pool,mailbox_provider,mailbox_provider_region,mailfrom,message_id,msg_from,msg_size,num_retries,open_tracking,outbound_tls,queue_time,raw_rcpt_to,raw_reason,rcpt_hash,rcpt_meta,rcpt_subs,rcpt_tags,rcpt_to,rcpt_type,reason,recipient_domain,recv_method,remote_addr,report_by,report_to,routing_domain,scheduled_time,sending_domain,sending_ip,sms_coding,sms_dst,sms_dst_npi,sms_dst_ton,sms_remoteids,sms_segments,sms_src,sms_src_npi,sms_src_ton,sms_text,stat_state,stat_type,subaccount_id,subject,target_link_name,target_link_url,template_id,template_version,timestamp,transactional,transmission_id,type,user_agent
```

```
./sparkyEvents.py --show_types
```
```
amp_click,amp_initial_open,amp_open,bounce,click,delay,delivery,generation_failure,generation_rejection,initial_open,injection,link_unsubscribe,list_unsubscribe,open,out_of_band,policy_rejection,sms_status,spam_complaint
```


## See Also
[SparkPost Developer Hub](https://developers.sparkpost.com/)

[SparkPost Event Types](https://developers.sparkpost.com/api/events/#header-event-types)

[SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/)

