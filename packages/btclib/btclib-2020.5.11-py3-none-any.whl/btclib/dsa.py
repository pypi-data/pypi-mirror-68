#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""Elliptic Curve Digital Signature Algorithm (ECDSA).

   Implementation according to SEC 1 v.2:

   http://www.secg.org/sec1-v2.pdf

   specialized with bitcoin canonical 'low-s' encoding.
"""

import secrets
from hashlib import sha256
from typing import List, Optional, Tuple

from . import der
from .alias import DSASig, DSASigTuple, HashF, JacPoint, Key, Point, PrvKey, String
from .curve import Curve
from .curvemult import _double_mult, _mult_jac
from .curves import secp256k1
from .numbertheory import mod_inv
from .rfc6979 import _rfc6979
from .to_prvkey import int_from_prvkey
from .to_pubkey import point_from_key
from .utils import int_from_bits

# _validate_sig, deserialize and serialize are basically just wrappers
# for the equivalent functions in the der module


def _validate_sig(r: int, s: int, ec: Curve = secp256k1) -> None:
    return der._validate_sig(r, s, None, ec)


def deserialize(sig: DSASig, ec: Curve = secp256k1) -> DSASigTuple:
    """Return the verified components of the provided ECDSA signature.

    The ECDSA signature can be represented as (r, s) tuple or
    as strict ASN.1 DER binary representation.
    """

    if isinstance(sig, tuple):
        r, s = sig
        _validate_sig(r, s, ec)
        return r, s
    else:
        return der._deserialize(sig, ec)[0:2]


def serialize(r: int, s: int, ec: Curve = secp256k1) -> bytes:
    "Return the ECDSA signature as strict ASN.1 DER representation."

    return der._serialize(r, s, None, ec)


def gen_keys(prvkey: PrvKey = None, ec: Curve = secp256k1) -> Tuple[int, Point]:
    "Return a private/public (int, Point) key-pair."

    if prvkey is None:
        # q in the range [1, ec.n-1]
        q = 1 + secrets.randbelow(ec.n - 1)
    else:
        q = int_from_prvkey(prvkey, ec)

    QJ = _mult_jac(q, ec.GJ, ec)
    Q = ec._aff_from_jac(QJ)
    # q.to_bytes(ec.nsize, 'big')
    # bytes_from_point(Q, ec, compressed)
    return q, Q


def _challenge(msg: String, ec: Curve, hf: HashF) -> int:

    if isinstance(msg, str):
        msg = msg.encode()

    # Steps numbering follows SEC 1 v.2 section 4.1.3
    h = hf()
    h.update(msg)
    mhd = h.digest()  # 4
    # leftmost ec.nlen bits %= ec.n
    c = int_from_bits(mhd, ec.nlen) % ec.n  # 5
    return c


def _sign(c: int, q: int, k: int, ec: Curve) -> DSASigTuple:
    # Private function for testing purposes: it allows to explore all
    # possible value of the challenge c (for low-cardinality curves).
    # It assume that c is in [0, n-1], while q and k are in [1, n-1]

    # Steps numbering follows SEC 1 v.2 section 4.1.3

    KJ = _mult_jac(k, ec.GJ, ec)  # 1

    # affine x-coordinate of K (field element)
    K_x = (KJ[0] * mod_inv(KJ[2] * KJ[2], ec.p)) % ec.p
    # mod n makes it a scalar
    r = K_x % ec.n  # 2, 3
    if r == 0:  # r≠0 required as it multiplies the public key
        raise ValueError("r = 0, failed to sign")

    s = mod_inv(k, ec.n) * (c + r * q) % ec.n  # 6
    if s == 0:  # s≠0 required as verify will need the inverse of s
        raise ValueError("s = 0, failed to sign")

    # bitcoin canonical 'low-s' encoding for ECDSA signatures
    # it removes signature malleability as cause of transaction malleability
    # see https://github.com/bitcoin/bitcoin/pull/6769
    if s > ec.n / 2:
        s = ec.n - s  # s = - s % ec.n

    return r, s


# RFC6979 is used for deterministic nonce
def sign(
    msg: String,
    prvkey: PrvKey,
    k: Optional[PrvKey] = None,
    ec: Curve = secp256k1,
    hf: HashF = sha256,
) -> DSASigTuple:
    """ECDSA signature with canonical low-s encoding.

    Implemented according to SEC 1 v.2
    The message m is first processed by hf, yielding the value

        mhd = hf(m),

    a sequence of bits of length *hlen*.

    Normally, hf is chosen such that its output length *hlen* is
    roughly equal to *nlen*, the bit-length of the group order *n*,
    since the overall security of the signature scheme will depend on
    the smallest of *hlen* and *nlen*; however, the ECDSA standard
    supports all combinations of *hlen* and *nlen*.

    See https://tools.ietf.org/html/rfc6979#section-3.2
    """

    c = _challenge(msg, ec, hf)  # 4, 5

    # The secret key q: an integer in the range 1..n-1.
    # SEC 1 v.2 section 3.2.1
    q = int_from_prvkey(prvkey, ec)

    if k is None:
        k = _rfc6979(c, q, ec, hf)  # 1
    else:
        k = int_from_prvkey(k, ec)

    # second part delegated to helper function
    return _sign(c, q, k, ec)


def _to_sig(sig: DSASig, ec: Curve) -> DSASigTuple:
    if isinstance(sig, tuple):
        r, s = sig
        _validate_sig(r, s, ec)
    else:
        # it is a DER serialized signature
        # sighash is not needed
        r, s = deserialize(sig, ec)
    return r, s


def _verhlp(c: int, QJ: JacPoint, r: int, s: int, ec: Curve) -> None:
    # Private function for test/dev purposes

    w = mod_inv(s, ec.n)
    u = c * w % ec.n
    v = r * w % ec.n  # 4
    # Let K = u*G + v*Q.
    KJ = _double_mult(v, QJ, u, ec.GJ, ec)  # 5

    # Fail if infinite(K).
    assert KJ[2] != 0, "how did you do that?!?"  # 5

    # affine x-coordinate of K
    K_x = (KJ[0] * mod_inv(KJ[2] * KJ[2], ec.p)) % ec.p
    x = K_x % ec.n  # 6, 7
    # Fail if r ≠ K_x %n.
    assert r == x, "Signature verification failed"  # 8


def _verify(msg: String, P: Key, sig: DSASig, ec: Curve, hf: HashF) -> None:
    # Private function for test/dev purposes
    # It raises Errors, while verify should always return True or False

    r, s = _to_sig(sig, ec)  # 1

    c = _challenge(msg, ec, hf)  # 2, 3

    Q = point_from_key(P, ec)
    QJ = Q[0], Q[1], 1 if Q[1] else 0

    # second part delegated to helper function
    _verhlp(c, QJ, r, s, ec)


def verify(
    msg: String, P: Key, sig: DSASig, ec: Curve = secp256k1, hf: HashF = sha256
) -> bool:
    """ECDSA signature verification (SEC 1 v.2 section 4.1.4)."""

    # try/except wrapper for the Errors raised by _verify
    try:
        _verify(msg, P, sig, ec, hf)
    except Exception:
        return False
    else:
        return True


def recover_pubkeys(
    msg: String, sig: DSASig, ec: Curve = secp256k1, hf: HashF = sha256
) -> List[Point]:
    """ECDSA public key recovery (SEC 1 v.2 section 4.1.6).

    See also:
    https://crypto.stackexchange.com/questions/18105/how-does-recovering-the-public-key-from-an-ecdsa-signature-work/18106#18106
    """

    c = _challenge(msg, ec, hf)  # 1.5

    r, s = _to_sig(sig, ec)

    QJs = _recover_pubkeys(c, r, s, ec)
    return [ec._aff_from_jac(QJ) for QJ in QJs]


# TODO: use _recover_pubkey to avoid code duplication
def _recover_pubkeys(c: int, r: int, s: int, ec: Curve) -> List[JacPoint]:
    # Private function provided for testing purposes only.

    # precomputations
    r1 = mod_inv(r, ec.n)
    r1s = r1 * s % ec.n
    r1e = -r1 * c % ec.n
    keys: List[JacPoint] = list()
    # r = K[0] % ec.n
    # if ec.n < K[0] < ec.p (likely when cofactor ec.h > 1)
    # then both x=r and x=r+ec.n must be tested
    for j in range(ec.h):  # 1
        # affine x-coordinate of K (field element)
        x = (r + j * ec.n) % ec.p  # 1.1
        # two possible y-coordinates, i.e. two possible keys for each cycle
        try:
            # even root first for bitcoin message signing compatibility
            yodd = ec.y_odd(x, False)
            KJ = x, yodd, 1  # 1.2, 1.3, and 1.4
            # 1.5 has been performed in the recover_pubkeys calling function
            Q1J = _double_mult(r1s, KJ, r1e, ec.GJ, ec)  # 1.6.1
            try:
                _verhlp(c, Q1J, r, s, ec)  # 1.6.2
            except Exception:
                pass
            else:
                keys.append(Q1J)  # 1.6.2
            KJ = x, ec.p - yodd, 1  # 1.6.3
            Q2J = _double_mult(r1s, KJ, r1e, ec.GJ, ec)
            try:
                _verhlp(c, Q2J, r, s, ec)  # 1.6.2
            except Exception:
                pass
            else:
                keys.append(Q2J)  # 1.6.2
        except Exception:  # K is not a curve point
            pass
    return keys


def _recover_pubkey(key_id: int, c: int, r: int, s: int, ec: Curve) -> JacPoint:
    # Private function provided for testing purposes only.

    # precomputations
    r1 = mod_inv(r, ec.n)
    r1s = r1 * s % ec.n
    r1e = -r1 * c % ec.n
    # r = K[0] % ec.n
    # if ec.n < K[0] < ec.p (likely when cofactor ec.h > 1)
    # then both x=r and x=r+ec.n must be tested
    j = key_id & 0b110  # allow for key_id in [0, 7]
    x = (r + j * ec.n) % ec.p  # 1.1

    # even root first for Bitcoin Core compatibility
    i = key_id & 0b01
    y = ec.y_odd(x, i)
    KJ = x, y, 1  # 1.2, 1.3, and 1.4
    # 1.5 has been performed in the recover_pubkeys calling function
    QJ = _double_mult(r1s, KJ, r1e, ec.GJ, ec)  # 1.6.1
    _verhlp(c, QJ, r, s, ec)  # 1.6.2
    return QJ


def crack_prvkey(
    m1: String,
    sig1: DSASig,
    m2: String,
    sig2: DSASig,
    ec: Curve = secp256k1,
    hf: HashF = sha256,
) -> Tuple[int, int]:

    r1, s1 = _to_sig(sig1, ec)
    r2, s2 = _to_sig(sig2, ec)
    if r1 != r2:
        raise ValueError("Not the same r in signatures")
    if s1 == s2:
        raise ValueError("Identical signatures")

    c1 = _challenge(m1, ec, hf)
    c2 = _challenge(m2, ec, hf)
    k = (c1 - c2) * mod_inv(s1 - s2, ec.n) % ec.n
    q = (s2 * k - c2) * mod_inv(r1, ec.n) % ec.n
    return q, k
