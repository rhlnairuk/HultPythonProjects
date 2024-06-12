import urllib.request
import json
import time
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TransportFetchData:
    def __init__(self):
        self.all_arrivals = None
        self.baseurl = "https://api.tfl.gov.uk/StopPoint"
        self.stop_point_lat = 51.52143248340143
        self.stop_point_lon = -0.1151982313809993
        self.radius = 500

    def fetch_stop_points(self):
        sp_url = urllib.request.urlopen(
            f"{self.baseurl}?lat={self.stop_point_lat}&lon={self.stop_point_lon}&radius={self.radius}&stoptypes=NaptanMetroStation,NaptanRailStation,NaptanBusCoachStation,NaptanFerryPort,NaptanPublicBusCoachTram")
        return json.loads(sp_url.read().decode())

    def fetch_arrivals(self, id):
        fa_url = urllib.request.urlopen(f"{self.baseurl}/{id}/Arrivals")
        return json.loads(fa_url.read().decode())

    def save_arrival_data(self, all_arrivals, file_path):
        with open(file_path, 'w') as file:
            json.dump(all_arrivals, file, indent=4)

    def get_all_arrivals(self, file_path):
        stop_points_dict = self.fetch_stop_points()
        stop_point_dict = {}
        self.all_arrivals = {}
        for stop in stop_points_dict['stopPoints']:
            stop_point_dict[stop['id']] = {stop['stopType']: stop['commonName']}
        for id, cn in stop_point_dict.items():
            print(f"Stop: {list(cn.values())[0]}, StopID: {id}")
            arrivals = self.fetch_arrivals(id)
            if arrivals:
                for arrival in arrivals:
                    print(
                        f"Mode: {arrival['modeName']},  Line: {arrival['lineId']}, Destination: {arrival['destinationName']}, stationName: {arrival['stationName']},  Time to Station: {arrival['timeToStation'] / 60} Minutes, platformName: {arrival['platformName']}")
                    self.all_arrivals.setdefault(id, []).append({
                        "Arrivals": True,
                        "Mode": arrival['modeName'],
                        "Line": arrival['lineId'],
                        "Destination": arrival['destinationName'],
                        "stationName": arrival['stationName'],
                        "timeToStation": arrival['timeToStation'],
                        "platformName": arrival['platformName']
                    })
            else:
                print("No arrivals")
                self.all_arrivals[id] = [{"Arrivals": False}]
            time.sleep(10)
        self.save_arrival_data(self.all_arrivals, file_path)


# Load the data
class TransportDataLoader:
    def __init__(self):
        self.file_path = 'upcoming_arrivals_multiple_stops.json'
        #transport_fetcher = TransportFetchData()
        #transport_fetcher.get_all_arrivals(self.file_path)

    def load_data(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return pd.DataFrame.from_dict(data, orient='index')


# Analyse the data
class TransportAnalyseData:
    def __init__(self):
        loader = TransportDataLoader()
        self.data = loader.load_data()
        print(self.data[0])
        rows, cols = self.data.shape
        self.data_copy = self.data.copy()
        stations = [ self.data[0]['940GZZLUCHL']['stationName'] ]
        times = [ self.data[0]['940GZZLUCHL']['timeToStation'] ]
        self.time_sorted = sorted(zip(stations, times), key=lambda x: x[1])
        print(self.time_sorted)
        #stations = self.data_copy['490007391E']['Arrivals'].explode()['stationName'].tolist()
        #times = self.data_copy['490007391E']['Arrivals'].explode()['timeToStation'].tolist()
        #self.time_sorted = sorted(zip(stations, times), key=lambda x: x[1])
        #print(self.time_sorted)


#Number of Arrivals per Stop
#Number of Arrivals per Line
#Distribution of Arrival Times based on Time to Station and Frequency
#Average arrival time for each stop and line
#Peak average arrivals in each stops and lines


# Execute the analysis
if __name__ == "__main__":
    TransportAnalyseData()
