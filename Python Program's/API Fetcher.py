import requests

url = "https://api.spacexdata.com/v4/launches/latest"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Mission: {data['name']}")
    print(f"Date: {data['date_utc']}")
else:
    print("Failed to fetch data!")
