import os
from dotenv import load_dotenv
import urllib3
import requests
import time
import dotenv
load_dotenv()
urllib3.disable_warnings()

class CopilotProvider():

    def __init__(self):
        self.secret = os.getenv("psr_copilot_secret")

    def generate(self,notes: str,) -> str:

        headers = {
            "Authorization":
                f"Bearer {self.secret}",
            "Content-Type": "application/json"
        }
        conversation = requests.post(os.getenv("copilot_url"),
            headers=headers,
            verify=False
        ).json()

        conversation_id = (
            conversation["conversationId"]
            if "conversationId" in conversation
            else conversation["conversation"]["id"]
        )
        print(f"Id {conversation_id}")
        print("\n\n".join(notes))

        payload = {
            "type": "message",
            "from": {
                "id": "discovery-agent",
                "name": "Discovery Agent"
            },
            "text": "\n\n".join(notes),
        }
        #print(f"url: {os.getenv('copilot_url')}/{conversation_id}/activities")
        response = requests.post(os.getenv("copilot_url") + f"/{conversation_id}/activities",
            headers=headers,
            json=payload,
            verify=False
        )
        '''
        print("REQUEST BODY:")
        print(response.request.body)

        print("REQUEST HEADERS:")
        print(response.request.headers)

        print("STATUS:")
        print(response.status_code)

        print("RESPONSE:")
        print(response.text)
        #print(f"Response: {response.json()}")
        '''

        time.sleep(15)

        activities = requests.get(
            os.getenv("copilot_url") + f"/{conversation_id}/activities",
            headers=headers,
            verify=False
        ).json()
        #print(f"Activities: {activities}")

        messages = [
                activity.get("text")
                for activity in activities["activities"]
                if (
                    activity.get("type") == "message"
                    and activity.get("text")
                    and activity.get("from", {}).get("id")
                    != "discovery-agent"
                )
            ]

        return messages[-1]