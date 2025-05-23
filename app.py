import streamlit as st
from datetime import datetime
import requests

'''
# NY TaxiFare
'''

st.markdown('''
Estimate Taxi Fare Pricing in NY

Enter your info below:
''')



# 1. USER INPUT
now = datetime.now()

col1, col2, col3= st.columns(3)
with col1:
    passenger_count = st.number_input(
        "Number of Passengers",
        min_value=1,
        step=1,
        format="%d"
    )
with col2:
    d = st.date_input(
        "Select a Date",
        value=now.date()
    )
with col3:
    t = st.time_input(
        "Select a Time",
        value=now.time()
    )

t=t.replace(second=0, microsecond=0)
combine_datetime = f'{d} {t}'

# st.subheader("Pickup and Drop Off Locations")

# col1, col2 = st.columns(2)
# with col1:
#     pickup_add = st.text_input('Pickup Address')
# with col2:
#     drop_off_add = st.text_input('Drop Off Address')

with col1:
    pickup_lat = st.number_input("Pickup Latitude", format="%.6f", value=40.783282)
    pickup_lon = st.number_input("Pickup Longitude", format="%.6f", value=-73.950655)

with col2:
    dropoff_lat = st.number_input("Drop-off Latitude", format="%.6f", value=40.769802)
    dropoff_lon = st.number_input("Drop-off Longitude", format="%.6f", value=-73.984365)

# 2. Params for API request

params = {
    'pickup_datetime': combine_datetime,
    'pickup_longitude': pickup_lon,
    'pickup_latitude': pickup_lat,
    'dropoff_longitude': dropoff_lon,
    'dropoff_latitude': dropoff_lat,
    'passenger_count': passenger_count
}

url = 'https://taxifare-523741188942.asia-northeast1.run.app/predict'

if st.button("Predict Fare"):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        prediction = response.json().get("fare")
        st.success(f"💰 Estimated Fare: ${prediction}")

    except Exception as e:
        st.error(f'Error: {e}')
