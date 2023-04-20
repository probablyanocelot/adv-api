import json
import requests
import os

file_name = 'bank.json'


def do_post(file_name):
    with open(file_name) as file:

        bank = json.load(file)
        print(bank)

        r = requests.post('http://localhost:8001/api/bank', data=bank)
        return print(r)


# r = requests.get('http://localhost:8001/api/bank')

do_post(file_name)
