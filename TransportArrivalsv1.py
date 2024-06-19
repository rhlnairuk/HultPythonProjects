import urllib.request
import json
import time
import pandas as pd
import ssl
import matplotlib.pyplot as plt

ssl._create_default_https_context = ssl._create_unverified_context


class TransportFetchData:
    def __init__(self):
        self.all_arrivals = None
        self.baseurl = "https://api.tfl.gov.uk/StopPoint"
        # Latitude and Longitude of HULT International Business School
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
        stop_points_data = self.fetch_stop_points()
        stop_point_dict = {}
        self.all_arrivals = {}
        for stop in stop_points_data['stopPoints']:
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
        transport_fetcher = TransportFetchData()
        transport_fetcher.get_all_arrivals(self.file_path)

    def load_data(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        records = []
        for stop_id, arrivals_list in data.items():
            for arrival in arrivals_list:
                if arrival['Arrivals']:
                    records.append(arrival)
        return pd.DataFrame(records)


# Analyse the data
class TransportAnalyseData:
    def __init__(self):
        loader = TransportDataLoader()
        self.data = loader.load_data()
        mode_bus = self.data.query('Mode == "bus"')
        mode_tube = self.data.query('Mode == "tube"')
        arrivals_per_stop = mode_bus.groupby('stationName').size().sort_values(ascending=False)
        arrivals_per_line = mode_bus.groupby('Line').size().sort_values(ascending=False)

        # Plot arrivals per Bus stop
        plt.figure(figsize=(10, 6))
        arrivals_per_stop.plot(kind='barh')
        plt.title('Number of Bus Arrivals per Stop')
        plt.xlabel('Stop Name')
        plt.ylabel('Number of Arrivals')
        plt.xticks(rotation=90)

        # Plot arrival times distribution
        plt.figure(figsize=(10, 6))
        time_to_station_minutes = self.data['timeToStation'] / 60
        time_to_station_minutes.plot(kind='hist', bins=20, edgecolor='black')
        plt.title('Distribution of Arrival Times')
        plt.xlabel('Time to Station (minutes)')
        plt.ylabel('Frequency')

        # Plot popular lines
        plt.figure(figsize=(10, 6))
        arrivals_per_line.plot(kind='bar')
        plt.title('Number of Arrivals per Bus Number')
        plt.xlabel('Bus Number')
        plt.ylabel('Number of Arrivals')


        plt.figure(figsize=(10, 6))
        arrivals_per_line.plot(kind='bar')
        plt.title('Frequency of Buses per Line')
        plt.xlabel('Line')
        plt.ylabel('Number of Buses')

        plt.tight_layout()
        plt.show()



#Number of Arrivals per Stop
#Number of Arrivals per Line
#Distribution of Arrival Times based on Time to Station and Frequency
#Average arrival time for each stop and line
#Peak average arrivals in each stops and lines


# Execute the analysis
if __name__ == "__main__":
    TransportAnalyseData()
