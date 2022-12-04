import os
from conversation import Conversation

def get_input():
    return input('You: ')

if __name__ == '__main__':
    # get auth token from env
    auth_token = os.environ['CHAT_GPT_TOKEN']
    conv = Conversation(auth_token=auth_token)

    while True:
        prompt = get_input()
        response = conv.get_response(prompt).strip()
        print(f'> {response}\n')