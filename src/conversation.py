import json
import uuid
import requests

class Conversation:
    parent_id: str
    conversation_id: str
    headers: dict

    def __init__(self, auth_token: str):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }

        self.reset()

    def reset(self):
        self.conversation_id = None
        self.parent_id = str(uuid.uuid4())

    def get_response(self, prompt):
        req_body = {
            'action': 'next',
            'messages': [
                {
                    'id': str(uuid.uuid4()),
                    'role': 'user',
                    'content': {
                        'content_type': 'text',
                        'parts': [prompt]
                    }
                }
            ],
            'conversation_id': self.conversation_id,
            'parent_message_id': self.parent_id,
            'model': 'text-davinci-002-render'
        }

        # Make POST request
        response = requests.post('https://chat.openai.com/backend-api/conversation', headers=self.headers, data=json.dumps(req_body))

        try: 
            # Get completion from response
            response = response.text.splitlines()[-4][6:]
            response = json.loads(response)
        except Exception as e:
            print(response.text)

        # Update conversation_id and parent_id
        self.conversation_id = response['conversation_id']
        self.parent_id = response['message']['id']

        message = response['message']['content']['parts'][0]
        return message
