#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2017, Wayne Witzel III <wayne@riotousliving.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: tower_host
version_added: "2.3"
author: "Wayne Witzel III (@wwitzel3)"
short_description: create, update, or destroy Ansible Tower host.
description:
    - Create, update, or destroy Ansible Tower hosts. See
      U(https://www.ansible.com/tower) for an overview.
options:
    name:
      description:
        - The name to use for the host.
      required: True
    description:
      description:
        - The description to use for the host.
    inventory:
      description:
        - Inventory the host should be made a member of.
      required: True
    enabled:
      description:
        - If the host should be enabled.
      type: bool
      default: 'yes'
    variables:
      description:
        - Variables to use for the host. Use C(@) for a file.
    state:
      description:
        - Desired state of the resource.
      choices: ["present", "absent"]
      default: "present"
extends_documentation_fragment: tower
'''


EXAMPLES = '''
- name: Add tower host
  tower_host:
    name: localhost
    description: "Local Host Group"
    inventory: "Local Inventory"
    state: present
    tower_config_file: "~/tower_cli.cfg"
    variables:
      example_var: 123
'''


import os

from ansible.module_utils.ansible_tower import TowerModule, tower_auth_config, tower_check_mode, HAS_TOWER_CLI

try:
    import tower_cli
    import tower_cli.exceptions as exc

    from tower_cli.conf import settings
except ImportError:
    pass


def main():
    argument_spec = dict(
    )
    module = TowerModule(argument_spec=argument_spec, supports_check_mode=True)

    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        host = tower_cli.get_resource('host')

        try:
            result = host.list()
            json_output = {'hosts': result}
        except (exc.NotFound) as excinfo:
            module.fail_json(msg='Failed to update host, inventory not found: {0}'.format(excinfo), changed=False)
        except (exc.ConnectionError, exc.BadRequest, exc.AuthError) as excinfo:
            module.fail_json(msg='Failed to update host: {0}'.format(excinfo), changed=False)



    module.exit_json(**json_output)


if __name__ == '__main__':
    main()
