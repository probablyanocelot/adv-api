import requests

r = requests.post('http://192.168.80.4:5000/api/bank', properties='json_object', json={
    'something': 'somethinge else', 'something': 'somethinge else',
    'something': 'somethinge else', 'something': 'somethinge else',
    'something': 'somethinge else', })
