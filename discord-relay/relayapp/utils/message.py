__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
relayer.py
- Sends requests to the Statesman bot
"""


import os
import logging
import discord


def is_targeted(message:object):
    """
    """

    channel = message.channel
    logging.debug("channel: %s", channel)
    author = message.author
    logging.debug("author: %s", author)

    # if channel is DM
    logging.debug("channel.type: %s", channel.type)
    if channel.type == discord.ChannelType.private:
        logging.debug("channel type is private; returning True")
        return True

    body = message.content
    logging.debug("body: %s", body)

    if body.startswith('!statesman') or body.startswith('!sb'):
        return True

    return False
