#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Helper function to validate and parse the json config file"""

import json
import sys
import traceback
import jsonschema
from rockit.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'log_name', 'control_machines', 'query_delay', 'humidity_enable_limit', 'humidity_disable_limit',
        'power_daemon', 'power_switch', 'dome_daemon', 'dome_closed_key', 'humidity_daemon', 'humidity_value_key'
    ],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'query_delay': {
            'type': 'number',
            'min': 0
        },
        'humidity_enable_limit': {
            'type': 'number',
            'min': 0,
            'max': 100
        },
        'humidity_disable_limit': {
            'type': 'number',
            'min': 0,
            'max': 100
        },
        'power_daemon': {
            'daemon_name': True,
            'type': 'string',
        },
        'power_switch': {
            'type': 'string',
        },
        'dome_daemon': {
            'daemon_name': True,
            'type': 'string',
        },
        'dome_closed_key': {
            'type': 'string',
        },
        'humidity_daemon': {
            'daemon_name': True,
            'type': 'string',
        },
        'humidity_value_key': {
            'type': 'string',
        },
        'humidity_valid_key': {
            'type': 'string',
        }
    }
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validation.validate_config(config_json, CONFIG_SCHEMA, {
            'daemon_name': validation.daemon_name_validator,
            'machine_name': validation.machine_name_validator
        })

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.query_delay = config_json['query_delay']

        self.power_daemon = getattr(daemons, config_json['power_daemon'])
        self.power_switch = config_json['power_switch']
        self.dome_daemon = getattr(daemons, config_json['dome_daemon'])
        self.dome_closed_key = config_json['dome_closed_key']
        self.humidity_daemon = getattr(daemons, config_json['humidity_daemon'])
        self.humidity_value_key = config_json['humidity_value_key']
        if 'humidity_valid_key' in config_json:
            self.humidity_valid_key = config_json['humidity_valid_key']
        else:
            self.humidity_valid_key = None
        self.humidity_enable_limit = config_json['humidity_enable_limit']
        self.humidity_disable_limit = config_json['humidity_disable_limit']
