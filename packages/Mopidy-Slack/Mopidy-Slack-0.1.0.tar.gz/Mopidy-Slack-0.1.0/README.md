# Mopidy-Slack

[Mopidy](http://www.mopidy.com/>) extension for controlling music from
[Slack](https://api.slack.com/>).

Requires you to create a slack app in your workspace.

## Installation

Install by running: `pip install Mopidy-Slack`

## Configuration

### Slack App

To work you need to [create a Slack App](https://api.slack.com/apps) and install it to your workspace.
This way you get the bot user OAuth access token, useful later
![](docs/bot_token.png)

Then you need to activate the events API. This API requires the URL on which your mopidy instance is callable. If you are testing it on local you can use [ngork](https://ngrok.com/>) to expose your instance on the web. After you domain, add the endpoint `/slack/events`.

You also need to subcribe the app to the event `message.channels`. This way the app will receive all messages posted in channel where its had been added. Beware not to post confidential data :warning:
![](docs/events.png)

### Mopidy 

In mopidy configuration, you must add your Slack app's Bot User OAuth Access Token using `bot_token`

So configuration is:
```
[slack]
bot_token=xoxb-123456789123-1234567891234-xxx
```

## Extension commands

All available commands are available in the folder `command`. Currently there is :
 - `help` Display the help
 - `keep` Ask to keep the current playing song
 - `next` Ask to skip the current playing song
 - `request song_name [- artist_name]` Request a new song to be played
 - `start [playlist_name]` Start the radio broadcast. The bot will look for playlist starting with given name of fallback to the default playlist

Note that there is no `/` before the command, this way we are not using the slack app commands. If we used this mecanism, the configuration of app would be long and difficult to maintain.

## Project resources

- [Blog article](https://ablanchard.me)

## Changelog

### v0.1.0 (2020-05-13)
 - Initial release.
