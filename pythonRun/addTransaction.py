import requests

line = []

line.append({ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" })
line.append({ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" })
line.append({ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" })
line.append({ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" })
line.append({ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" })


for l in line:
    r =requests.post('https://gaywev1vs0.execute-api.us-east-1.amazonaws.com/addTransaction',json=l)
    print(r.text)

#add single transaction here:-
# input =
# r =requests.post('https://gaywev1vs0.execute-api.us-east-1.amazonaws.com/addTransaction',json=input)
# print(r.text)
