import nltk
from api_cal.gcal import gcal

dtags = {
    "date": 'formal',  "event": 'formal', "wedding": 'formal',
    "run": 'sportswear', "jog": "sportswear", "yoga": "sportswear",
    "bus": 'casual'
    # 'business-casual': [""],
    # 'sportswear': ["run", "jog", "yoga"],
    # 'formal': ["date", "event", "wedding"],
    # 'casual': [""],
}

def get_dresscode():
    cal = gcal.get_today()

    dresscodes = []

    for c in cal:
        words = nltk.word_tokenize(c['summary'])

        for w in words:
            try:
                d_code = dtags[w]
                if d_code:
                    dresscodes.append(d_code)
                    # print "Tag: %s; Dresscode: %s \n" % (w, d_code)
            except:
                pass

    print dresscodes

# import sklearn
