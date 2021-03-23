#
# This file is part of dehumidifierd.
#
# dehumidifierd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dehumidifierd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dehumidifierd.  If not, see <http://www.gnu.org/licenses/>.

"""Helper function to validate and parse the json config file"""

import json
import sys
import traceback
import jsonschema
from warwick.observatory.common import daemons, IP

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


class ConfigSchemaViolationError(Exception):
    """Exception used to report schema violations"""
    def __init__(self, errors):
        message = 'Invalid configuration:\n\t' + '\n\t'.join(errors)
        super(ConfigSchemaViolationError, self).__init__(message)


def __create_validator():
    """Returns a template validator that includes support for the
       custom schema tags used by the observation schedules:
            daemon_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.daemons address book
            machine_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.IP address book
    """
    validators = dict(jsonschema.Draft4Validator.VALIDATORS)

    # pylint: disable=unused-argument
    def daemon_name(validator, value, instance, schema):
        """Validate a string as a valid daemon name"""
        try:
            getattr(daemons, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid daemon name'.format(instance))

    def machine_name(validator, value, instance, schema):
        """Validate a string as a valid machine name"""
        try:
            getattr(IP, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid machine name'.format(instance))
    # pylint: enable=unused-argument

    validators['daemon_name'] = daemon_name
    validators['machine_name'] = machine_name
    return jsonschema.validators.create(meta_schema=jsonschema.Draft4Validator.META_SCHEMA,
                                        validators=validators)


def validate_config(config_json):
    """Tests whether a json object defines a valid environment config file
       Raises SchemaViolationError on error
    """
    errors = []
    try:
        validator = __create_validator()
        for error in sorted(validator(CONFIG_SCHEMA).iter_errors(config_json),
                            key=lambda e: e.path):
            if error.path:
                path = '->'.join([str(p) for p in error.path])
                message = path + ': ' + error.message
            else:
                message = error.message
            errors.append(message)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        errors = ['exception while validating']

    if errors:
        raise ConfigSchemaViolationError(errors)


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validate_config(config_json)

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
