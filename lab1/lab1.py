import requests
print(requests.__version__)

request = requests.get('https://raw.githubusercontent.com/willzawong/cmput404-labs/main/lab1/lab1.py')
print(request.content)