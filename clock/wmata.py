import httplib
import json

from secrets import KEY_PRIMARY

# Base api url: https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{StationCodes}

headers = {
  'api_key': KEY_PRIMARY,
}

# List of station codes in /stations.json
# `stations` should be a comma-separated string of station codes; ex: 'E03,A03'
stations = 'E03' # U Street

# Only return times for trains going in the desired direction:
destinations = ['Branch Ave', 'Huntington']

def train_query(stations):
  try:
    conn = httplib.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/StationPrediction.svc/json/GetPrediction/{}".format(stations), "{body}", headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return data

  except Exception as e:
    print "Error: {}".format(e)

def next_train_times(stations, destinations):
  data = train_query(stations)

  try:
    d = json.loads(data)
  except Exception as e:
    print "Error reading json: {}".format(e)
    return [('ERR', '')]

  trains = d['Trains']

  next_trains = [(str(t['Line']), str(t['Min'])) for t in trains if t['DestinationName'] in destinations]
  return next_trains

def get_relevant_info():
  return next_train_times(stations, destinations)
