# STEP1 Step 1: Load and Explore NASA SMAP H5 Data

import h5py
import pandas as pd

# Path to your NASA SMAP H5 data file
h5_file_path = "path_to_your_file.h5"

# Open the H5 file
with h5py.File(h5_file_path, 'r') as h5_file:
    # List all datasets in the file
    print("Available datasets:")
    def print_attrs(name, obj):
        print(name)

    h5_file.visititems(print_attrs)

# STEP2 Extracting Soil Moisture Data

# Extracting soil moisture data (assuming dataset is named 'Soil_Moisture_Retrieval_Data_AM')
with h5py.File(h5_file_path, 'r') as h5_file:
    soil_moisture = h5_file['Soil_Moisture_Retrieval_Data_AM/soil_moisture'][:]
    latitudes = h5_file['Soil_Moisture_Retrieval_Data_AM/latitude'][:]
    longitudes = h5_file['Soil_Moisture_Retrieval_Data_AM/longitude'][:]

# Create a Pandas DataFrame to store and visualize the soil moisture data
data = pd.DataFrame({
    'Latitude': latitudes.flatten(),
    'Longitude': longitudes.flatten(),
    'Soil Moisture': soil_moisture.flatten()
})

# Display the first few rows
print(data.head())


#STEP 3  Integrating Weather Data (OpenWeatherMap API)
# Sign Up for OpenWeatherMap and get an API key: OpenWeatherMap API.

import requests

# API key and endpoint for OpenWeatherMap
API_KEY = 'your_api_key'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# Define your location
location = {'lat': 'your_latitude', 'lon': 'your_longitude'}

# Fetch weather data
response = requests.get(BASE_URL, params={'lat': location['lat'], 'lon': location['lon'], 'appid': API_KEY, 'units': 'metric'})
weather_data = response.json()

# Example: extracting precipitation forecast for the next 5 days
for forecast in weather_data['list']:
    date = forecast['dt_txt']
    rainfall = forecast['rain']['3h'] if 'rain' in forecast else 0
    print(f"Date: {date}, Rainfall: {rainfall} mm")

# STEP 4 Irrigation Scheduling Logic
# Define thresholds (you can customize these)
SOIL_MOISTURE_THRESHOLD = 0.2  # Below this value, irrigation is needed (example threshold)
RAIN_THRESHOLD = 5  # If more than 5 mm of rain is expected, skip irrigation

def check_irrigation(soil_moisture, expected_rainfall):
    if soil_moisture < SOIL_MOISTURE_THRESHOLD and expected_rainfall < RAIN_THRESHOLD:
        return "Irrigation needed"
    elif expected_rainfall >= RAIN_THRESHOLD:
        return "No irrigation needed (Rain expected)"
    else:
        return "Soil moisture sufficient, no irrigation needed"

# Example usage
for index, row in data.iterrows():
    forecast_rain = 3  # Example rain forecast in mm (you should use actual weather data here)
    irrigation_decision = check_irrigation(row['Soil Moisture'], forecast_rain)
    print(f"Location: {row['Latitude']}, {row['Longitude']}, Irrigation Decision: {irrigation_decision}")

# STEP 5 Monitoring and Feedback
# Track water usage and efficiency
water_usage_log = []

def log_water_usage(location, water_used, efficiency):
    water_usage_log.append({
        'Location': location,
        'Water Used': water_used,
        'Efficiency': efficiency
    })

# Example usage
log_water_usage("Location 1", 500, "High Efficiency")
print(pd.DataFrame(water_usage_log))

