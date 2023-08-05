"""Database Utils

"""

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'xiawu@newtonproject.org'

import logging
import base58
import binascii
from .crypto import HDPrivateKey, HDPublicKey, HDKey


logger = logging.getLogger(__name__)


def gen_address_from_xpub(xpub, index):
    acct_pub_key = HDKey.from_b58check(xpub)
    keys = HDKey.from_path(
        acct_pub_key, '{change}/{index}'.format(change=0, index=index))
    address = keys[-1].address()
    print('Account address: ' + address)
    return address


def gen_private_from_xpriv(xpriv, index):
    x_private = HDKey.from_hex(xpriv)
    keys = HDKey.from_path(
        x_private, '{change}/{index}'.format(change=0, index=index))
    private_key = keys[-1]
    return private_key._key.to_hex()


def new_to_hex(new_address):
    return new_address_to_hex_address(new_address)


def new_address_to_hex_address(new_address):
    return "0x%s" % base58.b58decode_check(new_address[3:]).hex().lower()[6:]


def hex_to_new(hex_address, chain_id):
    return hex_address_to_new_address(hex_address, chain_id)


def hex_address_to_new_address(hex_address, chain_id):
    if hex_address.startswith('0x'):
        hex_address = hex_address[2:]
    hex_chain_id = hex(chain_id)[2:][-8:]
    if (len(hex_chain_id) % 2) == 1:
        hex_chain_id = '0' + hex_chain_id
    num_sum = hex_chain_id + hex_address
    data = base58.b58encode_check(b'\0' + binascii.a2b_hex(num_sum))
    new_address = 'NEW' + data.decode()
    return new_address


def is_new_address(address):
    return len(address) == 39 and address[:3] == "NEW"


def read_newchain_block():
    return ""
