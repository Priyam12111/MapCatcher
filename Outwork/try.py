import requests
from foliummm import show_on_map

def get_lat_long_from_pincode(pincode, district, state):
    url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&county={district}&state={state}&format=json"
    if district == "N/A" or state == "N/A":
        # url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&format=json"
        url = f"https://nominatim.openstreetmap.org/search?state={state}&format=json"


    headers = {
        "User-Agent": "YourApp/1.0"  # Replace YourApp/1.0 with your application name and version
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            return None, None
    else:
        print("Error:", response.status_code)
        return None, None
    
# Example usage
pincode = "212207"
district = "N/A"
state = "Uttar Pradesh"
latitude, longitude = get_lat_long_from_pincode(pincode, district, state)
map_obj = show_on_map(latitude, longitude)
map_obj.save("map.html")
print("Latitude:", latitude)
print("Longitude:", longitude)

