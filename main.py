import requests
from datetime import datetime
import smtplib
import time

# Southern California Cords
MY_LAT = 34.077687  # Your latitude
MY_LONG = -118.425937  # Your longitude
# my info
MY_EMAIL = "bombastic.code@gmail.com"
MY_NAME = "Mardean"


def check_ISS_location():
    # get iss cordinates
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    # save the cords to variables
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # checks if your position is within +5 or -5 degrees of the ISS position.
    print(iss_latitude)
    print(iss_longitude)
    print(MY_LAT)
    print(MY_LONG)
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
            return True
    return False


def night_time_check():
    # parameters to pass to sunrise-sunset api
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    # save the hours in variables
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    # get time now
    time_now = datetime.now().hour

    if sunset <= time_now or time_now <= sunrise:
        return True
    return False


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
while True:

    if check_ISS_location() and night_time_check():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password="rqejgbjowttnlukz")
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="mardeanmontane@gmail.com",
                                msg=f"Subject:ISS Overhead\n\n The ISS is above you and since it is dark you can see it. Look in the sky!")
    time.sleep(60)
