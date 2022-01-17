import requests

args = { "points": 5000 } # change points to spend here

r =requests.post('https://gaywev1vs0.execute-api.us-east-1.amazonaws.com/spend',json=args)
print(r.text)





