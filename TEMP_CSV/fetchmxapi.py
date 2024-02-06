import requests
domain='google.com'
url = f"https://api.securitytrails.com/v1/history/{domain}/dns/mx"
headers = {"APIKEY": "OEqZ2i9fIfFFLyOgz"}
response = requests.get(url, headers=headers)
print(response)
# mx_records = response.json()["records"]