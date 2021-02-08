import requests, json, uuid
from datetime import datetime,timedelta
from .models import Peas

def peas_pass():
	state = {
		"is_acquired":False	
	}
	try:
		j = Peas.objects.get(pk=1)
	except Peas.DoesNotExist:
		url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
		payload = {}
		headers = {
  			'Ocp-Apim-Subscription-Key': 'ebb66531cc274d31b848dac1148a583d',
  			'Authorization': 'Basic NmQ5ZGFmOGItNWZmOC00ODM3LTgwN2ItNWQ5NzY3N2Y4ODExOjIzNTA1NWQ0ZjUyMTRhNDU4ZTlmZWIzODE0M2Q4YWQ3'
		}
		try:
			response = requests.request("POST", url, headers=headers, data = payload)
		except Exception as e:
			state['is_acquired'] = False
			return state
		else:
			if response.status_code == 200:
				seed = response.json().get("access_token")
				j = Peas.objects.create(seed=seed)
				j.save()
				state['is_acquired'] = True
				state['t'] = j.seed
				return state
			else:
				state['is_acquired'] = False
				return state
	else:
		et = timedelta(seconds=3600)
		ct = datetime.now()
		lt = j.slt
		d = ct - lt

		if d >= et:
			url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
			payload = {}
			headers = {
  				'Ocp-Apim-Subscription-Key': 'ebb66531cc274d31b848dac1148a583d',
  				'Authorization': 'Basic NmQ5ZGFmOGItNWZmOC00ODM3LTgwN2ItNWQ5NzY3N2Y4ODExOjIzNTA1NWQ0ZjUyMTRhNDU4ZTlmZWIzODE0M2Q4YWQ3'
			}
			try:
				response = requests.request("POST", url, headers=headers, data = payload)
			except Exception as e:
				state['is_acquired'] = False
				return state
			else:
				if response.status_code == 200:
					seed = response.json().get('access_token')
					j.seed = seed
					j.slt = datetime.now()
					state['is_acquired'] = True
					state['t'] = j.seed
					return state
				else:
					state['is_acquired'] = False
					state['status_code'] = response.status_code
					return state
		else:
			t = j.seed
			state['t'] = t
			state['is_acquired'] = True
			return state