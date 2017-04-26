import json

#tTEst
customer = {
    'id': 152352,
    'name':'강진수',
    'history': [
        {'date': '2015-03-11', 'item': 'iPhone'},
        {'date': '2016-02-23', 'item': 'Monitor'},
    ]
}

#JSON 인코딩
jsonString = json.dumps(customer, indent=4) #가독성을 위한 ident 변수

#출력
print(jsonString)
print(type(jsonString))
