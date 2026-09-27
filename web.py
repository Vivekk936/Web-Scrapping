import requests
url = "http://127.0.0.1:8000/static/app1/images/2.jpg"

user={
    "User-Agent":"""" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 """
}

response = requests.get(url = url, headers = user)
pic= response.content

f=open("2.jpg","wb")
f.write(pic)
