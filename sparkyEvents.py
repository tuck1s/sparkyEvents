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
from datetime import datetime,timedelta
import configparser, time, json, sys, os, csv, requests

T = 20                  # Global timeout value for API requests

def printHelp():
    progName = sys.argv[0]
    shortProgName = os.path.basename(progName)
    print('\nNAME')
    print('   ' + progName)

# Validate SparkPost message-events start_time format, which is just to 1 minute resolution without timezone offset.
def isExpectedEventDateTimeFormat(timestamp):
    format_string = '%Y-%m-%dT%H:%M'
    try:
        datetime.strptime(timestamp, format_string)
        return True
    except ValueError:
        return False

def getMessageEvents(uri, apiKey, params):
    try:
        path = uri + '/api/v1/message-events'
        h = {'Authorization': apiKey, 'Accept': 'application/json'}

        moreToDo = True
        while moreToDo:
            response = requests.get(path, timeout=T, headers=h, params=params)

            # Handle possible 'too many requests' error inside this module
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                if response.json()['errors'][0]['message'] == 'Too many requests':
                    snooze = 30
                    print('.. pausing', snooze, 'seconds for rate-liming')
                    time.sleep(snooze)
                    continue                # try again
            else:
                print('Error:', response.status_code, ':', response.text)
                return None

    except ConnectionError as err:
        print('error code', err.status_code)
        exit(1)

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
baseUri = 'https://' + cfg.get('Host', 'api.sparkpost.com')

events = cfg.get('Events', '')                  # If events are not specified, defaults to all

attributes = cfg.get('Attributes', 'timestamp,type')     # if the fields are not specified, default to a basic few.  Strip newline and CR
attributes = attributes.replace('\r', '').replace('\n', '')

fList = attributes.split(',')

if len(sys.argv) >= 4:
    outFname = sys.argv[1]
    with open(outFname, 'w', newline='') as outfile:
        fromTime = sys.argv[2];
        if not(isExpectedEventDateTimeFormat(fromTime)):
            print('Error: unrecognised fromTime:',fromTime)
            exit(1)
        toTime = sys.argv[3];
        if not(isExpectedEventDateTimeFormat(toTime)):
            print('Error: unrecognised toTime:',toTime)
            exit(1)

        firstPass = True;
        morePages = True;
        eventPage = 1
        while morePages:
            startT = time.time()                        # Measure time for each processing iteration

            p = {
                'page': eventPage,
                'per_page': 10000,
                'from': fromTime,
                'to': toTime,
                'timezone': 'UTC'
            }
            if events:
                p['events'] = events
            res = getMessageEvents(uri = baseUri, apiKey=apiKey, params= p)

            if not res:                                 # No result - unexpected error
                exit(1)

            if firstPass:
                fh = csv.DictWriter(outfile, fieldnames = fList, restval='')
                fh.writeheader()
                startT = time.time()
                print('Collecting events from '+fromTime+' to '+toTime+' :',res['total_count'])
                firstPass=False

            # Write out results as CSV rows in the output file
            for i in res['results']:
                if 'tdate' in i:
                    pass #print(json.dumps(i))
                fh.writerow(i)

            endT = time.time()
            print(outFname, 'page:',eventPage,':',len(res['results']), 'events written in', round(endT - startT, 3), 'seconds')

            # Get the links.  If there is no 'next' link, we've reached the end.
            morePages = False
            for l in res['links']:
                if l['rel'] == 'next':
                    eventPage+=1
                    morePages=True
                elif l['rel'] == 'last' or l['rel'] == 'first' or l['rel'] == 'previous':
                    pass
                else:
                    print(json.dumps(l))

        # Done all pages now
else:
    printHelp()