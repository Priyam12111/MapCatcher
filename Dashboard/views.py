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
    collection = db["Mapcollection"]

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

    for location, pincode, data in zip(batch_locations, pincodes, documents):
        try:
            customIcontype = folium.CustomIcon(
                icon_image=f'static/{data["Crop_Type"].strip()}.jpg', icon_size=(60, 60)
            )
        except Exception:
            customIcontype = folium.CustomIcon(
                icon_image=f'static/{data["Crop_Type"]}.jpg', icon_size=(60, 60)
            )

        popup_text = f"<div onmouseover='sayHello(event)' id='poppuphtml' style='width: 200px;'>Crop Type: {data['Crop_Type']}<br>Crop Area: {data['CROP_AREA']} sq<br>Crop Production: {data['CROP_PRODUCTION']}<br>Season: {data['Season']}<br>Pincode: {pincode}</div>"
        folium.Marker(
            [location.latitude, location.longitude],
            popup=popup_text,
            icon=customIcontype,
        ).add_to(m)
    js_code = """
        <script>
            function sayHello(e) {
                var popupElement = e.currentTarget;
                var popupText = popupElement.innerHTML || popupElement.innerHTML;
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


def CropInsights(request):
    collection = db["LargeData"]

    total_documents = collection.count_documents({})
    page_number = request.GET.get("page")
    if page_number != None:
        start_index = (int(page_number) - 1) * totalElem
    else:
        start_index = 0

    pincodes = list(
        collection.find({}, {"pincode": 1}).skip(start_index).limit(totalElem)
    )
    pincodes = [terms["pincode"] for terms in pincodes]
    batch_locations = batch_geocode(pincodes)
    paginator = Paginator(range(total_documents), totalElem)
    page_obj = paginator.get_page(page_number)
    totalpages = paginator.num_pages
    documents = list(
        collection.find().sort("_id", 1).skip(start_index).limit(totalElem)
    )
    m = folium.Map(location=[20, 77], zoom_start=5)

    for location, pincode, data in zip(batch_locations, pincodes, documents):
        try:
            customIcontype = folium.CustomIcon(
                icon_image=f'static/{data["crop_name"].strip()}.jpg', icon_size=(60, 60)
            )
        except Exception:
            customIcontype = folium.CustomIcon(
                icon_image=f'static/{data["crop_name"]}.jpg', icon_size=(60, 60)
            )

        popup_text = f"""
<div onmouseover='sayHello(event)' id='popuphtml' style='width: 200px;height:100px;overflow:scroll;scrollbar-width: none;-ms-overflow-style: none;'>
    Name of BC: {data.get('name_of_bc', 'N/A')}<br>
    Contact Number: {data.get('contact_number', 'N/A')}<br>
    Gender: {data.get('gender', 'N/A')}<br>
    Bank Name: {data.get('bank_name', 'N/A')}<br>
    State: {data.get('state', 'N/A')}<br>
    District: {data.get('district', 'N/A')}<br>
    Office Name: {data.get('office_name', 'N/A')}<br>
    Pincode: {data.get('pincode', 'N/A')}<br>
    Corporate BC name: {data.get('corporate_bc_name', 'N/A')}<br>
    ODOP product: {data.get('odop_product', 'N/A')}<br>
    CODE WORD OF PRODUCT LIST: {data.get('code_word_of_product_list', 'N/A')}<br>
    CROP1 NAME: {data.get('crop1_name', 'N/A')}<br>
    CROP1 SEASON: {data.get('crop1_season', 'N/A')}<br>
    CROP1 AREA: {data.get('crop1_area', 'N/A')}<br>
    CROP1 PRODUCTION: {data.get('crop1_production', 'N/A')}<br>
    CROP1 Pincode: {data.get('crop1_pincode', 'N/A')}<br>
    CROP NAME: {data.get('crop_name', 'N/A')}<br>
    SEASON: {data.get('season', 'N/A')}<br>
    CROP AREA: {data.get('crop1_area', 'N/A')}<br>
    CROP PRODUCTION: {data.get('crop1_production', 'N/A')}<br>
    CROP NAME.1: {data.get('crop_name_1', 'N/A')}<br>
    SEASON.1: {data.get('season_1', 'N/A')}<br>
    CROP AREA.1: {data.get('crop_area_1', 'N/A')}<br>
</div>
"""
        folium.Marker(
            [location.latitude, location.longitude],
            popup=popup_text,
            icon=customIcontype,
        ).add_to(m)
    js_code = """
        <script>
            function sayHello(e) {
                var popupElement = e.currentTarget;
                var popupText = popupElement.innerHTML || popupElement.innerHTML;
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
        "templates/cropinsight.html",
        {
            "map_html": map_html,
            "items": documents,
            "page_obj": page_obj,
            "totalpages": totalpages,
        },
    )
