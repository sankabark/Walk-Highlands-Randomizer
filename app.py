import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import csv
import random

# 1. THE SETTINGS (Side of the screen)
st.title("🏔️ Walk Highlands Randomizer")

max_grade = st.slider("Max Grade - 1 Easy ---- 5 Hard", 1, 5, 3)
postcode = st.text_input("Your Postcode", "IV1 1AA")
max_dist = st.number_input("Max Travel Distance to Travel (miles)", value=25)
max_time = st.number_input("Max Walk Time (hours)", value=4.0)

# 2. LOAD DATA
with open('walks1.csv', mode='r', encoding='latin1') as file:
    hikes = list(csv.DictReader(file))

# 3. THE "GO" BUTTON
if st.button("Find a Random Walk"):
    geolocator = Nominatim(user_agent="my_hike_app")
    location = geolocator.geocode(postcode)

    if location:
        user_coords = (location.latitude, location.longitude)
        matches = []

        for hike in hikes:
            
            h_grade = int(hike['Grade'])
            h_hours = float(hike['Hours'])

            if h_grade <= max_grade and h_hours <= max_time:
                gps = hike['GPS START'].split(',')
                h_coords = (float(gps[0]), float(gps[1]))
                dist = geodesic(user_coords, h_coords).miles

                if dist <= max_dist:
                    hike['dist_away'] = round(dist, 1)
                    matches.append(hike)

        # 4. SHOW THE RESULT
        if matches:
            walk = random.choice(matches)
            gps_parts = walk['GPS START'].split(',')
            map_data = pd.DataFrame({
                'lat': [float(gps_parts[0])],
                'lon': [float(gps_parts[1])]
            })
            st.map(map_data)
            st.success(f"Go here: {walk['Walk']}")
            st.write(f"Grade: {walk['Grade']} | Distance: {walk['dist_away']} miles away")
            st.write(f"[Link to Walkhighlands]({walk['Link']})")
        else:
            st.error("No walks found. Try changing your filters!")
