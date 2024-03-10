from django.shortcuts import render
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pymongo import MongoClient
from django.core.paginator import Paginator


client = MongoClient("mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/")
db = client["MapData"]
collection = db["Mapcollection"]
print('NominatimCount')
geolocator = Nominatim(user_agent="pincode_locator", timeout=5)

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

totalElem = 10
def map_view(request):
    total_documents = collection.count_documents({})
    page_number = request.GET.get('page')
    if page_number != None:
        start_index = (int(page_number) - 1) * totalElem
    else:
        start_index = 0

    pincodes = list(collection.find({},{'Pincode':1}).skip(start_index).limit(totalElem))
    pincodes = [terms['Pincode'] for terms in pincodes]
    batch_locations = batch_geocode(pincodes)
    paginator = Paginator(range(total_documents), totalElem)
    page_obj = paginator.get_page(page_number)
    totalpages = paginator.num_pages
    documents = list(collection.find().sort('_id',1).skip(start_index).limit(totalElem))
    m = folium.Map(location=[20, 77], zoom_start=5)

    for location, pincode, data in zip(batch_locations, pincodes, documents):

        popup_text = f"<div style='width: 200px;'>Crop Type: {data['Crop_Type']}<br>Crop Area: {data['CROP_AREA']}<br>Crop Production: {data['CROP_PRODUCTION']}<br>Season: {data['Season']}<br>Pincode: {pincode}</div>"
        green_color = "#00FF00"  # Hex color for green
        icon_image = "https://w7.pngwing.com/pngs/51/802/png-transparent-circle-green-circle-color-grass-sphere.png"
        folium.CircleMarker(
            [location.latitude, location.longitude],
            radius=10,  # You can adjust the radius as needed
            popup=popup_text,
            color=green_color,
            fill=True,
            fill_color=green_color,
            fill_opacity=1,
        ).add_to(m)

    map_html = m._repr_html_()

    return render(
        request,
        "templates/dashboard.html",
        {"map_html": map_html, "items": documents,'page_obj':page_obj,'totalpages':totalpages},
    )
