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
            #print(f"Stop: {list(cn.values())[0]}, StopID: {id}")
            arrivals = self.fetch_arrivals(id)
            if arrivals:
                for arrival in arrivals:
                    #print(f"Mode: {arrival['modeName']},  Line: {arrival['lineId']}, Destination: {arrival['destinationName']}, StationName: {arrival['stationName']},  Time to Station: {round(arrival['timeToStation'] / 60, 2)} Minutes, PlatformName: {arrival['platformName']}")
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
                #print("No arrivals")
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
    def __init__(self, mode):
        self.mode = mode
        loader = TransportDataLoader()
        self.data = loader.load_data()
        self.mode_bus = self.data.query('Mode == "bus"')
        self.mode_tube = self.data.query('Mode == "tube"')
        self.destination_group = self.data.groupby('Destination').size().sort_values(ascending=False)
        self.conditional_data = self.mode_bus if mode == "bus" else self.mode_tube
        self.arrivals_per_stop = self.conditional_data.groupby('stationName').size().sort_values(ascending=False)
        self.arrivals_per_line = self.conditional_data.groupby('Line').size().sort_values(ascending=False)
        ten_min_time_to_station = self.conditional_data.query('timeToStation > 600')
        self.arrivals_per_stop_ten_min_limit = ten_min_time_to_station.groupby('stationName').size().sort_values(ascending=False)
        self.destination_group = self.conditional_data.groupby('Destination').size().sort_values(ascending=False)
        self.station_names = self.conditional_data['stationName'].unique()

    def display_data(self):
        for station in self.station_names:
            station_data = self.data[self.data['stationName'] == station].sort_values(by='timeToStation')
            print(f"{station}:")
            print('-' * 50)
            for _, row in station_data.iterrows():
                if row['Mode'] == 'bus':
                    print(f"Mode: {row['Mode']} Bus Number: {row['Line']} Destination: {row['Destination']} in {round(int(row['timeToStation']) / 60)} min")
                elif row['Mode'] == 'tube':
                    print(f"Mode: {row['Mode']} Line: {row['Line']} Destination: {row['Destination']} in {round(int(row['timeToStation']) / 60)} min")

            print('-' * 50)
    def create_plots(self):
        # Plot: Number of Arrivals per Station in 10 Minutes
        plt.figure(figsize=(12, 8))
        self.arrivals_per_stop_ten_min_limit.plot(kind='barh')
        plt.title(f'Number of Arrivals per {self.mode} Station in 10 Minutes')
        plt.xlabel('Number of Arrivals')
        plt.ylabel('Station Name')
        plt.tight_layout(pad=3.0)
        plt.show()

        # Plot arrivals per stop
        plt.figure(figsize=(10, 6))
        self.arrivals_per_stop.plot(kind='barh')
        plt.title(f"Total Number of {self.mode} Arrivals per Stop")
        plt.ylabel('Stop Name')
        plt.xlabel('Number of Arrivals')
        plt.xticks(rotation=90)
        plt.tight_layout(pad=3.0)
        plt.show()
        # Plot arrivals for destinations per stop
        plt.figure(figsize=(10, 6))
        self.destination_group.plot(kind='barh')
        plt.title(f"Number of {self.mode} Arrivals by Destinations")
        plt.ylabel('Stop Name')
        plt.xlabel('Number of Arrivals')
        plt.xticks(rotation=90)
        plt.tight_layout(pad=3.0)
        plt.show()

        # Prepare data for plotting
        data_to_plot = [self.conditional_data[self.conditional_data['stationName'] == station]['timeToStation'].values / 60 for station in self.station_names]

        # Box Plot: Time to Station per Bus/Tube at each Station
        plt.figure(figsize=(14, 8))
        plt.boxplot(data_to_plot, tick_labels=self.station_names,showmeans=True,
            meanline=True,
            medianprops=dict(color='blue', linewidth=2),
            meanprops=dict(color='red', linewidth=2))
        plt.title(f'Time to Station per {self.mode} at each Station/Stop')
        plt.xlabel('Station Name')
        plt.ylabel('Time to Station (minutes)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(True)
        plt.show()

        for station in self.station_names:
            station_data = self.conditional_data[self.conditional_data['stationName'] == station]
            plt.scatter([station] * len(station_data), (station_data['timeToStation'] / 60), alpha=0.6)

        plt.title(f'Time to Station per {self.mode} at each Station')
        plt.xlabel('Station Name')
        plt.ylabel('Time to Station (minutes)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    BusTransport = TransportAnalyseData("bus")
    TubeTransport = TransportAnalyseData("tube")
    BusTransport.create_plots()
    TubeTransport.create_plots()
    BusTransport.display_data()
    TubeTransport.display_data()

