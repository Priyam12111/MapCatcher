from django.shortcuts import render
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

df = pd.read_csv(r'static/nsample.csv')

pincodes = df['Pincode'].tolist()

geolocator = Nominatim(user_agent="pincode_locator")

def batch_geocode(pincodes):
    locations = []

    for pincode in pincodes:
        try:
            location = geolocator.geocode(str(pincode))
            if location:
                locations.append(location)
        except GeocoderTimedOut as e:
            print(f"Error processing Pincode {pincode}: {e}")

    return locations

batch_locations = batch_geocode(pincodes)

def map_view(request):
    m = folium.Map(location=[20, 77], zoom_start=5)

    for location, pincode, data in zip(batch_locations, pincodes, df.iterrows()):
        index, data = data

        popup_text = f"<div style='width: 200px;'>Crop Type: {data['Crop_Type']}<br>Crop Area: {data['CROP AREA']}<br>Crop Production: {data['CROP PRODUCTION']}<br>Season: {data['Season']}<br>Pincode: {pincode}</div>"

        icon_image = r'static/Bajra.jpg'
        folium.Marker([location.latitude, location.longitude], popup=popup_text, icon=folium.CustomIcon(icon_image=icon_image, icon_size=(60, 60))).add_to(m)

    map_html = m._repr_html_()

    return render(request, 'templates/dashboard.html', {'map_html': map_html})
