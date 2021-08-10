import vmanage
import csv
import json
import requests

auth = vmanage.Authentication()
api = vmanage.API()

path = "dataservice/statistics/interface/aggregation"

payload = json.dumps({
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "2021-08-01T00:00:00 UTC",
          "2021-08-01T23:59:59 UTC"
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
        "property": "rx_octets",
        "type": "sum"
      },
      {
        "property": "tx_octets",
        "type": "sum"
      }
    ]
  }
})


response = api.send_request("POST", path, auth.headers, payload)

print(json.dumps(response, indent=4))

with open("api1.csv", 'w', newline='', encoding='utf-8') as output:  
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['system-ip', 'hostname', 'interface', 'rx_octets', 'tx_octets'])
    for row in response['data']:
        writer.writerow([row['vmanage_system_ip'], row['host_name'], row['interface'], row['rx_octets'], row['tx_octets']])
