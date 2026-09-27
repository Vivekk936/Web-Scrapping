import requests
url= "http://127.0.0.1:8000/blogs/python-intro"
response = requests.get(url=url)
print(response.text)