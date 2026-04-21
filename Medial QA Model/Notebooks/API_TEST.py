import requests

API_KEY = "AIzaSyCioBuoKGWKhThS4WOS-YzNpeoB0TMJwAE"
CX = "b34da2bf587c940aa"

url = "https://www.googleapis.com/customsearch/v1"
params = {
    "key": API_KEY,
    "cx": CX,
    "q": "Heart attack symptoms"
}

response = requests.get(url, params=params)
print(response.status_code)
print(response.json())