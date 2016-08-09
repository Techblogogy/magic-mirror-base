import requests, json

def upload():
    url = "http://52.174.96.93/"
    file = {'file': open('static/bg.jpg', 'rb')}

    r = requests.post(url, files=file)
    cnt = json.loads(r.content)

    print cnt['dress']

upload()
