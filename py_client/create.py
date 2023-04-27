import requests

headers = {'Authorization': 'Bearer 3eb47671be1e94bd2427bc3cec6487c4b38dd6c5'}
endpoint = "http://localhost:8000/api/products/"

data = {
    'title': 'This field is done',
    'price': 32.99
}
get_response = requests.post(endpoint, json=data, headers=headers)
# print(get_response.json())
