#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import csv
import secrets
import unittest
from hashlib import sha256 as hf
from os import path
from typing import List

from btclib import ssa
from btclib.alias import INF, Point
from btclib.curvemult import double_mult, mult
from btclib.curves import CURVES
from btclib.curves import secp256k1 as ec
from btclib.numbertheory import mod_inv
from btclib.pedersen import second_generator
from btclib.tests.test_curves import low_card_curves
from btclib.utils import int_from_bits

secp224k1 = CURVES['secp224k1']


class TestSSA(unittest.TestCase):

    def test_signature(self):
        """Basic tests"""

        q, x_Q = ssa.gen_keys()
        mhd = hf(b'Satoshi Nakamoto').digest()
        sig = ssa.sign(mhd, q, None)
        self.assertEqual(sig, ssa.deserialize(sig))
        ssa._verify(mhd, x_Q, sig, ec, hf)
        self.assertTrue(ssa.verify(mhd, x_Q, sig))

        fmhd = hf(b'Craig Wright').digest()
        self.assertRaises(AssertionError, ssa._verify, fmhd, x_Q, sig, ec, hf)

        fssasig = (sig[0], sig[1], sig[1])
        self.assertRaises(ValueError, ssa._verify, mhd, x_Q, fssasig, ec, hf)

        # y(sG - eP) is not a quadratic residue
        _, fQ = ssa.gen_keys(0x2)
        self.assertRaises(AssertionError, ssa._verify, mhd, fQ, sig, ec, hf)

        _, fQ = ssa.gen_keys(0x4)
        self.assertRaises(AssertionError, ssa._verify, mhd, fQ, sig, ec, hf)

        # not ec.pIsThreeModFour
        self.assertRaises(ValueError, ssa._verify,
                          mhd, x_Q, sig, secp224k1, hf)

        # verify: message of wrong size
        wrongmhd = mhd[:-1]
        self.assertRaises(ValueError, ssa._verify, wrongmhd, x_Q, sig, ec, hf)
        # ssa._verify(wrongmhd, x_Q, sig)

        # sign: message of wrong size
        self.assertRaises(ValueError, ssa.sign, wrongmhd, q, None)
        # ssa.sign(wrongmhd, q, None)

        # invalid (zero) challenge e
        self.assertRaises(ValueError, ssa._recover_pubkeys,
                          0, sig[0], sig[1], ec)
        # ssa._recover_pubkeys(0, sig)

        # not a BIP340 public key
        self.assertRaises(ValueError, ssa._to_bip340_point,
                          ["not", "a BIP340", "public key"])
        # ssa._to_bip340_point(["not", "a BIP340", "public key"])

    def test_bip340_vectors(self):
        """BIP340 (Schnorr) test vectors

        https://github.com/bitcoin/bips/blob/master/bip-0340/test-vectors.csv
        """
        fname = "bip340_test_vectors.csv"
        filename = path.join(path.dirname(__file__), "test_data", fname)
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            # skip column headers while checking that there are 7 columns
            _, _, _, _, _, _, _ = reader.__next__()
            for row in reader:
                (index, seckey, pubkey, mhd, sig, result, comment) = row
                errmsg = f"Test vector #{int(index)}"
                if seckey != '':
                    seckey = bytes.fromhex(seckey)
                    _, pubkey_actual = ssa.gen_keys(seckey)
                    self.assertEqual(pubkey,
                                     hex(pubkey_actual).upper()[2:], errmsg)

                    sig_actual = ssa.serialize(*ssa.sign(mhd, seckey))
                    self.assertEqual(sig, sig_actual.hex().upper(), errmsg)

                result = result == 'TRUE'
                if comment:
                    errmsg += ": " + comment
                result_actual = ssa.verify(mhd, pubkey, sig)
                self.assertEqual(result, result_actual, errmsg)

    def test_low_cardinality(self):
        """test low-cardinality curves for all msg/key pairs."""
        # e_c.n has to be prime to sign
        prime = [11, 13, 17, 19]

        # for dsa it is possible to directy iterate on all
        # possible values for e;
        # for ssa we have to iterate over all possible hash values
        hsize = hf().digest_size
        H = [i.to_bytes(hsize, 'big') for i in range(max(prime) * 4)]
        # only low card curves or it would take forever
        for e_c in low_card_curves.values():
            if e_c.p in prime:  # only few curves or it would take too long
                # BIP340 Schnorr only applies to curve whose prime p = 3 %4
                if not e_c.pIsThreeModFour:
                    self.assertRaises(ValueError, ssa.sign, H[0], 1, None, e_c)
                    continue
                for q in range(1, e_c.n):  # all possible private keys
                    Q = mult(q, e_c.G, e_c)  # public key
                    if not e_c.has_square_y(Q):
                        q = e_c.n - q
                    for h in H:  # all possible hashed messages
                        k = ssa.k(h, q, e_c, hf)
                        K = mult(k, e_c.G, e_c)
                        if not e_c.has_square_y(K):
                            k = e_c.n - k
                        x_K = K[0]
                        try:
                            c = ssa._challenge(x_K, Q[0], h, e_c, hf)
                        except Exception:
                            pass
                        else:
                            s = (k + c * q) % e_c.n
                            sig = ssa.sign(h, q, None, e_c)
                            self.assertEqual((x_K, s), sig)
                            # valid signature must validate
                            self.assertIsNone(ssa._verify(h, Q, sig, e_c, hf))

                            if c != 0:  # FIXME
                                x_Q = ssa._recover_pubkeys(c, x_K, s, e_c)
                                self.assertEqual(Q[0], x_Q)

    def test_batch_validation(self):
        hsize = hf().digest_size
        hlen = hsize * 8

        ms = []
        Qs = []
        sigs = []
        ms.append(secrets.randbits(hlen).to_bytes(hsize, 'big'))
        q = 1 + secrets.randbelow(ec.n - 1)
        # bytes version
        Qs.append(mult(q, ec.G, ec)[0].to_bytes(ec.psize, 'big'))
        sigs.append(ssa.sign(ms[0], q, None, ec, hf))
        # test with only 1 sig
        ssa._batch_verify(ms, Qs, sigs, ec, hf)
        for _ in range(3):
            mhd = secrets.randbits(hlen).to_bytes(hsize, 'big')
            ms.append(mhd)
            q = 1 + secrets.randbelow(ec.n - 1)
            # Point version
            Qs.append(mult(q, ec.G, ec))
            sigs.append(ssa.sign(mhd, q, None, ec, hf))
        ssa._batch_verify(ms, Qs, sigs, ec, hf)
        self.assertTrue(ssa.batch_verify(ms, Qs, sigs, ec, hf))

        # invalid sig
        ms.append(ms[0])
        sigs.append(sigs[1])
        Qs.append(Qs[0])
        self.assertFalse(ssa.batch_verify(ms, Qs, sigs, ec, hf))
        self.assertRaises(AssertionError, ssa._batch_verify,
                          ms, Qs, sigs, ec, hf)
        # ssa._batch_verify(ms, Qs, sigs, ec, hf)
        sigs[-1] = sigs[0]  # valid again

        # Invalid size: 31 bytes instead of 32
        ms[-1] = ms[0][:-1]
        self.assertRaises(ValueError, ssa._batch_verify, ms, Qs, sigs, ec, hf)
        # ssa._batch_verify(ms, Qs, sigs, ec, hf)
        ms[-1] = ms[0]  # valid again

        # mismatch between number of pubkeys (5) and number of messages (6)
        ms.append(ms[0])  # add extra message
        self.assertRaises(ValueError, ssa._batch_verify, ms, Qs, sigs, ec, hf)
        # ssa._batch_verify(ms, Qs, sigs, ec, hf)
        ms.pop()  # valid again

        # mismatch between number of pubkeys (5) and number of signatures (6)
        sigs.append(sigs[0])  # add extra sig
        self.assertRaises(ValueError, ssa._batch_verify, ms, Qs, sigs, ec, hf)
        # ssa._batch_verify(ms, Qs, sigs, ec, hf)
        sigs.pop()  # valid again

        # field prime p is not equal to 3 (mod 4)
        self.assertRaises(ValueError, ssa._batch_verify,
                          ms, Qs, sigs, secp224k1, hf)
        # ssa._batch_verify(ms, Qs, sigs, secp224k1, hf)

    def test_threshold(self):
        """testing 2-of-3 threshold signature (Pedersen secret sharing)"""

        # parameters
        m = 2
        H = second_generator(ec, hf)
        mhd = hf(b'message to sign').digest()

        # FIRST PHASE: key pair generation ###################################

        # 1.1 signer one acting as the dealer
        commits1: List[Point] = list()
        q1, _ = ssa.gen_keys()
        q1_prime, _ = ssa.gen_keys()
        commits1.append(double_mult(q1_prime, H, q1, ec.G))
        # sharing polynomials
        f1 = [q1]
        f1_prime = [q1_prime]
        for i in range(1, m):
            f1.append(ssa.gen_keys()[0])
            f1_prime.append(ssa.gen_keys()[0])
            commits1.append(double_mult(f1_prime[i], H, f1[i], ec.G))
        # shares of the secret
        alpha12 = 0  # share of q1 belonging to signer two
        alpha12_prime = 0
        alpha13 = 0  # share of q1 belonging to signer three
        alpha13_prime = 0
        for i in range(m):
            alpha12 += (f1[i] * pow(2, i)) % ec.n
            alpha12_prime += (f1_prime[i] * pow(2, i)) % ec.n
            alpha13 += (f1[i] * pow(3, i)) % ec.n
            alpha13_prime += (f1_prime[i] * pow(3, i)) % ec.n
        # signer two verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(2, i), commits1[i]))
        t = double_mult(alpha12_prime, H, alpha12, ec.G)
        assert t == RHS, 'signer one is cheating'
        # signer three verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(3, i), commits1[i]))
        t = double_mult(alpha13_prime, H, alpha13, ec.G)
        assert t == RHS, 'signer one is cheating'

        # 1.2 signer two acting as the dealer
        commits2: List[Point] = list()
        q2, _ = ssa.gen_keys()
        q2_prime, _ = ssa.gen_keys()
        commits2.append(double_mult(q2_prime, H, q2, ec.G))
        # sharing polynomials
        f2 = [q2]
        f2_prime = [q2_prime]
        for i in range(1, m):
            f2.append(ssa.gen_keys()[0])
            f2_prime.append(ssa.gen_keys()[0])
            commits2.append(double_mult(f2_prime[i], H, f2[i], ec.G))
        # shares of the secret
        alpha21 = 0  # share of q2 belonging to signer one
        alpha21_prime = 0
        alpha23 = 0  # share of q2 belonging to signer three
        alpha23_prime = 0
        for i in range(m):
            alpha21 += (f2[i] * pow(1, i)) % ec.n
            alpha21_prime += (f2_prime[i] * pow(1, i)) % ec.n
            alpha23 += (f2[i] * pow(3, i)) % ec.n
            alpha23_prime += (f2_prime[i] * pow(3, i)) % ec.n
        # signer one verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(1, i), commits2[i]))
        t = double_mult(alpha21_prime, H, alpha21, ec.G)
        assert t == RHS, 'signer two is cheating'
        # signer three verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(3, i), commits2[i]))
        t = double_mult(alpha23_prime, H, alpha23, ec.G)
        assert t == RHS, 'signer two is cheating'

        # 1.3 signer three acting as the dealer
        commits3: List[Point] = list()
        q3, _ = ssa.gen_keys()
        q3_prime, _ = ssa.gen_keys()
        commits3.append(double_mult(q3_prime, H, q3, ec.G))
        # sharing polynomials
        f3 = [q3]
        f3_prime = [q3_prime]
        for i in range(1, m):
            f3.append(ssa.gen_keys()[0])
            f3_prime.append(ssa.gen_keys()[0])
            commits3.append(double_mult(f3_prime[i], H, f3[i], ec.G))
        # shares of the secret
        alpha31 = 0  # share of q3 belonging to signer one
        alpha31_prime = 0
        alpha32 = 0  # share of q3 belonging to signer two
        alpha32_prime = 0
        for i in range(m):
            alpha31 += (f3[i] * pow(1, i)) % ec.n
            alpha31_prime += (f3_prime[i] * pow(1, i)) % ec.n
            alpha32 += (f3[i] * pow(2, i)) % ec.n
            alpha32_prime += (f3_prime[i] * pow(2, i)) % ec.n
        # signer one verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(1, i), commits3[i]))
        t = double_mult(alpha31_prime, H, alpha31, ec.G)
        assert t == RHS, 'signer three is cheating'
        # signer two verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(2, i), commits3[i]))
        t = double_mult(alpha32_prime, H, alpha32, ec.G)
        assert t == RHS, 'signer three is cheating'
        # shares of the secret key q = q1 + q2 + q3
        alpha1 = (alpha21 + alpha31) % ec.n
        alpha2 = (alpha12 + alpha32) % ec.n
        alpha3 = (alpha13 + alpha23) % ec.n
        for i in range(m):
            alpha1 += (f1[i] * pow(1, i)) % ec.n
            alpha2 += (f2[i] * pow(2, i)) % ec.n
            alpha3 += (f3[i] * pow(3, i)) % ec.n

        # 1.4 it's time to recover the public key
        # each participant i = 1, 2, 3 shares Qi as follows
        # Q = Q1 + Q2 + Q3 = (q1 + q2 + q3) G
        A1: List[Point] = list()
        A2: List[Point] = list()
        A3: List[Point] = list()
        for i in range(m):
            A1.append(mult(f1[i]))
            A2.append(mult(f2[i]))
            A3.append(mult(f3[i]))
        # signer one checks others' values
        RHS2 = INF
        RHS3 = INF
        for i in range(m):
            RHS2 = ec.add(RHS2, mult(pow(1, i), A2[i]))
            RHS3 = ec.add(RHS3, mult(pow(1, i), A3[i]))
        assert mult(alpha21) == RHS2, 'signer two is cheating'
        assert mult(alpha31) == RHS3, 'signer three is cheating'
        # signer two checks others' values
        RHS1 = INF
        RHS3 = INF
        for i in range(m):
            RHS1 = ec.add(RHS1, mult(pow(2, i), A1[i]))
            RHS3 = ec.add(RHS3, mult(pow(2, i), A3[i]))
        assert mult(alpha12) == RHS1, 'signer one is cheating'
        assert mult(alpha32) == RHS3, 'signer three is cheating'
        # signer three checks others' values
        RHS1 = INF
        RHS2 = INF
        for i in range(m):
            RHS1 = ec.add(RHS1, mult(pow(3, i), A1[i]))
            RHS2 = ec.add(RHS2, mult(pow(3, i), A2[i]))
        assert mult(alpha13) == RHS1, 'signer one is cheating'
        assert mult(alpha23) == RHS2, 'signer two is cheating'
        # commitment at the global sharing polynomial
        A: List[Point] = list()
        for i in range(m):
            A.append(ec.add(A1[i], ec.add(A2[i], A3[i])))

        # aggregated public key
        Q = A[0]
        if not ec.has_square_y(Q):
            # print('Q has been negated')
            A[1] = ec.negate(A[1])  # pragma: no cover
            alpha1 = ec.n - alpha1  # pragma: no cover
            alpha2 = ec.n - alpha2  # pragma: no cover
            alpha3 = ec.n - alpha3  # pragma: no cover
            Q = ec.negate(Q)  # pragma: no cover

        # SECOND PHASE: generation of the nonces' pair  ######################
        # Assume signer one and three want to sign

        # 2.1 signer one acting as the dealer
        commits1: List[Point] = list()
        k1 = ssa.k(mhd, q1, ec, hf)
        k1_prime = ssa.k(mhd, q1_prime, ec, hf)
        commits1.append(double_mult(k1_prime, H, k1, ec.G))
        # sharing polynomials
        f1 = [k1]
        f1_prime = [k1_prime]
        for i in range(1, m):
            f1.append(ssa.gen_keys()[0])
            f1_prime.append(ssa.gen_keys()[0])
            commits1.append(double_mult(f1_prime[i], H, f1[i], ec.G))
        # shares of the secret
        beta13 = 0  # share of k1 belonging to signer three
        beta13_prime = 0
        for i in range(m):
            beta13 += (f1[i] * pow(3, i)) % ec.n
            beta13_prime += (f1_prime[i] * pow(3, i)) % ec.n
        # signer three verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(3, i), commits1[i]))
        t = double_mult(beta13_prime, H, beta13, ec.G)
        assert t == RHS, 'signer one is cheating'

        # 2.2 signer three acting as the dealer
        commits3: List[Point] = list()
        k3 = ssa.k(mhd, q3, ec, hf)
        k3_prime = ssa.k(mhd, q3_prime, ec, hf)
        commits3.append(double_mult(k3_prime, H, k3, ec.G))
        # sharing polynomials
        f3 = [k3]
        f3_prime = [k3_prime]
        for i in range(1, m):
            f3.append(ssa.gen_keys()[0])
            f3_prime.append(ssa.gen_keys()[0])
            commits3.append(double_mult(f3_prime[i], H, f3[i], ec.G))
        # shares of the secret
        beta31 = 0  # share of k3 belonging to signer one
        beta31_prime = 0
        for i in range(m):
            beta31 += (f3[i] * pow(1, i)) % ec.n
            beta31_prime += (f3_prime[i] * pow(1, i)) % ec.n
        # signer one verifies consistency of his share
        RHS = INF
        for i in range(m):
            RHS = ec.add(RHS, mult(pow(1, i), commits3[i]))
        t = double_mult(beta31_prime, H, beta31, ec.G)
        assert t == RHS, 'signer three is cheating'

        # 2.3 shares of the secret nonce
        beta1 = beta31 % ec.n
        beta3 = beta13 % ec.n
        for i in range(m):
            beta1 += (f1[i] * pow(1, i)) % ec.n
            beta3 += (f3[i] * pow(3, i)) % ec.n

        # 2.4 it's time to recover the public nonce
        # each participant i = 1, 3 shares Qi as follows
        B1: List[Point] = list()
        B3: List[Point] = list()
        for i in range(m):
            B1.append(mult(f1[i]))
            B3.append(mult(f3[i]))

        # signer one checks values from signer three
        RHS3 = INF
        for i in range(m):
            RHS3 = ec.add(RHS3, mult(pow(1, i), B3[i]))
        assert mult(beta31) == RHS3, 'signer three is cheating'

        # signer three checks values from signer one
        RHS1 = INF
        for i in range(m):
            RHS1 = ec.add(RHS1, mult(pow(3, i), B1[i]))
        assert mult(beta13) == RHS1, 'signer one is cheating'

        # commitment at the global sharing polynomial
        B: List[Point] = list()
        for i in range(m):
            B.append(ec.add(B1[i], B3[i]))

        # aggregated public nonce
        K = B[0]
        if not ec.has_square_y(K):
            # print('K has been negated')
            B[1] = ec.negate(B[1])  # pragma: no cover
            beta1 = ec.n - beta1  # pragma: no cover
            beta3 = ec.n - beta3  # pragma: no cover
            K = ec.negate(K)  # pragma: no cover

        # PHASE THREE: signature generation ###

        # partial signatures
        e = ssa._challenge(K[0], Q[0], mhd, ec, hf)
        gamma1 = (beta1 + e * alpha1) % ec.n
        gamma3 = (beta3 + e * alpha3) % ec.n

        # each participant verifies the other partial signatures

        # signer one
        RHS3 = ec.add(K, mult(e, Q))
        for i in range(1, m):
            temp = double_mult(pow(3, i), B[i], e * pow(3, i), A[i])
            RHS3 = ec.add(RHS3, temp)
        assert mult(gamma3) == RHS3, 'signer three is cheating'

        # signer three
        RHS1 = ec.add(K, mult(e, Q))
        for i in range(1, m):
            temp = double_mult(pow(1, i), B[i], e * pow(1, i), A[i])
            RHS1 = ec.add(RHS1, temp)
        assert mult(gamma1) == RHS1, 'signer one is cheating'

        # PHASE FOUR: aggregating the signature ###
        omega1 = 3 * mod_inv(3 - 1, ec.n) % ec.n
        omega3 = 1 * mod_inv(1 - 3, ec.n) % ec.n
        sigma = (gamma1 * omega1 + gamma3 * omega3) % ec.n

        sig = K[0], sigma

        self.assertTrue(ssa.verify(mhd, Q, sig))

        # ADDITIONAL PHASE: reconstruction of the private key ###
        secret = (omega1 * alpha1 + omega3 * alpha3) % ec.n
        self.assertIn((q1 + q2 + q3) % ec.n, (secret, ec.n - secret))

    def test_musig(self):
        """testing 3-of-3 MuSig

            https://github.com/ElementsProject/secp256k1-zkp/blob/secp256k1-zkp/src/modules/musig/musig.md
            https://blockstream.com/2019/02/18/musig-a-new-multisignature-standard/
            https://eprint.iacr.org/2018/068
            https://blockstream.com/2018/01/23/musig-key-aggregation-schnorr-signatures.html
            https://medium.com/@snigirev.stepan/how-schnorr-signatures-may-improve-bitcoin-91655bcb4744
        """
        mhd = hf(b'message to sign').digest()

        # the signers private and public keys,
        # including both the curve Point and the BIP340-Schnorr public key
        q1, x_Q1 = ssa.gen_keys()
        x_Q1 = x_Q1.to_bytes(ec.psize, 'big')

        q2, x_Q2 = ssa.gen_keys()
        x_Q2 = x_Q2.to_bytes(ec.psize, 'big')

        q3, x_Q3 = ssa.gen_keys()
        x_Q3 = x_Q3.to_bytes(ec.psize, 'big')

        # (non interactive) key setup
        # this is MuSig core: the rest is just Schnorr signature additivity
        # 1. lexicographic sorting of public keys
        keys: List[bytes] = list()
        keys.append(x_Q1)
        keys.append(x_Q2)
        keys.append(x_Q3)
        keys.sort()
        # 2. coefficients
        prefix = b''.join(keys)
        a1 = int_from_bits(hf(prefix + x_Q1).digest(), ec.nlen) % ec.n
        a2 = int_from_bits(hf(prefix + x_Q2).digest(), ec.nlen) % ec.n
        a3 = int_from_bits(hf(prefix + x_Q3).digest(), ec.nlen) % ec.n
        # 3. aggregated public key
        Q1 = mult(q1)
        Q2 = mult(q2)
        Q3 = mult(q3)
        Q = ec.add(double_mult(a1, Q1, a2, Q2), mult(a3, Q3))
        if not ec.has_square_y(Q):
            # print("Q has been negated")
            a1 = ec.n - a1  # pragma: no cover
            a2 = ec.n - a2  # pragma: no cover
            a3 = ec.n - a3  # pragma: no cover

        # ready to sign: nonces and nonce commitments
        k1, _ = ssa.gen_keys()
        K1 = mult(k1)

        k2, _ = ssa.gen_keys()
        K2 = mult(k2)

        k3, _ = ssa.gen_keys()
        K3 = mult(k3)

        # exchange {K_i} (interactive)

        # computes s_i (non interactive)
        # WARNING: signers must exchange the nonces commitments {K_i}
        # before sharing {s_i}

        # same for all signers
        K = ec.add(ec.add(K1, K2), K3)
        if not ec.has_square_y(K):
            k1 = ec.n - k1  # pragma: no cover
            k2 = ec.n - k2  # pragma: no cover
            k3 = ec.n - k3  # pragma: no cover
        r = K[0]
        e = ssa._challenge(r, Q[0], mhd, ec, hf)
        s1 = (k1 + e * a1 * q1) % ec.n
        s2 = (k2 + e * a2 * q2) % ec.n
        s3 = (k3 + e * a3 * q3) % ec.n

        # exchange s_i (interactive)

        # finalize signature (non interactive)
        s = (s1 + s2 + s3) % ec.n
        sig = r, s
        # check signature is valid
        ssa._verify(mhd, Q, sig, ec, hf)
        self.assertTrue(ssa.verify(mhd, Q, sig))

    def test_crack_prvkey(self):
        q = 0x6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725DEADBEEF
        x_Q = mult(q)[0]
        k = 1010101010101010101

        msg1 = "Paolo is afraid of ephemeral random numbers"
        msg1 = hf(msg1.encode()).digest()
        sig1 = ssa.sign(msg1, q, k)
        # print(f'\nmsg1: {msg1.hex().upper()}')
        # print(f'  r1: {hex(sig1[0]).upper()}')
        # print(f'  s1: {hex(sig1[1]).upper()}')

        msg2 = "and Paolo is right to be afraid"
        msg2 = hf(msg2.encode()).digest()
        sig2 = ssa.sign(msg2, q, k)
        # print(f'\nmsg2: {msg2.hex().upper()}')
        # print(f'  r2: {hex(sig2[0]).upper()}')
        # print(f'  s2: {hex(sig2[1]).upper()}')

        qc, kc = ssa.crack_prvkey(msg1, sig1, msg2, sig2, x_Q)
        self.assertIn(q, (qc, ec.n - qc))
        self.assertIn(k, (kc, ec.n - kc))

        self.assertRaises(ValueError, ssa.crack_prvkey, msg1,
                          sig1, msg2, (16, sig1[1]), x_Q)
        self.assertRaises(ValueError, ssa.crack_prvkey,
                          msg1, sig1, msg1, sig1, x_Q)


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()  # pragma: no cover
