import folium

def show_on_map(latitude, longitude):
    # Create a map centered around the provided latitude and longitude
    map_obj = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Add a marker for the provided location
    folium.Marker(location=[latitude, longitude], popup="Location").add_to(map_obj)

    # Display the map
    return map_obj

if __name__ == "__main__":
    map_obj = show_on_map(25.533508, 87.583748)
    # Save the map as an HTML file
    map_obj.save("map.html")

