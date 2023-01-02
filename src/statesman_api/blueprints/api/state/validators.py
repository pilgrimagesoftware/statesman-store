__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
validators.py
- Validators for API calls
"""


from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema


state_action_schema = {
    '$id': 'http://sweetrpg.com/schemas/state_action.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'server_id': {
            'type': 'string',
        },
        'action': {
            'type': 'string'
        },
    },
    'required': ['server_id', 'action']
}

class StateActionInput(Inputs):
    json = [JsonSchema(schema=state_action_schema)]
