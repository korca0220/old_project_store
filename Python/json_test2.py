import json

jsonString = '{"id": 152352, "name":"Gang-Jin-Su", "history": [{"date": "2015-03-11", "item": "iPhone"}, {"date": "2016-02-23", "item": "Monitor"}]}'

#JSON 디코딩
dict = json.loads(jsonString)

print(dict['name'])
for h in dict['history']:
    print(h['date'], h['item'])
