import requests

def upload():
    url = "http://localhost:8000/"
    file = {'file': open('static/bg.jpg', 'rb')}

    r = requests.post(url, files=file)
    print r.content

upload()
