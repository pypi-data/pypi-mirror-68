#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import secrets
import unittest
from typing import List

from btclib.alias import INF, INFJ
from btclib.curve import _mult_aff, _mult_jac
from btclib.curvemult import double_mult, mult, multi_mult
from btclib.curves import secp256k1
from btclib.tests.test_curves import low_card_curves

ec23_31 = low_card_curves["ec23_31"]


class TestEllipticCurve(unittest.TestCase):
    def test_mult(self):
        for ec in low_card_curves.values():
            for q in range(ec.n):
                Q = _mult_aff(q, ec.G, ec)
                QJ = _mult_jac(q, ec.GJ, ec)
                Q2 = ec._aff_from_jac(QJ)
                self.assertEqual(Q, Q2)
        # with last curve
        self.assertEqual(INF, _mult_aff(3, INF, ec))
        self.assertEqual(INFJ, _mult_jac(3, INFJ, ec))

    def test_shamir(self):
        ec = ec23_31
        for k1 in range(ec.n):
            for k2 in range(ec.n):
                shamir = double_mult(k1, ec.G, k2, ec.G, ec)
                std = ec.add(mult(k1, ec.G, ec), mult(k2, ec.G, ec))
                self.assertEqual(shamir, std)
                shamir = double_mult(k1, INF, k2, ec.G, ec)
                std = ec.add(mult(k1, INF, ec), mult(k2, ec.G, ec))
                self.assertEqual(shamir, std)
                shamir = double_mult(k1, ec.G, k2, INF, ec)
                std = ec.add(mult(k1, ec.G, ec), mult(k2, INF, ec))
                self.assertEqual(shamir, std)

    def test_boscoster(self):
        ec = secp256k1

        k: List[int] = list()
        ksum = 0
        for i in range(11):
            k.append(secrets.randbits(ec.nlen) % ec.n)
            ksum += k[i]

        P = [ec.G] * len(k)
        boscoster = multi_mult(k, P, ec)
        self.assertEqual(boscoster, mult(ksum, ec.G, ec))

        # mismatch between scalar length and Points length
        P = [ec.G] * (len(k) - 1)
        self.assertRaises(ValueError, multi_mult, k, P, ec)
        # multi_mult(k, P, ec)


def test_double_mult():
    H = (
        0x50929B74C1A04954B78B4B6035E97A5E078A5A0F28EC96D547BFEE9ACE803AC0,
        0x31D3C6863973926E049E637CB1B5F40A36DAC28AF1766968C30C2313F3A38904,
    )
    G = secp256k1.G

    # 0*G + 1*H
    T = double_mult(1, H, 0, G)
    assert T == H

    # 0*G + 2*H
    T = double_mult(2, H, 0, G)
    assert T == mult(2, H)

    # 0*G + 3*H
    T = double_mult(3, H, 0, G)
    assert T == mult(3, H)

    # 1*G + 0*H
    T = double_mult(0, H, 1, G)
    assert T == G

    # 2*G + 0*H
    T = double_mult(0, H, 2, G)
    assert T == mult(2, G)

    # 3*G + 0*H
    T = double_mult(0, H, 3, G)
    assert T == mult(3, G)

    # 0*G + 5*H
    T = double_mult(5, H, 0, G)
    assert T == mult(5, H)

    # 0*G - 5*H
    T = double_mult(-5, H, 0, G)
    assert T == mult(-5, H)

    # 1*G - 5*H
    U = double_mult(-5, H, 1, G)
    assert U == secp256k1.add(G, T)


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()  # pragma: no cover
