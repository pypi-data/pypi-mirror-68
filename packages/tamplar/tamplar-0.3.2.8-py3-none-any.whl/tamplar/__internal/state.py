import json
import os

from tamplar.__internal import utils


def read_config():
    if not os.path.exists(utils.tamplar_config):
        return {'service': 'stop'}
    with open(utils.tamplar_config) as fd:
        state = json.load(fd)
    return state


# def check_ran_service(state):
#     if state['service']:
