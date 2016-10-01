import requests, json

def upload():
    url = "http://13.95.237.230:5000/"
    file = {'file': open('pic2.jpg', 'rb')}

    r = requests.post(url, files=file)
    print r
    cnt = json.loads(r.content)

    print cnt

upload()
