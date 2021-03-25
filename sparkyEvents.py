#!/usr/bin/env python3
from __future__ import print_function
import configparser, argparse, time, csv, requests, sys

def kwdStr(s):
    """
    SparkPost params with keyword search. In fact argparse strips surrounding quotes, and requests encodes spaces in query params, so nothing do do!
    """
    return s


def getMessageEvents(url, apiKey, params):
    """
    Get SparkPost message events with specified endpoint URL, API Key, and search params.
    """
    try:
        T = 60  # Reasonable timeout value for API requests
        h = {'Authorization': apiKey, 'Accept': 'application/json'}

        moreToDo = True
        while moreToDo:
            response = requests.get(url, timeout=T, headers=h, params=params)

            # Handle possible 'too many requests' error inside this module
            if response.status_code == 200:
                return response.json()
            elif (response.status_code == 429 and response.json()['errors'][0]['message'] == 'Too many requests') or \
                 (response.status_code == 502 and response.json()['errors'][0]['message'] == 'Could not proceed (502 error)'):
                snooze = 30
                eprint(response.json(),
                      '.. pausing {} seconds for rate-limiting'.format(snooze))
                time.sleep(snooze)
                continue                # try again
            else:
                eprint('Error:', response.status_code, ':', response.text)
                return None

    except ConnectionError as err:
        eprint('error code', err)
        exit(1)


def showDocs(url, types=False):
    """
    List available event properties and types
    """
    response = requests.request("GET", url, headers={'Accept': 'application/json'})
    properties = set()
    for i in response.json()['results']:
        if types:
            properties.add(i.get('type').get('sampleValue')) # accumulate all the event types
        else:
            for k, v in i.items():
                properties.add(k) # accumulate all the properties reported across all event types
    return sorted(properties)


def eprint(*args, **kwargs):
    """
    Print to stderr - see https://stackoverflow.com/a/14981125/8545455
    """
    print(*args, file=sys.stderr, **kwargs)


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
    eprint('Error: missing Authorization line in ' + configFile)
    exit(1)
baseUrl = 'https://' + cfg.get('Host', 'api.sparkpost.com')

# If the fields are not specified, default to a basic few
properties = cfg.get('Properties', 'timestamp,type')
fList = properties.replace('\r', '').replace('\n', '').split(',')  # Strip newline and CR

# Offer all the API query parameters as command-line arguments (name, type-check function, help text)
parser = argparse.ArgumentParser(
    description='Simple command-line tool to retrieve SparkPost message events into a .CSV file.',
    epilog='For keyword searches with whitespace, enclose your values in quotes, e.g. --reasons "gsmtp,ripe avocados". SparkPost API key, host, and properties are specified in {}.'.format(configFile))
in1 = parser.add_argument_group()
in1.add_argument('-o', '--outfile', metavar='outfile.csv', type=argparse.FileType('w'), default='-', help='output filename (CSV format), must be writeable. If omitted, prints to stdout.')
# See: https://developers.sparkpost.com/api/events/#events. cursor and per_page are filled in by this tool
in1.add_argument('--from', type=str, help='Datetime in format of YYYY-MM-DDTHH:MM:ssZ, inclusive. Value should be in UTC. If omitted, defaults to "24 hours ago"')
in1.add_argument('--to', type=str, action='store',help='Datetime in format of YYYY-MM-DDTHH:MM:ssZ, exclusive. Value should be in UTC. If omitted, defaults to "1 minute ago"')
in1.add_argument('--delimiter', type=str, help='string, if omitted default is ,')
in1.add_argument('--event_ids', type=str, help='Comma delimited list of event IDs to search')
in1.add_argument('--events', type=str, help='Comma delimited list of event types to search')
in1.add_argument('--recipients', type=str, help='Comma delimited list of recipients to search')
in1.add_argument('--recipient_domains', type=kwdStr, help='Comma delimited list of recipient domains to search. Supports keyword searching by domain segment')
in1.add_argument('--from_addresses', type=str, help='Comma delimited list of friendly from addresses to search')
in1.add_argument('--sending_domains', type=kwdStr, help='Comma delimited list of sending domains to search. Supports keyword searching by domain segment')
in1.add_argument('--subjects', type=kwdStr, help='Comma delimited list of subject lines from the email header to search. Supports keyword searching')
in1.add_argument('--bounce_classes', type=str, help='Comma delimited list of bounce classification codes to search. See Bounce Classification Codes')
in1.add_argument('--reasons', type=kwdStr, help='Comma delimited list of Bounce/failure/rejection reason to search. Supports keyword searching')
in1.add_argument('--campaigns', type=kwdStr, help='Comma delimited list of campaign IDs to search. Supports keyword searching')
in1.add_argument('--templates', type=kwdStr, help='Comma delimited list of template IDs to search. Supports keyword searching')
in1.add_argument('--sending_ips', type=str, help='Comma delimited list of sending IP addresses to search')
in1.add_argument('--ip_pools', type=kwdStr, help='Comma delimited list of IP pool IDs to search. Supports keyword searching')
in1.add_argument('--subaccounts', type=str, help='Comma delimited list of subaccount IDs to search')
in1.add_argument('--messages', type=str, help='Comma delimited list of message IDs to search')
in1.add_argument('--transmissions', type=str, help='Comma delimited list of transmission IDs to search')
in1.add_argument('--mailbox_providers', type=kwdStr, help='Comma delimited list of mailbox providers to search. Supports keyword searching.')
in1.add_argument('--mailbox_provider_regions', type=kwdStr, help='Comma delimited list of mailbox provider regions to search. Supports keyword searching.')
in1.add_argument('--ab_tests', type=kwdStr, help='Comma delimited list of A/B test IDs to search. Supports keyword searching')
in1.add_argument('--ab_test_versions', type=str, help='Comma delimited list of version numbers of A/B tests to search. If provided, ab_tests parameter becomes required')
in2 = parser.add_argument_group('Special options')
in2.add_argument('--show_properties', action='store_true', help='List available event properties from your SparkPost service, then quit')
in2.add_argument('--show_types', action='store_true', help='List available event types from your SparkPost service, then quit')
p = vars(parser.parse_args()) # Use a dict, because 'from' is a Python reserved word and can't be accessed as an object member

if p['show_properties']:
    print(','.join(showDocs(baseUrl + '/api/v1/events/message/documentation')))
    exit(0)

if p['show_types']:
    print(','.join(showDocs(baseUrl + '/api/v1/events/message/documentation', types=True)))
    exit(0)

# Also allow old behavior of getting events list from config file, if user did not specify in command-line args
if not p['events']:
    events = cfg.get('Events', '')
    if events:
        p['events'] = events

# Write CSV file header
fh = csv.DictWriter(p['outfile'], fieldnames=fList, restval='', extrasaction='ignore')
fh.writeheader()
eprint('Writing to {}'.format(p['outfile'].name))
del p['outfile'] # don't pass this as an API parameter

# Build the API query parameters from command-line args that are set
qp = {
    'cursor': 'initial',
    'per_page': 10000,
}
for k, v in p.items():
    if v:
        eprint('{:24} {:24}'.format(k, str(v)))
        qp[k] = v

eprint('Properties: ', fList)
morePages = True
eventPage = 1
url = baseUrl + '/api/v1/events/message'

while morePages:
    # Measure time for each processing iteration
    startT = time.time()
    res = getMessageEvents(url=url, apiKey=apiKey, params=qp)
    if not res:                                 # Unexpected error - quit
        exit(1)
    for i in res['results']:
        # Write out results as CSV rows in the output file
        fh.writerow(i)
    endT = time.time()

    if eventPage == 1:
        eprint('Total events to fetch: ', res['total_count'])
    eprint('Page {0:6d}: got {1:6d} events in {2:2.3f} seconds'.format(eventPage, len(res['results']), endT - startT))

    # Get the links from the response.  If there is a 'next' link, continue processing
    if 'links' in res and 'next' in res['links']:
        eventPage += 1
        url = baseUrl + res['links']['next']
        qp = None                                # All new params are in the returned "next" url
    else:
        morePages = False
