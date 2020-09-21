import requests

class SlackWebhookApp:
    def __init__(self, wenhook_endpoint, user_name, user_icon):
        self.webhook_endpoint = wenhook_endpoint
        self.user_name = user_name
        self.user_icon = user_icon

    def post_message(self, message):
        dict_json = {'username': self.user_name, 'icon_emoji': self.user_icon, 'text': message}
        headers = {'Content-Type': 'application/json'}
        return requests.post(self.webhook_endpoint, headers=headers, json=dict_json)