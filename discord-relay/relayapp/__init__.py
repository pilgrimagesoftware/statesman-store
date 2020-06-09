__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
relayapp
- Discord relay application package root
"""


import logging
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--debug', help='enable debug logging', action='store_true')
args = parser.parse_args()


FORMAT = '[%(levelname)s %(filename)s:%(lineno)d] - %(message)s'

loglevel = logging.INFO
if args.debug:
    loglevel = logging.DEBUG
logging.basicConfig(level=loglevel, format=FORMAT)
log = logging.getLogger(__name__)
