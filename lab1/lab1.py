import requests
print(requests.__version__)

request = requests.get('https://www.google.ca/')
print(request)