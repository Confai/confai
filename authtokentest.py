import requests

headers = {
    'Authorization': 'Token 2cf67c03e28500a90bd397fe95fa65b30304bc44',
}

response = requests.get('http://localhost:8000/api/symbol/AAPL', headers=headers)

print(response.json())