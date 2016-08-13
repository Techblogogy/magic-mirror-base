import requests, json

def upload():
    url = "http://13.95.237.230:8000/"
    file = {'file': open('static/bg.jpg', 'rb')}

    r = requests.post(url, files=file)
    cnt = json.loads(r.content)

    print cnt['dress']

upload()
