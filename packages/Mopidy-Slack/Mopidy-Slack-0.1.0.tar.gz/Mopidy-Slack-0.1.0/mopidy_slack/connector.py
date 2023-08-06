from slack import WebClient
import slack

class SlackConnector():

    # run_async allows to disable the slack client event loop
    def __init__(self, config, run_async):
        self.config = config
        self.slack_client = WebClient(token=config["slack"]['bot_token'], run_async=run_async)

    def send_message(self, body, channel):
        message = {
            "channel": channel,
            "text": body,
        }
        self.slack_client.chat_postMessage(**message)
