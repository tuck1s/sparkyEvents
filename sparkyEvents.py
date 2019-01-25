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

T = 60                  # Global timeout value for API requests

def printHelp():
    progName = sys.argv[0]
    shortProgName = os.path.basename(progName)
    print('\nNAME')
    print('   ' + progName)
    print('   Simple command-line tool to retrieve SparkPost message events into a .CSV file.\n')
    print('SYNOPSIS')
    print('  ./' + shortProgName + ' outfile.csv from_time to_time\n')
    print('MANDATORY PARAMETERS')
    print('    outfile.csv     output filename, must be writeable. Records included are specified in the .ini file.')
    print('    from_time')
    print('    to_time         Format YYYY-MM-DDTHH:MM')
    print('')

# Validate SparkPost message-events start_time format, which is just to 1 minute resolution without timezone offset.
def isExpectedEventDateTimeFormat(timestamp):
    format_string = '%Y-%m-%dT%H:%M'
    try:
        datetime.strptime(timestamp, format_string)
        return True
    except ValueError:
        return False

def getMessageEvents(url, apiKey, params):
    try:
        h = {'Authorization': apiKey, 'Accept': 'application/json'}

        moreToDo = True
        while moreToDo:
            response = requests.get(url, timeout=T, headers=h, params=params)

            # Handle possible 'too many requests' error inside this module
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                if response.json()['errors'][0]['message'] == 'Too many requests':
                    snooze = 120
                    print('.. pausing', snooze, 'seconds for rate-limiting')
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

properties = cfg.get('Properties', 'timestamp,type')        # If the fields are not specified, default to a basic few
properties = properties.replace('\r', '').replace('\n', '') # Strip newline and CR
fList = properties.split(',')

timeZone = cfg.get('Timezone', 'UTC')         # If not specified, default to UTC

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

        fh = csv.DictWriter(outfile, fieldnames=fList, restval='', extrasaction='ignore')
        fh.writeheader()
        print('SparkPost events from ' + fromTime + ' to ' + toTime + ' ' + timeZone + ' to', outFname)
        print('Events:     ', events if events else '<all>')
        print('Properties: ', fList)
        morePages = True;
        eventPage = 1
        url = baseUri + '/api/v1/events/message'
        p = {
            'cursor': 'initial',
            'per_page': 10000,
            'from': fromTime,
            'to': toTime,
            'timezone': timeZone
        }
        if events:
            p['events'] = events

        while morePages:
            startT = time.time()                        # Measure time for each processing iteration
            res = getMessageEvents(url=url, apiKey=apiKey, params=p)
            if not res:                                 # Unexpected error - quit
                exit(1)
            for i in res['results']:
                fh.writerow(i)                          # Write out results as CSV rows in the output file
            endT = time.time()

            if eventPage == 1:
                print('Total events to fetch: ', res['total_count'])
            print('Page {0:6d}: got {1:6d} events in {2:2.3f} seconds'.format(eventPage, len(res['results']), endT - startT) )

            # Get the links from the response.  If there is a 'next' link, we continue processing
            if 'links' in res and 'next' in res['links']:
                eventPage+=1
                url = baseUri + res['links']['next']
                p = None                                 # All new params are in the returned "next" url
            else:
                morePages = False
else:
    printHelp()