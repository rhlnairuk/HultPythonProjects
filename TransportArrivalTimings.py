import urllib.request
from pprint import pprint
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context


# Identifying required API and understanding the data

stop_point_lat = 51.52143248340143
stop_point_lon = -0.1151982313809993
stop_points = urllib.request.urlopen('https://api.tfl.gov.uk/Stoppoint?lat=51.52143248340143&lon=-0.1151982313809993&radius=500&stoptypes=NaptanMetroStation,NaptanRailStation,NaptanBusCoachStation,NaptanFerryPort,NaptanPublicBusCoachTram')
#stop_point = urllib.request.urlopen('https://api.tfl.gov.uk/Stoppoint/940GZZLUHBN')
#arrivals = urllib.request.urlopen('https://api.tfl.gov.uk/StopPoint/940GZZLUHBN/Arrivals')

stop_points_data = stop_points.read().decode()
stop_points_dict = json.loads(stop_points_data)

pprint(stop_points_dict['stopPoints'])

stop_point_dict = {}
arrivals_dict = []
for stop in stop_points_dict['stopPoints']:
#    print(f"Stop: {stop['commonName']}, Type: {stop['stopType']}, Distance: {stop['distance']} meters, id is {stop['id']}")
    stop_point_dict[stop['id']] = { stop['stopType']: stop['commonName'] }
pprint(stop_point_dict)
#"""
for id, cn in stop_point_dict.items():
    if "NaptanMetroStation" not in cn.keys():
        stop_point = urllib.request.urlopen(f"https://api.tfl.gov.uk/Stoppoint/{id}")
        stop_point_data = stop_point.read().decode()
        stop_point_dict = json.loads(stop_point_data)
        print(f"Stop: {cn}, Type: {stop_point_dict['stopType']}, StopID: {stop_point_dict['id']}")
    #print(f"Stop: {stop['commonName']}, Type: {stop['stopType']}")
        arrivals = urllib.request.urlopen(f"https://api.tfl.gov.uk/StopPoint/{stop_point_dict['id']}/Arrivals")
        arrivals_data = arrivals.read().decode()
        arrivals_dict = json.loads(arrivals_data)
if arrivals_dict != []:
    if len(arrivals_dict) > 0:
        for i in range(0 ,len(arrivals_dict) - 1):
            if len(arrivals_dict) > 0:
                print(f"Mode: {arrivals_dict[i]['modeName']},  Line: {arrivals_dict[i]['lineId']}, Destination: {arrivals_dict[i]['destinationName']}, Time to Station: {arrivals_dict[i]['timeToStation']} seconds")
            else:
                print(f"Mode: {arrivals_dict[0]['modeName']},  Line: {arrivals_dict[0]['lineId']}, Destination: {arrivals_dict[0]['destinationName']}, Time to Station: {arrivals_dict[0]['timeToStation']} seconds")


