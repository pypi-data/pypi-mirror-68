#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

""" Base58 address functions.

Base58 encoding of public keys and scripts as addresses.
"""

from typing import Optional, Tuple

from .alias import Key, Octets, Script, String
from .base58 import b58decode, b58encode
from .bech32address import b32address_from_witness, witness_from_b32address
from .hashes import hash160_from_pubkey, hash160_from_script, hash256_from_script
from .network import _P2PKH_PREFIXES, _P2SH_PREFIXES, NETWORKS, network_from_key_value
from .scriptpubkey import payload_from_scriptPubKey, scriptPubKey_from_payload
from .utils import bytes_from_octets

# 1. Hash/WitnessProgram from pubkey/script
# imported from the hashes module

# 2. base58 address from HASH and vice versa


def b58address_from_h160(prefix: Octets, h160: Octets, network: str) -> bytes:
    "Encode a base58 address from the payload."

    prefix = bytes_from_octets(prefix)
    prefixes = NETWORKS[network]["p2pkh"], NETWORKS[network]["p2sh"]
    if prefix not in prefixes:
        raise ValueError(f"Invalid {network} base58 address prefix {prefix!r}")
    payload = prefix + bytes_from_octets(h160, 20)
    return b58encode(payload)


def h160_from_b58address(b58addr: String) -> Tuple[bytes, bytes, str, bool]:
    "Return the payload from a base58 address."

    if isinstance(b58addr, str):
        b58addr = b58addr.strip()

    payload = b58decode(b58addr, 21)
    prefix = payload[0:1]
    if prefix in _P2PKH_PREFIXES:
        network = network_from_key_value("p2pkh", prefix)
        is_script_hash = False
    elif prefix in _P2SH_PREFIXES:
        network = network_from_key_value("p2sh", prefix)
        is_script_hash = True
    else:
        raise ValueError(f"Invalid base58 address prefix {prefix!r}")

    return prefix, payload[1:], network, is_script_hash


# 1.+2. = 3. base58 address from pubkey/script


def p2pkh(
    key: Key, network: Optional[str] = None, compressed: Optional[bool] = None
) -> bytes:
    "Return the p2pkh base58 address corresponding to a public key."
    h160, network = hash160_from_pubkey(key, network, compressed)
    prefix = NETWORKS[network]["p2pkh"]
    return b58address_from_h160(prefix, h160, network)


def p2sh(script: Script, network: str = "mainnet") -> bytes:
    "Return the p2sh base58 address corresponding to a script."
    h160 = hash160_from_script(script)
    prefix = NETWORKS[network]["p2sh"]
    return b58address_from_h160(prefix, h160, network)


# 2b. base58 address from WitnessProgram
# it cannot be inverted because of the hash performed by p2sh


def b58address_from_witness(wp: Octets, network: str = "mainnet") -> bytes:
    "Encode a legacy base58 p2sh-wrapped SegWit address."

    length = len(wp)
    if length == 20:
        redeem_script = scriptPubKey_from_payload("p2wpkh", wp)
    elif length == 32:
        redeem_script = scriptPubKey_from_payload("p2wsh", wp)
    else:
        m = f"Invalid witness program length ({len(wp)})"
        raise ValueError(m)

    return p2sh(redeem_script, network)


# 1.+2b. = 3b. base58 (p2sh-wrapped) SegWit addresses from pubkey/script


def p2wpkh_p2sh(key: Key, network: Optional[str] = None) -> bytes:
    "Return the p2wpkh-p2sh base58 address corresponding to a pubkey."
    compressed = True  # needed to force check on pubkey
    witprog, network = hash160_from_pubkey(key, network, compressed)
    return b58address_from_witness(witprog, network)


def p2wsh_p2sh(wscript: Script, network: str = "mainnet") -> bytes:
    "Return the p2wsh-p2sh base58 address corresponding to a script."
    witprog = hash256_from_script(wscript)
    return b58address_from_witness(witprog, network)


##########################


def has_segwit_prefix(addr: String) -> bool:

    if isinstance(addr, str):
        str_addr = addr.strip()
        str_addr = str_addr.lower()
    else:
        str_addr = addr.decode("ascii")

    for net in NETWORKS:
        if str_addr.startswith(NETWORKS[net]["p2w"] + "1"):
            return True

    return False


def scriptPubKey_from_address(addr: String) -> Tuple[bytes, str]:
    "Return (scriptPubKey, network) from the input bech32/base58 address"

    if has_segwit_prefix(addr):
        # also check witness validity
        wv, wp, network, is_script_hash = witness_from_b32address(addr)
        if wv != 0:
            raise ValueError(f"Unmanaged witness version ({wv})")
        if is_script_hash:
            return scriptPubKey_from_payload("p2wsh", wp), network
        else:
            return scriptPubKey_from_payload("p2wpkh", wp), network
    else:
        _, h160, network, is_p2sh = h160_from_b58address(addr)
        if is_p2sh:
            return scriptPubKey_from_payload("p2sh", h160), network
        else:
            return scriptPubKey_from_payload("p2pkh", h160), network


def address_from_scriptPubKey(s: Script, network: str = "mainnet") -> bytes:
    "Return the bech32/base58 address from the input scriptPubKey."

    script_type, payload, m = payload_from_scriptPubKey(s)
    if script_type == "p2pk":
        raise ValueError("No address for p2pk script")
    if script_type == "p2ms" or isinstance(payload, list) or m != 0:
        raise ValueError("No address for p2ms script")
    if script_type == "nulldata":
        raise ValueError("No address for null data script")

    if script_type == "p2pkh":
        prefix = NETWORKS[network]["p2pkh"]
        return b58address_from_h160(prefix, payload, network)
    if script_type == "p2sh":
        prefix = NETWORKS[network]["p2sh"]
        return b58address_from_h160(prefix, payload, network)

    # 'p2wsh' or 'p2wpkh'
    return b32address_from_witness(0, payload, network)
