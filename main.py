import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv 

#####################################LOAD PASSWORDS########################################
load_dotenv("C:/Users/Popuś/Desktop/Python/environment_variables/.env")

#########################################TWILIO#############################################
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
TEL_TWILIO = os.getenv("TEL_TWILIO")
TEL_MY = os.getenv("TEL_MY")

OWM_Endpoint= "https://api.openweathermap.org/data/2.8/onecall"
api_key = os.getenv("api_key")


######################################ENDPOINTS#####################################
#Endpoint current weather
# ("https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}")
#Endpoint weather one_call - 48hours
# https://api.openweathermap.org/data/2.8/onecall

#############################INFORMATION FROM API########################################
#rainy place
rainy_lat = 54.352024
rainy_lon = 18.646639

weather_params = {
    "lat":rainy_lat,
    "lon":rainy_lon,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
# print(response.status_code)
response.raise_for_status()
weather_data = response.json()
# print(weather_data)

#single info about condition
single_data_hour = weather_data["hourly"][0:12][2]["weather"][0]["id"]
# print(single_data_hour)

##################################SMS SEND SECTION##################################

will_rain = False

#all info about 12 hour
twelve_hourly_data = weather_data["hourly"][0:12]
for one_hour in  twelve_hourly_data:
    one_weather_id = one_hour["weather"][0]["id"]
    # print(one_weather_id)
    if int(one_weather_id) < 700:
        # print("Bring an umbrella.")
        will_rain = True

if will_rain is True:
    # print("Single info: Bring an umbrella.")

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="It's going to rain today. Remember to bring an umbrella with you!☂️",
                        from_=TEL_TWILIO,
                        to=TEL_MY,
                    )

    print(message.sid)# create id for message
    print(message.status)#check status of message

