import folium, requests
from folium.plugins import HeatMap
from time import sleep
from pymongo import MongoClient


def batch_geocode2(pincodes, districts, states):
    locations = []
    for pincode, district, state in zip(pincodes, districts, states):
        try:
            print("Checking", pincode, district, state)

            url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&county={district}&state={state}&format=json"
            if district == "N/A" or district == "":
                url = f"https://nominatim.openstreetmap.org/search?state={state}&format=json"

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
                print(f"Error processing Pincode {pincode}: {response.status_code}")
                locations.append((None, None))
        except Exception:
            pass

        sleep(1)

    return locations


client = MongoClient(
    "mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/"
)
db = client["MapData"]

collection = db["LargeData"]

pincodes_3 = list(
    collection.find({}, {"pincode": 1, "district ": 1, "state": 1})
    .sort("_id", 1)
    .skip(0)
    .limit(10)
)
pincodes = [terms["pincode"] for terms in pincodes_3]
districts = [
    term.get("district ", "") for term in pincodes_3
]  # Use get() with a default value
states = [term.get("state", "") for term in pincodes_3]
batch_locations2 = batch_geocode2(pincodes, districts, states)

formatted_data = [[point[0], point[1]]for point in batch_locations2 if point[0] is not None and point[1] is not None]

# Create a map centered at a specific location
m = folium.Map(location=[formatted_data[0][0], formatted_data[0][1]], zoom_start=4)

# Add heatmap layer
HeatMap(formatted_data, min_opacity=0.5, max_zoom=18, radius=15, blur=10).add_to(m)

# Save the map to an HTML file
m.save("heatmap.html")
