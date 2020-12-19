<a href="https://www.sparkpost.com"><img src="https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?plan=free-0817?src=Social%20Media&sfdcid=70160000000pqBb&pc=GitHubSignUp&utm_source=github&utm_medium=social-media&utm_campaign=github&utm_content=sign-up) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

# sparkyEvents (new)
[![Build Status](https://travis-ci.com/tuck1s/sparkyEvents.svg?branch=master)](https://travis-ci.com/tuck1s/sparkyEvents)

Simple command-line tool to retrieve SparkPost message events into a .CSV file.

> Dec 2020: Command-line options have changed! Now supports all event search parameters.

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

`./sparkyEvents.py -h` for usage info. Flags mirror the events search parameters in the [Events API documentation](https://developers.sparkpost.com/api/events/#events).

## Pre-requisites
Set up the `sparkpost.ini` file as per the example.

Replace `<YOUR API KEY>` with your specific, private API key. The key needs the "**Events Search: Read Only**" permission.

`Host` is only needed for SparkPost EU, or for legacy Enterprise services with specific URLs. You can omit for [sparkpost.com](https://www.sparkpost.com/).

`Properties` can be any of the [SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/). Definition can be split over lines
using indentation, as per [Python .ini file structure](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure).

## Examples

The syntax for specifying time ranges has changed, and takes times in UTC only, in line with the API docs.

`--from` is *inclusive* and `--to` is *exclusive* (see [API definition](https://developers.sparkpost.com/api/events/#events-get-search-for-message-events)).

The following example fetches events for the December 2020 Gmail outage.

```
./sparkyEvents.py out6.csv --from 2020-12-14T22:00:00Z --to 2020-12-16T00:00:00Z --events bounce --bounce_classes 10 --reasons gsmtp
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

## See Also
[SparkPost Developer Hub](https://developers.sparkpost.com/)

[SparkPost Event Types](https://developers.sparkpost.com/api/events/#header-event-types)

[SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/)

