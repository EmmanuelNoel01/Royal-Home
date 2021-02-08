import requests, json, uuid
from datetime import datetime,timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here
# a unit is a the room in a hostel or an apartment in  a condominium. It's what a single client would rent
class Accomodation(models.Model):
	image1 = models.ImageField(upload_to='properties/', blank=True)
	image2 = models.ImageField(upload_to='properties/', blank=True)
	image3 = models.ImageField(upload_to='properties/', blank=True)
	image4 = models.ImageField(upload_to='properties/', blank=True)
	image5 = models.ImageField(upload_to='properties/', blank=True)
	name = models.CharField(max_length=50)
	location = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	for_students = models.BooleanField(default=False)
	images = [image1,image2,image3,image4,image5]
	location_nick_name = models.TextField(default="Kla")
	university = models.CharField(max_length=100,default="Makerere University")

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("hostels:hostel_detail",kwargs={'pk': self.pk})

	def __str__(self):
		return self.name

class Units(models.Model):
	accomodation = models.ForeignKey(Accomodation, on_delete=models.CASCADE)
	unit_type = models.CharField(max_length=100)
	additional_services = models.TextField(default="Swimming Pool",blank=True)
	amount_per_month = models.IntegerField(default=0)
	minimum_number_of_months = models.IntegerField(default=4)
	actual_amount = models.IntegerField()
	capacity = models.IntegerField(default=1)
	available_number = models.IntegerField(default=0)
	is_self_contained = models.BooleanField(default=False)

	def __str__(self):
		return self.unit_type

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("e_commerce:hostel_detail", kwargs={'pk':self.accomodation.id})

class Peas(models.Model):
	seed = models.CharField(max_length=10000, default='*')
	slt = models.DateTimeField(default=timezone.now())

def peas_pass():
	state = {
		"is_acquired":False	
	}
	try:
		print("Checking for token in db")
		j = Peas.objects.get(pk=1)
	except Peas.DoesNotExist:
		print("No token in db")
		turl = "https://sandbox.momodeveloper.mtn.com/collection/token/"
		tpayload = {}
		theaders = {
  			'Ocp-Apim-Subscription-Key': 'ebb66531cc274d31b848dac1148a583d',
  			'Authorization': 'Basic NmQ5ZGFmOGItNWZmOC00ODM3LTgwN2ItNWQ5NzY3N2Y4ODExOjIzNTA1NWQ0ZjUyMTRhNDU4ZTlmZWIzODE0M2Q4YWQ3'
		}
		try:
			tresponse = requests.request("POST", turl, headers=theaders, data = tpayload)
		except Exception as e:
			state['is_acquired'] = False
			return state
		else:
			if tresponse.status_code == 200:
				seed = tresponse.json().get("access_token")
				j = Peas.objects.create(seed=seed)
				j.save()
				state['is_acquired'] = True
				state['t'] = j.seed
				return state
			else:
				state['is_acquired'] = False
				return state
	else:
		print("token present in db")
		et = timedelta(seconds=3600)
		ct = timezone.now()
		lt = j.slt
		d = ct - lt

		if d >= et:
			print("Token time expired")
			turl = "https://sandbox.momodeveloper.mtn.com/collection/token/"
			tpayload = {}
			theaders = {
  				'Ocp-Apim-Subscription-Key': 'ebb66531cc274d31b848dac1148a583d',
  				'Authorization': 'Basic NmQ5ZGFmOGItNWZmOC00ODM3LTgwN2ItNWQ5NzY3N2Y4ODExOjIzNTA1NWQ0ZjUyMTRhNDU4ZTlmZWIzODE0M2Q4YWQ3'
			}
			try:
				tresponse = requests.request("POST", turl, headers=theaders, data = tpayload)
			except Exception as e:
				state['is_acquired'] = False
				return state
			else:
				if tresponse.status_code == 200:
					seed = tresponse.json().get('access_token')
					j.seed = seed
					j.slt = datetime.now()
					state['is_acquired'] = True
					state['t'] = j.seed
					return state
				else:
					state['is_acquired'] = False
					state['status_code'] = tresponse.status_code
					return state
		else:
			print("Token in db used ")
			t = j.seed
			state['t'] = t
			state['is_acquired'] = True
			return state

class Payment(models.Model):
	payer = models.ForeignKey(User,on_delete=models.CASCADE)
	accomodation = models.ForeignKey(Accomodation,on_delete=models.CASCADE)
	amount = models.IntegerField(default=1)
	phone_number = models.CharField(max_length=10)
	telecom_network = models.CharField(default = "MTN", max_length=10,blank=True)
	unit = models.CharField(default = "Single Apartment",max_length=100)
	time_of_payment = models.DateTimeField(auto_now_add=True)
	is_complete = models.BooleanField(default=False)
	day_of_moving_in = models.DateTimeField(default=timezone.now())
	duration_of_occupancy = models.DurationField(blank=True)
	day_of_moving_out = models.DateTimeField(default = timezone.now(), blank=True )
	currency = models.CharField(max_length=10,default='UGX')
	x_Reference_Id = models.CharField(max_length=1000,default=str(uuid.uuid4()))
	status_code = models.CharField(max_length=5,default="1")
	is_assigned = models.BooleanField(default=False)

	def calculate_exit_date(self):
		exit_date = self.day_of_moving_in + self.duration_of_occupancy
		return exit_date

	def collect_money(self):
		url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
		payerMessage = ""
		payeeNote = ""

		info  = {
			'is_successful':False,
		}

		body = {
			'amount': self.amount,
			'currency':self.currency,
			'externalId':'ACC2020KLA',
			'payer':{
				'partyIdType':'MSISDN',
				'partyId':self.phone_number
			},
			'payerMessage':payerMessage,
			'payeeNote':payeeNote,    
		}
		# REQUEST TO PAY JSON DATA
		payload = json.dumps(body,indent=4)

		w = peas_pass()
		#PEAS
		if w.get("is_acquired"):
			print("Token acquired")
			token = w.get('t')
			authorization = 'Bearer '+token
			print(authorization)
			print("Authorization made")
			print(self.x_Reference_Id)
			headers = {
				'X-Reference-Id': self.x_Reference_Id,
				'X-Target-Environment': 'sandbox',
				'Ocp-Apim-Subscription-Key': 'ebb66531cc274d31b848dac1148a583d',
				'Content-Type': 'application/json',
				'Authorization': authorization
			}
			try:
				response = requests.request("POST", url, headers=headers, data = payload)
				print("Request to pay sent")
			except:
				info['is_successful'] = False
				info['reason'] = "Request to pay failed"
				print(info['reason'])
				return info
			else:
				print("Request to pay successful")
				print(response.status_code)
				if response.status_code == 202:
					print(response.status_code)
					print('Status code of request to pay is 202')
					def check():
						get_url = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/'+self.x_Reference_Id
						get_payload = {}
						get_headers = {
							'Authorization': authorization,
							'X-Target-Environment':'sandbox',
							'Ocp-Apim-Subscription-Key':'ebb66531cc274d31b848dac1148a583d'
						}
						get_response = requests.request("GET", get_url, headers=get_headers,data=get_payload)
						# print(get_response.status_code+"<= That is the status code for the check request to pay")
						# print(get_response.text)
						return get_response
							# CHECK STATUS
					payment_status = check()
					if payment_status.status_code == 200:
						print("request to pay status code is 200 Tick")
						if payment_status.json().get('status') == "PENDING":
							print("request to pay status is pending Tick")
							while payment_status.json().get('status') == "PENDING":
								print("Status is still pending")
								payment_status = check()
								print("Check function executed again")
								if payment_status.status_code == 200:
									print("Status code for check request to pay is 200")
									if payment_status.json().get('status') == "PENDING":
										print("Status still pending. While loop")
										continue
									elif payment_status.json().get('status') == "SUCCESSFUL":
										break
										info['is_successful'] = True
										info['status_code'] = payment_status.status_code
										print("Request to pay status is successful Yayyyyyyyyyyyyyyyy While loop")
										return info
									else:
										break
										info['is_successful'] = False
										info['status_code'] = payment_status.status_code
										print("Request to pay status is failed While loop")
										return info
								else:
									info['is_successful'] = False
									info['status_code'] = payment_status.status_code
									print("Status code for check request to pay is not 200.")
									return info
						elif payment_status.json().get('status') == "SUCCESSFUL":
							info['is_successful'] = True
							info['status_code'] = payment_status.status_code
							print("Request to pay status is successful Yayyyyyyyyyyyyyyyy")
							return info
						else:
							info['is_successful'] = False
							info['status_code'] = payment_status.status_code
							print("Request to pay status is Failed :(")
							return info
					else:
						info['is_successful'] = False
						info['status_code'] = payment_status.status_code
						print("Check Request to pay status code is not 200")
						return info
				else:
					info['is_successful'] = False
					info['status_code'] = response.status_code
					print("Check request to pay failed")
					print(response.json())
					return info
		else:
			info['is_successful'] = False
			print("Token was not acquired")
			return info

	def __str__(self):
		return self.payer.username +" paying to "+self.accomodation.name

def payment():
	j = Payment.objects.get(pk=1)
	return j

class RoomAssignment(models.Model):
	room_name = models.CharField(max_length=100,blank=True)
	payment = models.ForeignKey(Payment,on_delete=models.CASCADE)

	def __str__(self):
		return self.room_name

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("e_commerce:dashboard",kwargs={'accomodation_id':self.payment.accomodation.id})