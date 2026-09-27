import requests

url = "http://127.0.0.1:8000/posts/"

payload = {
    "title": "Greetings",
    "content": "Hello World"
}

response = requests.post(url=url, data=payload)


print(response.text)