
# import requests
# from foliummm import show_on_map

# def get_lat_long_from_pincode(pincode, district, state):
#     url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&county={district}&state={state}&format=json"
#     if district == "N/A" or state == "N/A":
#         print("Some value is missing")
#         # url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&format=json"
#         url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&state={state}&format=json"


#     headers = {
#         "User-Agent": "YourApp/1.0"  # Replace YourApp/1.0 with your application name and version
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         if data:
#             latitude = float(data[0]["lat"])
#             longitude = float(data[0]["lon"])
#             return latitude, longitude
#         else:
#             return None, None
#     else:
#         print("Error:", response.status_code)
#         return None, None
    
# # Example usage
# pincode = "212207"
# district = "KAUSHAMBI"
# state = "Uttar Pradesh"
# latitude, longitude = get_lat_long_from_pincode(pincode, district, state)
# map_obj = show_on_map(latitude, longitude)
# map_obj.save("map.html")
# print("Latitude:", latitude)
# print("Longitude:", longitude)
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/"
)
db = client["MapData"]
collection = db["Mapcollection"]

# Update documents to remove extra spaces from the 'district' field
collection.update_many(
    # Filter to match all documents where the 'district' field exists
    {"district ": {"$exists": True}},
    # Update operation to trim the 'district' field
    [{"$set": {"district": {"$trim": {"input": "$district"}}}}]
)

print("Extra spaces removed from the 'district' field in all documents.")