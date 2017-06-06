#!/usr/bin/env python3
#
#Copyright  2017 SparkPost
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#
# Author: Steve Tuck (June 2017)
#

from __future__ import print_function
from sparkpost import SparkPost
from datetime import datetime,timedelta
from sparkpost.exceptions import SparkPostAPIException
import configparser, time, json, sys, os, csv

def printHelp():
    progName = sys.argv[0]
    shortProgName = os.path.basename(progName)
    print('\nNAME')
    print('   ' + progName)

# Validate SparkPost start_time format, slightly different to Python datetime (which has no : in timezone offset format specifier)
def isExpectedDateTimeFormat(timestamp):
    format_string = '%Y-%m-%dT%H:%M:%S%z'
    try:
        colon = timestamp[-3]
        if not colon == ':':
            raise ValueError()
        colonless_timestamp = timestamp[:-3] + timestamp[-2:]
        datetime.strptime(colonless_timestamp, format_string)
        return True
    except ValueError:
        return False

from sparkpost.base import Resource

class MessageEvents(Resource):
        key = "api/v1/message-events"

        def list(self, **kwargs):
            results = self.request('GET', self.uri, **kwargs)
            return results


# -----------------------------------------------------------------------------------------
# Main code
# -----------------------------------------------------------------------------------------
# Get parameters from .ini file
configFile = 'sparkpost.ini'
config = configparser.ConfigParser()
config.read_file(open(configFile))
cfg = config['SparkPost']
apiKey = cfg.get('Authorization', '')           # API key is mandatory
if not apiKey:
    print('Error: missing Authorization line in ' + configFile)
    exit(1)
baseUri = 'https://' + cfg.get('Host', 'api.sparkpost.com')     # optional, default to public service

# Check list-type and argument count
if len(sys.argv) < 2:
    printHelp()
    exit(0)

else:
    # Open the adapter towards SparkPost
    me = MessageEvents(api_key = apiKey, base_uri = baseUri)
    print('Opened connection to', baseUri)
    p = {
        'events': 'bounce',
        'page': 1,
        'per_page': 100
    }
    e = me.list( params=p)
    print(json.dumps(e, indent=4))


