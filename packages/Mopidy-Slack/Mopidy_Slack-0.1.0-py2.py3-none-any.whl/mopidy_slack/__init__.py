from __future__ import unicode_literals

import logging
import os

from .song_notification import SongNotification
from .command import help, request, next, keep, start
from .connector import SlackConnector

import tornado.web
from mopidy import config, ext
import json
import time

__version__ = '0.1.0'
logger = logging.getLogger(__name__)

class EventsHandler(tornado.web.RequestHandler):
    def initialize(self, core, slack_connector, listeners):
        self.core = core
        self.slack_connector = slack_connector
        self.listeners = listeners

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        callType = data['type']
        if callType == "url_verification":
            self.verify_url(data)
        
        if callType == "event_callback":
            event = data["event"]
            if event["type"] == "message":
                self.apply_message(event)

    def apply_message(self, event):
        text = event["text"]
        logger.debug("[SlackHandler] got message: {} from {} on chan {}".format(text, event["user"], event["channel"]))
        for listener in self.listeners:
            if text.startswith(listener.command()):
                message_back = listener.action(text, event["user"], event["channel"])
                self.slack_connector.send_message(message_back, event["channel"])
        self.set_header("Content-type","application/json")
        self.write({ 'status' : 'ok' })

    def verify_url(self, data):
        challenge = data['challenge']
        self.set_header("Content-type","application/json")
        self.write({ 'challenge' : challenge })
       

class Extension(ext.Extension):

    dist_name = 'Mopidy-Slack'
    ext_name = 'slack'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['bot_token'] = config.String()
        return schema
    
    def factory(self, config, core):
        next_counter = next.NextCounter()
        channel_holder = ChannelHolder()
        self.song_notification = SongNotification.start(SlackConnector(config, False), next_counter, channel_holder)
        self.listeners = []
        self.listeners.append(start.StartListener(core, channel_holder))
        self.listeners.append(request.RequestListener(core))
        self.listeners.append(next.NextListener(core, next_counter))
        self.listeners.append(keep.KeepListener(core, next_counter))
        # list listeners usages
        self.listeners.append(help.HelpListener(self.listeners))
        return [
            ('/events', EventsHandler, {"core": core, "slack_connector": SlackConnector(config, True), "listeners": self.listeners})
        ]

    def setup(self, registry):
        registry.add('http:app', {
            'name': self.ext_name,
            'factory': self.factory
        })

class ChannelHolder():

    def __init__(self):
        self.channel = ""

    def set_channel(self, channel):
        self.channel = channel

    def get_channel(self):
        return self.channel


