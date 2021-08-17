import csv
import json

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

from api import settings
from api.packages import vmanage


def run(report_date=None, tzinfo="Asia/Bangkok"):
    auth = vmanage.Authentication()
    api = vmanage.API()

    path = "/statistics/interface/aggregation"

    if not report_date:
        today = date.today()
    else:
        today = report_date

    tz = ZoneInfo(tzinfo)
    d2 = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=tz)
    d1 = d2 - timedelta(days=1)
    d2_utc = (d2 - d2.utcoffset()).replace(tzinfo=timezone.utc)
    d1_utc = d2_utc - timedelta(days=1)

    payload = json.dumps({
      "query": {
        "condition": "AND",
        "rules": [
            {
                "value": [
                    d1_utc.strftime("%Y-%m-%dT%H:00:00 UTC"), # startdate
                    d2_utc.strftime("%Y-%m-%dT%H:00:00 UTC")  # enddate
                ],
                "field": "entry_time",
                "type": "date",
                "operator": "between"
            },
            {
                "value": [
                    "ge0/1",
                    "ge0/2"
                ],
                "field": "interface",
                "type": "string",
                "operator": "in"
            }]
        },
        "aggregation": {
            "field": [
                {
                    "property": "vmanage_system_ip",
                    "sequence": 1
                },
                {
                    "property": "host_name",
                    "sequence": 2
                },
                {
                    "property": "interface",
                    "sequence": 3
                }
            ],
            "metrics": [
                {
                    "property": "rx_kbps",
                    "type": "max"
                },
                {
                    "property": "rx_octets",
                    "type": "sum"
                },
                {
                    "property": "tx_kbps",
                    "type": "max"
                },
                {
                    "property": "tx_octets",
                    "type": "sum"
                }
            ]
        }
    })

    response = api.send_request("POST", path, auth.headers, payload)

    # debug output
    # print(json.dumps(response, indent=4))
    
    file_path = Path.joinpath(settings.BASE_DIR, "api1/csv")
    file_name = "api1-{}.csv".format(d2.strftime("%Y-%m-%d"))
    full_path = Path(file_path, file_name)

    with open(full_path,  'w', newline='', encoding='utf-8') as output:  
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['system-ip', 'hostname', 'interface', 'max_rx_kbps', 'sum_rx_octets', 'max_tx_kbps', 'sum_tx_octets', 'sample', 'start_datetime', 'end_datetime'])
        for row in response['data']:
            writer.writerow([row['vmanage_system_ip'], row['host_name'], row['interface'], row['rx_kbps'], row['rx_octets'], row['rx_kbps'], row['tx_octets'], row['count'], d1, d2])
