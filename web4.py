import requests
url = "http://127.0.0.1:8000/posts/"
params={
    "offset": "10",
}
response = requests.get(url=url, data=params)
print(response.url)