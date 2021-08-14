from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

from api import settings
from api.packages import vmanage

import csv
import json
import os


def run():
  auth = vmanage.Authentication()
  api = vmanage.API()

  path = "/statistics/interface/aggregation"

  tz = ZoneInfo("Asia/Bangkok")
  d_now = datetime.now(tz=tz)
  d_now_utc = d_now - d_now.utcoffset()
  d2 = d_now_utc.strftime("%Y-%m-%dT%H:00:00 UTC")
  d1 = (d_now_utc - timedelta(days=1)).strftime("%Y-%m-%dT%H:00:00 UTC")

  payload = json.dumps({
    "query": {
      "condition": "AND",
      "rules": [
        {
          "value": [
            d1,
            d2
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
        }
      ]
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
  file_name = "api1-{}.csv".format(d_now.strftime("%Y-%m-%d"))
  full_path = Path(file_path, file_name)

  with open(full_path,  'w', newline='', encoding='utf-8') as output:  
      writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(['system-ip', 'hostname', 'interface', 'max_rx_kbps', 'sum_rx_octets', 'max_tx_kbps', 'sum_tx_octets', 'sample', 'start_datetime', 'end_datetime'])
      for row in response['data']:
          writer.writerow([row['vmanage_system_ip'], row['host_name'], row['interface'], row['rx_kbps'], row['rx_octets'], row['rx_kbps'], row['tx_octets'], row['count'], d1, d2])
