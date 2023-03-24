# Copyright (c) 2022, Red Hat, Inc.
# Copyright (c) 2022, Guido Grazioli <ggraziol@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
  name: pbkdf2_hmac
  author: ggraziol@redhat.com
  version_added: '1.1.0'
  short_description: Generate a salted PBKDF2_HMAC password hash
  description:
    - Generate a salted one-way PBKDF2 HMAC_password hash
  positional: _input
  options:
    _input:
      description:
      type: string
      required: true
    hexsalt:
      description: salt for password hashing, in uppercase hexstring format
      type: string
      required: true
    iterations:
      description: number of iterations, default 1024
      type: int
      required: false
'''

EXAMPLES = '''
# generate pbkdf2_hmac hash in hex format for 'password' with given salt
- name: Generate salted PBKDF2_HMAC password hash
  ansible.builtin.debug:
    msg: >-
      {{ 'password' | pbkdf2_hmac(hexsalt='7BD6712B68F9BD60B51D77EBD851A21F63E61F2B52301E7CA38DD1602CA662EB' }}
'''

RETURN = '''
  _value:
    description: the uppercase hexstring representation of the hashed password
    type: string
'''

from ansible.errors import AnsibleFilterError

import base64
import sys
import hashlib


def pbkdf2_hmac(string, hexsalt, iterations=1024):
    key = hashlib.pbkdf2_hmac(
        hash_name='sha1',
        password=str.encode(string),
        salt=bytearray.fromhex(hexsalt),
        iterations=iterations,
        dklen=64
    )
    return key.hex().upper()


class FilterModule(object):

    def filters(self):
        return {
            # pbkdf2_hmac
            'pbkdf2_hmac': pbkdf2_hmac
        }
