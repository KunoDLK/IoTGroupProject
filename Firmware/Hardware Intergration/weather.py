import requests

city = 'Middlesbrough'
url = f'https://wttr.in/{city}?format=%t'  # %t = temperature

response = requests.get(url)

if response.status_code == 200:
    print(f"Temperature in {city}: {response.text.strip()}")
else:
    print("Failed to retrieve data")