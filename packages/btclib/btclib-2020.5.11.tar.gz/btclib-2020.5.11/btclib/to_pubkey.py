#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from typing import Optional, Tuple

from . import bip32
from .alias import BIP32Key, Key, Point, PrvKey, PubKey
from .curve import Curve
from .curvemult import mult
from .curves import secp256k1
from .network import (
    NETWORKS,
    curve_from_xpubversion,
    network_from_xkeyversion,
    xpubversions_from_network,
)
from .secpoint import bytes_from_point, point_from_octets
from .to_prvkey import prvkeyinfo_from_prvkey
from .utils import bytes_from_octets, hash160


def _point_from_xpub(xpub: BIP32Key, ec: Curve) -> Point:
    "Return an elliptic curve point tuple from a xpub key."

    if not isinstance(xpub, dict):
        xpub = bip32.deserialize(xpub)
    if xpub["key"][0] in (2, 3):
        ec2 = curve_from_xpubversion(xpub["version"])
        if ec != ec2:
            raise ValueError(f"ec/xpub version ({xpub['version'].hex()}) mismatch")
        return point_from_octets(xpub["key"], ec)
    raise ValueError(f"Not a public key: {xpub['key'].hex()}")


def point_from_key(key: Key, ec: Curve = secp256k1) -> Point:
    """Return a point tuple from any possible key representation.

    It supports:

    - BIP32 extended keys (bytes, string, or BIP32KeyDict)
    - SEC Octets (bytes or hex-string, with 02, 03, or 04 prefix)
    - native tuple
    """

    if isinstance(key, tuple):
        return point_from_pubkey(key, ec)
    elif isinstance(key, int):
        q, _, _ = prvkeyinfo_from_prvkey(key)
        return mult(q, ec.G, ec)
    else:
        try:
            q, net, _ = prvkeyinfo_from_prvkey(key)
        except Exception:
            pass
        else:
            if ec != NETWORKS[net]["curve"]:
                raise ValueError("Curve mismatch")
            return mult(q, ec.G, ec)

    return point_from_pubkey(key, ec)


def point_from_pubkey(P: PubKey, ec: Curve = secp256k1) -> Point:
    "Return an elliptic curve point tuple from a public key."

    if isinstance(P, tuple):
        if ec.is_on_curve(P) and P[1] != 0:
            return P
        raise ValueError(f"Not a public key: {P}")
    elif isinstance(P, dict):
        return _point_from_xpub(P, ec)
    else:
        try:
            return _point_from_xpub(P, ec)
        except Exception:
            pass

    return point_from_octets(P, ec)


# not used so far, probably useless
# def point_from_prvkey(prvkey: PrvKey, network: Optional[str] = None)->Point:
#    "Return an elliptic curve point tuple from a private key."
#
#    q, net, compr = prvkeyinfo_from_prvkey(prvkey, network)
#    ec = NETWORKS[net]['curve']
#    return mult(q, ec.G, ec)


PubKeyInfo = Tuple[bytes, str]


def _pubkeyinfo_from_xpub(
    xpub: BIP32Key, network: Optional[str] = None, compressed: Optional[bool] = None
) -> PubKeyInfo:
    """Return the pubkey tuple (SEC-bytes, network) from a BIP32 xpub.

    BIP32Key is always compressed and includes network information:
    here the 'network, compressed' input parameters are passed
    only to allow consistency checks.
    """

    compressed = True if compressed is None else compressed
    if not compressed:
        raise ValueError("Uncompressed SEC / compressed BIP32 mismatch")

    if not isinstance(xpub, dict):
        xpub = bip32.deserialize(xpub)
    if xpub["key"][0] not in (2, 3):
        m = f"Not a public key: {bip32.serialize(xpub).decode()}"
        raise ValueError(m)

    if network is not None:
        allowed_versions = xpubversions_from_network(network)
        if xpub["version"] not in allowed_versions:
            m = f"Not a key for ({network}): "
            m += f"{bip32.serialize(xpub).decode()}"
            raise ValueError(m)
        return xpub["key"], network
    else:
        return xpub["key"], network_from_xkeyversion(xpub["version"])


def pubkeyinfo_from_key(
    key: Key, network: Optional[str] = None, compressed: Optional[bool] = None
) -> PubKeyInfo:
    "Return the pub key tuple (SEC-bytes, network) from a pub/prv key."

    if isinstance(key, tuple):
        return pubkeyinfo_from_pubkey(key, network, compressed)
    elif isinstance(key, int):
        P, network = pubkeyinfo_from_prvkey(key, network, compressed)
    else:
        try:
            P, network = pubkeyinfo_from_prvkey(key, network, compressed)
        # FIXME: catch the NotPrvKeyError only
        except Exception:
            return pubkeyinfo_from_pubkey(key, network, compressed)

    return pubkeyinfo_from_pubkey(P, network, compressed)


def pubkeyinfo_from_pubkey(
    P: PubKey, network: Optional[str] = None, compressed: Optional[bool] = None
) -> PubKeyInfo:
    "Return the pub key tuple (SEC-bytes, network) from a public key."

    compr = True if compressed is None else compressed
    net = "mainnet" if network is None else network
    ec = NETWORKS[net]["curve"]

    if isinstance(P, tuple):
        return bytes_from_point(P, ec, compr), net
    elif isinstance(P, dict):
        return _pubkeyinfo_from_xpub(P, network, compressed)
    else:
        try:
            return _pubkeyinfo_from_xpub(P, network, compressed)
        except Exception:
            pass

    # it must octets
    if compressed is None:
        pubkey = bytes_from_octets(P, (ec.psize + 1, 2 * ec.psize + 1))
        compr = False
        if len(pubkey) == ec.psize + 1:
            compr = True
    else:
        size = ec.psize + 1 if compressed else 2 * ec.psize + 1
        pubkey = bytes_from_octets(P, size)
        compr = compressed

    # verify that it is a valid point
    Q = point_from_octets(pubkey, ec)

    return bytes_from_point(Q, ec, compr), net


def pubkeyinfo_from_prvkey(
    prvkey: PrvKey, network: Optional[str] = None, compressed: Optional[bool] = None
) -> PubKeyInfo:
    "Return the pub key tuple (SEC-bytes, network) from a private key."

    q, net, compr = prvkeyinfo_from_prvkey(prvkey, network, compressed)
    ec = NETWORKS[net]["curve"]
    Pub = mult(q, ec.G, ec)
    pubkey = bytes_from_point(Pub, ec, compr)
    return pubkey, net


def fingerprint(key: Key, network: Optional[str] = None) -> bytes:
    """Return the public key fingerprint from a private/public key.

    The fingerprint is the last four bytes
    of the compressed public key HASH160.
    """

    pubkey, _ = pubkeyinfo_from_key(key, network, compressed=True)
    return hash160(pubkey)[:4]
