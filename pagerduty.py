# Christian Mundwiler
# 1.22.24

# This python program allows the user to create an incident, update the last incident, and list all incidents in PagerDuty.

import os
import requests
from json import loads, dumps
from dotenv import load_dotenv

load_dotenv()

# get user data from .env
api_token = os.getenv("pd_token")
user_email = os.getenv("user_email")

# Create incident
# create payload
incident_payload = {
    "url": "https://api.pagerduty.com/incidents",
    "headers": {
        "Authorization": "Token token=" + api_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "From": user_email,
    },
    "body": {
        "incident": {
            "type": "incident",
            "title": "The server is on fire.",
            "urgency": "high",
            "body": {
                "type": "incident_body",
                "details": "A disk is getting full on this machine. You should investigate what is causing the disk to fill, and ensure that there is an automated process in place for ensuring data is rotated.",
            },
            "service": {"id": "PCM9730", "type": "service_reference"},
        }
    },
}
update_payload = {
    "url": "https://api.pagerduty.com/incidents/",
    "headers": {
        "Authorization": "Token token=" + api_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "From": user_email,
    },
    "body": {
        "incident": {
            "type": "incident_reference",
            "title": "The server is not on fire anymore",
            "urgency": "low",
        }
    },
}


def post_incident(incident_payload: dict):
    # send payload, receive response
    incident_response = requests.post(
        url=incident_payload["url"],
        headers=incident_payload["headers"],
        data=dumps(incident_payload["body"]),
    )

    return incident_response


# Update last incident
def update_incident(incident_id: str, update_payload: dict):
    # send payload
    # put last incident id into payload
    update_payload["url"] = update_payload["url"] + incident_id
    return requests.put(
        url=update_payload["url"],
        headers=update_payload["headers"],
        data=dumps(update_payload["body"]),
    )


# List all incidents
def get_all_incidents():
    # get incidents
    return requests.get(
        url=incident_payload["url"],
        headers=incident_payload["headers"],
        params={"limit": 100},
    )


# run functions
if __name__ == "__main__":
    # get and print incident response
    post_response = post_incident(incident_payload)
    print("\nCreate incident:")
    print("Status code: ", post_response.status_code)
    post_response_json = post_response.json()
    # dictionary comprehension to display pertinent info on specific keys
    keys = ["id", "type", "title", "urgency", "body"]
    new_dict = {
        key: value
        for (key, value) in post_response_json.get("incident", {}).items()
        if key in keys
    }
    print(
        "Title, urgency, id, type, and body of created incident:\n",
        dumps(new_dict, separators=(",", " : "), indent=4),
    )

    # get last incident id
    incident_id = post_response_json["incident"]["id"]
    # update incident
    update_response = update_incident(incident_id, update_payload)
    update_response_json = update_response.json()

    # print status code and pertinent info
    print("\nUpdate incident:")
    print("Status code:", update_response.status_code)
    print("Incident id:", post_response_json.get("incident", {}).get("id"))

    # print API response
    print("Updated title:", update_response_json["incident"]["title"])
    print("Updated urgency:", update_response_json["incident"]["urgency"])

    # get incidents and put into json
    get_response = get_all_incidents()
    get_response_json = get_response.json()

    # print status code and incident ids
    print("\nStatus code:", get_response.status_code)
    print(
        "All incidents by id:",
        # list comp to get incident ids
        [item.get("id") for item in get_response_json["incidents"]],
    )
