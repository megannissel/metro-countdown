"""
This code was used to generate the stations.json file, which can be
used as a reference when specifying desired stations in wmata.py
"""

import httplib
import json

from secrets import KEY_PRIMARY

headers = {'api_key': KEY_PRIMARY}

def stations_query():
  try:
    conn = httplib.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/Rail.svc/json/jStations", "{body}", headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return data

  except Exception as e:
    print "Error: {}".format(e)
    return None

def generate_stations_json():
  data = stations_query()

  if data:
    try:
      d = json.loads(data)
    except Exception as e:
      return "Error reading json: {}".format(e)

    stations = d['Stations']

    stations_dict = [{'code': str(s['Code']), 'name': str(s['Name']), 'line': str(s['LineCode1'])} for s in stations]

    with open('stations.json', 'w') as fout:
      json.dump(stations_dict, fout, sort_keys=True, indent=2)
    return 'OK'

  return "API request failed"

generate_stations_json()
