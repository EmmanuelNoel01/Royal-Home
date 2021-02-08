import requests, json, uuid

class Payment():
    def __init__(self,amount,phone_number,currency,X_Reference_Id):
        self.amount = amount 
        self.phone_number = phone_number
        self.currency = currency
        self.X_Reference_Id = X_Reference_Id

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

        token_url = "https://sandbox.momodeveloper.mtn.com/collection/token/"

        token_payload = {}
        token_headers = {
            'Ocp-Apim-Subscription-Key': 'ebb66531cc274d31b848dac1148a583d',
            'Authorization': 'Basic NmQ5ZGFmOGItNWZmOC00ODM3LTgwN2ItNWQ5NzY3N2Y4ODExOjIzNTA1NWQ0ZjUyMTRhNDU4ZTlmZWIzODE0M2Q4YWQ3'
        }
        try:
            token_response = requests.request("POST", token_url, headers=token_headers, data = token_payload)
        except Exception as e:
            info['is_successful'] = False
            info['reason'] = "Failed to acquire access_token"
            return info
        else:
            #BEARER TOKEN
            if token_response.status_code == 200:
                token = token_response.json().get('access_token')
                authorization = 'Bearer '+token

                headers = {
                    'X-Reference-Id': self.X_Reference_Id,
                    'X-Target-Environment': 'sandbox',
                    'Ocp-Apim-Subscription-Key': 'ebb66531cc274d31b848dac1148a583d',
                    'Content-Type': 'application/json',
                    'Authorization': authorization
                }
                try:
                    response = requests.request("POST", url, headers=headers, data = payload)
                except:
                    info['is_successful'] = False
                    info['reason'] = "Request to pay failed"
                    return info
                else:
                    if response.status_code == 202:
                        # print('Request to pay sent')
                        # CHECK STATUS OF REQUEST TO PAY
                        def check():
                            get_url = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/'+self.X_Reference_Id
                            get_payload = {}
                            get_headers = {
                                'Authorization': authorization,
                                'X-Target-Environment':'sandbox',
                                'Ocp-Apim-Subscription-Key':'ebb66531cc274d31b848dac1148a583d'
                            }
                            get_response = requests.request("GET", get_url, headers=get_headers,data=get_payload)
                            # print(get_response.status_code)
                            # print(get_response.text)
                            return get_response
                            # CHECK STATUS
                        payment_status = check()
                        if payment_status.status_code == 200:
                            if payment_status.json().get('status') == "PENDING":
                                while payment_status.json().get('status') == "PENDING":
                                    payment_status = check()
                                    if payment_status.status_code == 200:
                                        if payment_status.json().get('status') == "PENDING":
                                            continue
                                        elif payment_status.json().get('status') == "SUCCESSFUL":
                                            break
                                            info['is_successful'] = True
                                            info['status_code'] = payment_status.status_code
                                            return info
                                        else:
                                            break
                                            info['is_successful'] = False
                                            info['status_code'] = payment_status.status_code
                                            return info
                                    else:
                                        info['is_successful'] = False
                                        info['status_code'] = payment_status.status_code
                                        return info
                            elif payment_status.json().get('status') == "SUCCESSFUL":
                                info['is_successful'] = True
                                info['status_code'] = payment_status.status_code
                                return info
                            else:
                                info['is_successful'] = False
                                info['status_code'] = payment_status.status_code
                                return info
                        else:
                            info['is_successful'] = False
                            info['status_code'] = payment_status.status_code
                            return info
                    else:
                        info['is_successful'] = False
                        info['status_code'] = response.status_code
                        return info
            else:
                info['is_successful'] = False
                info['status_code'] = token_response.status_code
                return info
# url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"

# amount = 5.0
# currency = 'EUR'
# externalId = '02463547'
# partyId = '0781666410'
# payerMessage = 'Please Pay'
# payeeNote = 'Hi'

# print(collect_money(url,amount,currency,externalId,partyId,payerMessage,payeeNote))
x_id = str(uuid.uuid4())
payment = Payment(300,'0781666410','EUR',x_id)
print(payment.collect_money())