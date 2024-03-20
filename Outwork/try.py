
# import requests
# from foliummm import show_on_map

# def get_lat_long_from_pincode(pincode, district, state):
#     try:
#         url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&county={district}&state={state}&format=json"
#         if district == "N/A" or state == "N/A":
#             print("Some value is missing")
#             # url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&format=json"
#             url = f"https://nominatim.openstreetmap.org/search?state={state}&format=json"


#         headers = {
#             "User-Agent": "YourApp/1.0"  # Replace YourApp/1.0 with your application name and version
#         }
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             data = response.json()
#             if data:
#                 latitude = float(data[0]["lat"])
#                 longitude = float(data[0]["lon"])
#                 return latitude, longitude
#             else:
#                 print("Blank")
#                 return None, None
#         else:
#             print("Error:", response.status_code)
#             return None, None
#     except Exception:
#         url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&format=json"
#         headers = {
#                 "User-Agent": "YourApp/1.0"  # Replace YourApp/1.0 with your application name and version
#             }
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             data = response.json()
#             if data:
#                 latitude = float(data[0]["lat"])
#                 longitude = float(data[0]["lon"])
#                 return latitude, longitude
#             else:
#                 return None, None
#         else:
#             print("Error:", response.status_code)
#             return None, None
# # Example usage
# pincode = "206251"
# district = "AURAIYA"
# state = "Uttar Pradesh"
# latitude, longitude = get_lat_long_from_pincode(pincode, district, state)
# print(latitude,longitude)
# map_obj = show_on_map(latitude, longitude)
# map_obj.save("map.html")
# print("Latitude:", latitude)
# print("Longitude:", longitude)

# ->>>>>>>>>>>>>>>>>>>>>>>>>>>>

# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient(
#     "mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/"
# )
# db = client["MapData"]
# collection = db["Mapcollection"]

# # Update documents to remove extra spaces from the 'district' field
# collection.update_many(
#     # Filter to match all documents where the 'district' field exists
#     {"district ": {"$exists": True}},
#     # Update operation to trim the 'district' field
#     [{"$set": {"district": {"$trim": {"input": "$district"}}}}]
# )

# print("Extra spaces removed from the 'district' field in all documents.")







import folium
from folium.plugins import HeatMap

# Sample data (latitude, longitude, popup_text)
data = [
    [37.7749, -122.4194, "San Francisco Popup"],   # San Francisco
    [34.0522, -118.2437, "Los Angeles Popup"],   # Los Angeles
    [40.7128, -74.0060, "New York Popup"],    # New York
    [41.8781, -87.6298, "Chicago Popup"],    # Chicago
    [29.7604, -95.3698, "Houston Popup"]     # Houston
]

# Create a map centered at a specific location
# m = folium.Map(location=[data[0][0], data[0][1]], zoom_start=4, tiles='Stamen Terrain')

m = folium.Map(location=[40.7128, -74.0060],tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)')

# folium.LayerControl().add_to(m)
# Add heatmap layer
# HeatMap(data, min_opacity=0.5, max_zoom=18, radius=15, blur=10).add_to(m)

# Save the map to an HTML file
m.save('heatmap_with_popup.html')
