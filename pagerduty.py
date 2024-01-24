# Christian Mundwiler
# 1.22.24

# This python program allows the user to create an incident, update the last incident, and list all incidents in PagerDuty.
# Specific requirements:

# 1.    Create an incident. These are the only fields required for the program: Type, Title, Urgency, Body.
# 2.    Update an incident. These are the only fields required for the program to update: Title, Urgency.
# 3.    List all incidents.

import os
import requests
from json import loads, dumps
from dotenv import load_dotenv
load_dotenv()

api_token = os.getenv('pd_token')

# Create incident
    
# create payload 
incident_payload = {
  "url" : "https://api.pagerduty.com/incidents",

  "headers" : {
      "Authorization": "Token token=" + api_token,
      "Content-Type":"application/json",
      "Accept":"application/json",
      "From":"christian.mundwiler@ucdenver.edu"
      },

  "body" : {
    "incident": {
      "type": "incident",
      "title": "The server is on fire.",
      "urgency": "high",
      "body": {
        "type": "incident_body",
        "details": "A disk is getting full on this machine. You should investigate what is causing the disk to fill, and ensure that there is an automated process in place for ensuring data is rotated."
      },
      "service": {
        "id": "PCM9730",
        "type": "service_reference"
      }
    }
  }
}
update_payload = {
    "url" : "https://api.pagerduty.com/incidents/",

    "headers" : {
        "Authorization": "Token token=" + api_token,
        "Content-Type":"application/json",
        "Accept":"application/json",
        "From":"christian.mundwiler@ucdenver.edu"
        },

    "body" : {
        "incident": {
        "type": "incident_reference",
        "status": "resolved",
        "urgency": "low"
        }
    }
    }
def post_incident(incident_payload: dict):
    # send payload, receive response
    incident_response = requests.post(url = incident_payload["url"], headers = incident_payload["headers"], data = dumps(incident_payload["body"]))

    return incident_response
    # json and prettify data 
    # dumps(incident_response.json(), separators=(",",": "), indent=4)

# Update last incident
def update_incident(incident_id: str, update_payload: dict):
    # Create payload
    
    # send payload
    # get last incident id
    update_payload["url"] = update_payload["url"] + incident_id
    return requests.put(url = update_payload["url"], headers = update_payload["headers"], data = dumps(update_payload["body"]))

    # json and prettify data 
    # json_update_data = dumps(update_response.json(), separators=(","," : "), indent=4)

    # return json_update_data


# List all incidents
def get_all_incidents():
    # get incidents
    return requests.get(url = incident_payload["url"], headers = incident_payload["headers"], params={"limit":100})

    # json and prettify data 
    # json_incidents_data = dumps(incidents_response.json()["incidents"], separators=(","," : "), indent=4)



# Step 6: Automate tests

if __name__ == "__main__":
    post_response = post_incident(incident_payload) 
    # print status code and response

    print("Create incident")
    print("Status code: ", post_response.status_code)
    post_response_json = post_response.json()
    keys = ["id", "type", "title", "urgency", "body"]
    new_dict = {key:value for (key, value) in post_response_json.get("incident", {}).items() if key in keys}
    print("Title, urgency, id, type, and body of created incident:\n", dumps(new_dict, separators=(","," : "), indent=4))
    incident_id = post_response_json["incident"]["id"]

    update_response = update_incident(incident_id, update_payload)
    update_response_json = update_response.json()
    # print status code
    print("\nStatus code:", update_response.status_code)
    print("Updated incident id:", post_response_json.get("incident", {}).get("id"))

    # print API response
    print("Updated status:", update_response_json['incident']['status'])
    print("Updated urgency:", update_response_json['incident']['urgency'])

    get_response = get_all_incidents()
    get_response_json = get_response.json()

    # print API response
    print("\nStatus code:", get_response.status_code)
    print(get_response_json.get("limit"))
    print("All incidents by id:", [item.get("id") for item in get_response_json["incidents"]])