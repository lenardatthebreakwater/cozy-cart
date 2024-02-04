from dotenv import load_dotenv
import requests
import base64
import json
import os

load_dotenv()

def paymongo_request(line1, city, state, postal_code, country, name, email, phone, line_items):
	url = "https://api.paymongo.com/v1/checkout_sessions"
	payload = { "data": { "attributes":{
		"billing": {
			"address": {
				"line1": line1,
          		"city": city,
          		"state": state,
          		"postal_code": postal_code,
          		"country": country
        	},
        	"name": name,
        	"email": email,
        	"phone": phone
    	},
    	"line_items": line_items,
    	"payment_method_types": ["gcash"],
    	"send_email_receipts": True,
    	"show_line_items": True
    }}}
	paymongo_secret_key = os.getenv("PAYMONGO_SECRET_KEY")
	b64encoded_paymongo_secret_key = base64.b64encode(paymongo_secret_key.encode()).decode()
	headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Basic {b64encoded_paymongo_secret_key}"}
	response = requests.post(url, json=payload, headers=headers)
	response_dict = json.loads(response.text)
	return response_dict["data"]["id"], response_dict["data"]["attributes"]["checkout_url"]
