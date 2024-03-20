import folium,requests
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from time import sleep
import requests
from time import sleep

def batch_geocode2(districts):
    locations = []
    for district in districts:
        try:
            print("Checking", district)

            url = f"https://nominatim.openstreetmap.org/search?county={district}&format=json"

            headers = {
                "User-Agent": "MapSearch/1.0"  # Replace YourApp/1.0 with your application name and version
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data:
                    latitude = float(data[0]["lat"])
                    longitude = float(data[0]["lon"])
                    location = (latitude, longitude)
                    locations.append(location)
                else:
                    locations.append((None, None))
            else:
                print(f"Error processing District {district}: {response.status_code}")
                locations.append((None, None))
        except Exception:
            pass

        sleep(1)

    return locations

client = MongoClient("mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/")
db = client["LargeData"]
collection = db["Mapcollection"]


# Retrieve district data from MongoDB
district_data = collection.find({}, {"_id": 0, "district": 1, "latitude": 1, "longitude": 1})

# Create a folium map centered around your region
m = folium.Map(location=[20, 0], zoom_start=10)

# Iterate through district data and add markers to the map
for district in district_data:
    folium.Marker(
        location=[district["latitude"], district["longitude"]],
        popup=district["district"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

m.save("district_map.html")