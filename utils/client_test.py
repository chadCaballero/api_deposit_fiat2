import requests
import json
import time
while True:
	token = requests.post('http://localhost:8000/v1/login', data=json.dumps({'username':'test','password':'test'}), headers={'Content-Type':'application/json'})
	#r = token.json()
	print(token.json())
	header = 'Bearer {}'.format(token.json()['access_token'])
	# response = requests.get('http://localhost:8000/v1/protected', headers={'Authorization': header})
	response = requests.get('http://localhost:8000/v1/protected', headers={'DataToken': header})
	print(json.loads(response.content))
	print(response.status_code)
	print(response.text)
	print(response.json())
	time.sleep(1)
