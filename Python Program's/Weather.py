import requests

API_KEY = "your_openweathermap_api_key"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

city = input("Enter city name: ")
response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})

if response.status_code == 200:
    data = response.json()
    print(f"Weather in {city}: {data['weather'][0]['description']}")
    print(f"Temperature: {data['main']['temp']}°C")
else:
    print("City not found!")
