from django.shortcuts import render
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pymongo import MongoClient
from django.core.paginator import Paginator


client = MongoClient(
    "mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/"
)
db = client["MapData"]
collection = db["Mapcollection"]
print("NominatimCount")
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
    page_number = request.GET.get("page")
    if page_number != None:
        start_index = (int(page_number) - 1) * totalElem
    else:
        start_index = 0

    pincodes = list(
        collection.find({}, {"Pincode": 1}).skip(start_index).limit(totalElem)
    )
    pincodes = [terms["Pincode"] for terms in pincodes]
    batch_locations = batch_geocode(pincodes)
    paginator = Paginator(range(total_documents), totalElem)
    page_obj = paginator.get_page(page_number)
    totalpages = paginator.num_pages
    documents = list(
        collection.find().sort("_id", 1).skip(start_index).limit(totalElem)
    )
    m = folium.Map(location=[20, 77], zoom_start=5)
    color_mapping = {"Bajra": "#00FF00", "Wheat": "#FFA500"}  # Adjust as per your needs

    for location, pincode, data in zip(batch_locations, pincodes, documents):
        popup_text = f"<div onmouseover='sayHello(event)' id='poppuphtml' style='width: 200px;'>Crop Type: {data['Crop_Type']}<br>Crop Area: {data['CROP_AREA']}<br>Crop Production: {data['CROP_PRODUCTION']}<br>Season: {data['Season']}<br>Pincode: {pincode}</div>"
        green_color = "#00FF00"  # Hex color for green
        try:
            color = color_mapping[data['Crop_Type']]
        except Exception:
            color = "#FFA500"
        folium.CircleMarker(
            [location.latitude, location.longitude],
            radius=float(data['CROP_AREA'])/10000, 
            popup=popup_text,
            color=color,
            fill_color=color,
            fill=True,
            fill_opacity=1,
        ).add_to(m)
    js_code = """
        <script>
            function sayHello(e) {
                var popupElement = e.currentTarget;
                var popupText = popupElement.innerHTML || popupElement.innerHTML;

                // Update the content of the div with class 'mapDetails' in the parent document
                var parentDiv = window.parent.document.querySelector('.mapDetails');
                if (parentDiv) {
                    parentDiv.innerHTML = popupText;
                }
            }
        </script>
    """

    # Add the JavaScript code to the map
    m.get_root().html.add_child(folium.Element(js_code))
    map_html = m._repr_html_()

    return render(
        request,
        "templates/dashboard.html",
        {
            "map_html": map_html,
            "items": documents,
            "page_obj": page_obj,
            "totalpages": totalpages,
        },
    )
