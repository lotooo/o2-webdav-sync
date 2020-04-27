#!/usr/bin/env python
import requests
import json
import caldav
import sys
import os
from datetime import datetime,timedelta

calendar_url = "https://%s:%s@%s" % (
    os.environ.get('WEBDAV_USER'), 
    os.environ.get('WEBDAV_PASS'),
    os.environ.get('WEBDAV_URL')
)

url = "https://client.o2.fr/wp-admin/admin-ajax.php"
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Origin" : "https://client.o2.fr",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.7,fr;q=0.3",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

vcal_date_format = "%Y%m%dT%H%M%S"

vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:%s
DTSTAMP:%s
DTSTART:%s
DTEND:%s
SUMMARY:%s
END:VEVENT
END:VCALENDAR
"""

s = requests.Session()
r1 = s.post(url, data={"action":"ask_login","login": os.environ.get('O2_USER'),"pwd":os.environ.get('O2_PASS')}, headers=headers)
extract_start = 1000 * int((datetime.now()-timedelta(days=7)).timestamp())
extract_end = 1000 * int((datetime.now()+timedelta(days=7)).timestamp())

r2 = s.post(url, data={"action":"get_planning_events", "startDate": str(extract_start), "endDate": str(extract_end)}, headers=headers)

client = caldav.DAVClient(calendar_url)
principal = client.principal()
calendars = principal.calendars()

if len(calendars) > 0:
    for c in calendars:
        if os.environ.get('WEBDAV_CAL') in str(c):
            calendar = c
else:
    logging.error("No calendar found")
    sys.exit(1)

for event in r2.json():
    start = datetime.fromtimestamp(event['eventStart'] / 1000)
    end = datetime.fromtimestamp((event['eventStart']+event['eventPlanDur']) /1000)
    summary = "%s - %s %s %s" % (event['hsType'].capitalize(), event['civility'].capitalize(), event['firstName'], event['lastName'])
    if "annul" in event['eventStatus']:
        summary = "(Annulé) %s" % summary
    myvcal = vcal % (event['eventId'], datetime.now().strftime(vcal_date_format), start.strftime(vcal_date_format), end.strftime(vcal_date_format), summary)
    e = calendar.add_event(myvcal)
    print(e)

