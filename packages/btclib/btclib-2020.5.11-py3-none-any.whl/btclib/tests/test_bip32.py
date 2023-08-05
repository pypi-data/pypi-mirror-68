#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import json
import unittest
from os import path

from btclib import bip39
from btclib.base58 import b58decode, b58encode
from btclib.base58address import p2pkh, p2wpkh_p2sh
from btclib.bech32address import p2wpkh
from btclib.bip32 import (
    crack_prvkey,
    derive,
    deserialize,
    mxprv_from_bip39_mnemonic,
    rootxprv_from_seed,
    serialize,
    xpub_from_xprv,
)
from btclib.curves import secp256k1 as ec
from btclib.network import NETWORKS


class TestBIP32(unittest.TestCase):
    def test_serialize(self):
        xprv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
        xprv_dict = deserialize(xprv)
        xprv_dict = deserialize(xprv_dict)
        xpr2 = serialize(xprv_dict)
        self.assertEqual(xpr2.decode(), xprv)

        invalid_key = (ec.n).to_bytes(ec.nsize, "big")
        # private key not in [1, n-1]
        xprv_dict["key"] = b"\x00" + invalid_key
        self.assertRaises(ValueError, deserialize, xprv_dict)
        # deserialize(xprv_dict)
        decoded_key = b58decode(xprv, 78)
        xkey = b58encode(decoded_key[:46] + invalid_key, 78)
        self.assertRaises(ValueError, deserialize, xkey)
        # deserialize(xkey)

        xpub = xpub_from_xprv(xprv)
        xpub2 = xpub_from_xprv(deserialize(xprv))
        self.assertEqual(xpub, xpub2)

    def test_utils(self):
        # root key, zero depth
        xprv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
        xdict = deserialize(xprv)

        decoded_key = b58decode(xprv, 78)
        self.assertEqual(xdict["version"], decoded_key[:4])
        self.assertEqual(xdict["depth"], decoded_key[4])
        self.assertEqual(xdict["parent_fingerprint"], decoded_key[5:9])
        self.assertEqual(xdict["index"], decoded_key[9:13])
        self.assertEqual(xdict["chain_code"], decoded_key[13:45])
        self.assertEqual(xdict["key"], decoded_key[45:])

        # Zero depth with non-zero parent_fingerprint b"\x01\x01\x01\x01"
        f2 = b"\x00\x00\x00\x0f"
        invalid_key = b58encode(decoded_key[:5] + f2 + decoded_key[9:], 78)
        self.assertRaises(ValueError, deserialize, invalid_key)
        # deserialize(invalid_key)

        # Zero depth with non-zero index
        i2 = b"\x00\x00\x00\xff"
        invalid_key = b58encode(decoded_key[:9] + i2 + decoded_key[13:], 78)
        self.assertRaises(ValueError, deserialize, invalid_key)
        # deserialize(invalid_key)

        # Non-zero depth (255) with zero parent_fingerprint (00000000)
        d2 = b"\xff"
        invalid_key = b58encode(decoded_key[:4] + d2 + decoded_key[5:], 78)
        self.assertRaises(ValueError, deserialize, invalid_key)
        # deserialize(invalid_key)

        child_key = derive(xprv, 0)

        # Derivation path final depth 256>255
        self.assertRaises(ValueError, derive, child_key, "." + 255 * "/0")
        # derive(child_key, "."+255*"/0")

        # Empty derivation path
        self.assertRaises(ValueError, derive, child_key, "")
        # derive(child_key, "")

        # Invalid derivation path root: ";"
        self.assertRaises(ValueError, derive, child_key, ";/0")
        # derive(child_key, ";/0")

        # Derivation path depth 256>255
        self.assertRaises(ValueError, derive, child_key, "." + 256 * "/0")
        # derive(child_key, "." + 256*"/0")

        # xkey is not a public one
        # self.assertRaises(ValueError, p2pkh, xprv)
        # p2pkh(xprv)

    def test_bip32_vectors(self):
        """BIP32 test vector 3

        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
        """
        fname = "bip32_test_vectors.json"
        filename = path.join(path.dirname(__file__), "test_data", fname)
        with open(filename, "r") as f:
            test_vectors = json.load(f)

        for seed in test_vectors:
            mxprv = rootxprv_from_seed(seed)
            for der_path, xpub, xprv in test_vectors[seed]:
                self.assertEqual(xprv, derive(mxprv, der_path).decode())
                self.assertEqual(xpub, xpub_from_xprv(xprv).decode())

    def test_bip39_vectors(self):
        """BIP32 test vectors from BIP39

        https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
        """
        fname = "bip39_test_vectors.json"
        filename = path.join(path.dirname(__file__), "test_data", fname)
        with open(filename, "r") as f:
            test_vectors = json.load(f)["english"]

        for test_vector in test_vectors:
            seed = test_vector[2]
            rootxprv = rootxprv_from_seed(seed)
            self.assertEqual(rootxprv, test_vector[3].encode("ascii"))

    def test_mainnet(self):
        # bitcoin core derivation style
        rootxprv = "xprv9s21ZrQH143K2ZP8tyNiUtgoezZosUkw9hhir2JFzDhcUWKz8qFYk3cxdgSFoCMzt8E2Ubi1nXw71TLhwgCfzqFHfM5Snv4zboSebePRmLS"

        # m / 0h / 0h / 463h
        addr1 = b"1DyfBWxhVLmrJ7keyiHeMbt7N3UdeGU4G5"
        indexes = [0x80000000, 0x80000000, 0x800001CF]
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, indexes)))
        self.assertEqual(addr, addr1)
        path = "m / 0h / 0h / 463h"
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, path)))
        self.assertEqual(addr, addr1)

        # m / 0h / 0h / 267h
        addr2 = b"11x2mn59Qy43DjisZWQGRResjyQmgthki"
        indexes = [0x80000000, 0x80000000, 0x8000010B]
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, indexes)))
        self.assertEqual(addr, addr2)
        path = "M / 0H / 0h // 267' / "
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, path)))
        self.assertEqual(addr, addr2)

        seed = "bfc4cbaad0ff131aa97fa30a48d09ae7df914bcc083af1e07793cd0a7c61a03f65d622848209ad3366a419f4718a80ec9037df107d8d12c19b83202de00a40ad"
        xprv = rootxprv_from_seed(seed)
        xpub = "xpub661MyMwAqRbcFMYjmw8C6dJV97a4oLss6hb3v9wTQn2X48msQB61RCaLGtNhzgPCWPaJu7SvuB9EBSFCL43kTaFJC3owdaMka85uS154cEh"
        self.assertEqual(xpub_from_xprv(xprv).decode(), xpub)

        ind = "./0/0"
        addr = p2pkh(xpub_from_xprv(derive(xprv, ind)))
        self.assertEqual(addr, b"1FcfDbWwGs1PmyhMVpCAhoTfMnmSuptH6g")

        ind = "./0/1"
        addr = p2pkh(xpub_from_xprv(derive(xprv, ind)))
        self.assertEqual(addr, b"1K5GjYkZnPFvMDTGaQHTrVnd8wjmrtfR5x")

        ind = "./0/2"
        addr = p2pkh(xpub_from_xprv(derive(xprv, ind)))
        self.assertEqual(addr, b"1PQYX2uN7NYFd7Hq22ECMzfDcKhtrHmkfi")

        ind = "./1/0"
        addr = p2pkh(xpub_from_xprv(derive(xprv, ind)))
        self.assertEqual(addr, b"1BvSYpojWoWUeaMLnzbkK55v42DbizCoyq")

        ind = "./1/1"
        addr = p2pkh(xpub_from_xprv(derive(xprv, ind)))
        self.assertEqual(addr, b"1NXB59hF4QzYpFrB7o6usLBjbk2D3ZqxAL")

        ind = "./1/2"
        addr = p2pkh(xpub_from_xprv(derive(xprv, ind)))
        self.assertEqual(addr, b"16NLYkKtvYhW1Jp86tbocku3gxWcvitY1w")

        # version/key mismatch in extended parent key
        temp = b58decode(rootxprv)
        bad_xprv = b58encode(temp[0:45] + b"\x01" + temp[46:], 78)
        self.assertRaises(ValueError, derive, bad_xprv, 1)
        # derive(bad_xprv, 1)

        # version/key mismatch in extended parent key
        xpub = xpub_from_xprv(rootxprv)
        temp = b58decode(xpub)
        bad_xpub = b58encode(temp[0:45] + b"\x00" + temp[46:], 78)
        self.assertRaises(ValueError, derive, bad_xpub, 1)
        # derive(bad_xpub, 1)

        # no private/hardened derivation from pubkey
        self.assertRaises(ValueError, derive, xpub, 0x80000000)
        # derive(xpub, 0x80000000)

    def test_testnet(self):
        # bitcoin core derivation style
        rootxprv = "tprv8ZgxMBicQKsPe3g3HwF9xxTLiyc5tNyEtjhBBAk29YA3MTQUqULrmg7aj9qTKNfieuu2HryQ6tGVHse9x7ANFGs3f4HgypMc5nSSoxwf7TK"

        # m / 0h / 0h / 51h
        addr1 = b"mfXYCCsvWPgeCv8ZYGqcubpNLYy5nYHbbj"
        indexes = [0x80000000, 0x80000000, 0x80000000 + 51]
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, indexes)))
        self.assertEqual(addr, addr1)
        path = "m/0h/0h/51h"
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, path)))
        self.assertEqual(addr, addr1)

        # m / 0h / 1h / 150h
        addr2 = b"mfaUnRFxVvf55uD1P3zWXpprN1EJcKcGrb"
        indexes = [0x80000000, 0x80000000 + 1, 0x80000000 + 150]
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, indexes)))
        self.assertEqual(addr, addr2)
        path = "m/0h/1h/150h"
        addr = p2pkh(xpub_from_xprv(derive(rootxprv, path)))
        self.assertEqual(addr, addr2)

    def test_exceptions(self):
        # valid xprv
        xprv = "xprv9s21ZrQH143K2oxHiQ5f7D7WYgXD9h6HAXDBuMoozDGGiYHWsq7TLBj2yvGuHTLSPCaFmUyN1v3fJRiY2A4YuNSrqQMPVLZKt76goL6LP7L"

        # invalid index
        self.assertRaises(ValueError, derive, xprv, "invalid index")
        # derive(xprv, "invalid index")

        # a 4 bytes int is required, not 3
        self.assertRaises(ValueError, derive, xprv, "800000")
        # derive(xprv, "800000")

        # Invalid derivation path root: ""
        self.assertRaises(ValueError, derive, xprv, "/1")
        # derive(xprv, "/1")

        # invalid checksum
        xprv = "xppp9s21ZrQH143K2oxHiQ5f7D7WYgXD9h6HAXDBuMoozDGGiYHWsq7TLBj2yvGuHTLSPCaFmUyN1v3fJRiY2A4YuNSrqQMPVLZKt76goL6LP7L"
        self.assertRaises(ValueError, derive, xprv, 0x80000000)
        # derive(xprv, 0x80000000)

        # invalid extended key version
        version = b"\x04\x88\xAD\xE5"
        xkey = version + b"\x00" * 74
        xkey = b58encode(xkey, 78)
        self.assertRaises(ValueError, derive, xkey, 0x80000000)
        # derive(xkey, 0x80000000)

        # unknown extended key version
        version = b"\x04\x88\xAD\xE5"
        seed = "5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570"
        self.assertRaises(ValueError, rootxprv_from_seed, seed, version)
        # rootxprv_from_seed(seed, version)

        # extended key is not a private one
        xpub = "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
        self.assertRaises(ValueError, xpub_from_xprv, xpub)
        # xpub_from_xprv(xpub)

        # Absolute derivation path for non-master key
        self.assertRaises(ValueError, derive, xpub, "m/44h/0h/1h/0/10")
        # derive(xpub, "m/0/1")

        # empty derivation path
        self.assertRaises(ValueError, derive, xpub, "")
        # derive(xpub, "")

        # extended key is not a public one
        self.assertRaises(ValueError, p2pkh, xprv)
        # p2pkh(xprv)

    def test_exceptions2(self):
        rootxprv = "xprv9s21ZrQH143K2ZP8tyNiUtgoezZosUkw9hhir2JFzDhcUWKz8qFYk3cxdgSFoCMzt8E2Ubi1nXw71TLhwgCfzqFHfM5Snv4zboSebePRmLS"
        d = deserialize(rootxprv)
        self.assertEqual(serialize(d).decode(), rootxprv)

        # invalid 34-bytes key length
        d["key"] += b"\x00"
        self.assertRaises(ValueError, serialize, d)
        # serialize(d)

        # invalid 33-bytes chain_code length
        d = deserialize(rootxprv)
        d["chain_code"] += b"\x00"
        self.assertRaises(ValueError, serialize, d)
        # serialize(d)

        # invalid 5-bytes parent_fingerprint length
        d = deserialize(rootxprv)
        d["parent_fingerprint"] += b"\x00"
        self.assertRaises(ValueError, serialize, d)
        # serialize(d)

        # invalid 5-bytes index length
        d = deserialize(rootxprv)
        d["index"] += b"\x00"
        self.assertRaises(ValueError, serialize, d)
        # serialize(d)

        # invalid depth (256)
        d = deserialize(rootxprv)
        d["depth"] = 256
        self.assertRaises(ValueError, serialize, d)
        # serialize(d)

        # zero depth with non-zero index b"\x00\x00\x00\x01"
        d = deserialize(rootxprv)
        d["index"] = b"\x00\x00\x00\x01"
        self.assertRaises(ValueError, serialize, d)
        # serialize(d)

        # zero depth with non-zero parent_fingerprint b"\x00\x00\x00\x01"
        d = deserialize(rootxprv)
        d["parent_fingerprint"] = b"\x00\x00\x00\x01"
        self.assertRaises(ValueError, serialize, d)
        # serialize(d)

        # non-zero depth (1) with zero parent_fingerprint b"\x00\x00\x00\x00"
        xprv = deserialize(derive(rootxprv, 1))
        xprv["parent_fingerprint"] = b"\x00\x00\x00\x00"
        self.assertRaises(ValueError, serialize, xprv)
        # serialize(xprv)

        # int too big to convert
        self.assertRaises(OverflowError, derive, rootxprv, 256 ** 4)

        # Index must be 4-bytes, not 5
        self.assertRaises(ValueError, derive, rootxprv, b"\x00" * 5)
        # derive(rootxprv, b"\x00"*5)

    def test_testnet_versions(self):

        # data cross-checked with Electrum and
        # https://jlopp.github.io/xpub-converter/

        # 128 bits
        raw_entr = bytes.fromhex("6" * 32)
        # 12 words
        mnemonic = bip39.mnemonic_from_entropy(raw_entr, "en")
        seed = bip39.seed_from_mnemonic(mnemonic, "")

        # p2pkh BIP44
        # m / 44h / coin_typeh / accounth / change / address_index
        path = "m/44h/1h/0h"
        version = NETWORKS["testnet"]["bip32_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "tpubDChqWo2Xi2wNsxyJBE8ipcTJHLKWcqeeNUKBVTpUCNPZkHzHTm3qKAeHqgCou1t8PAY5ZnJ9QDa6zXSZxmjDnhiBpgZ7f6Yv88wEm5HXVbm"
        self.assertEqual(xpub.decode(), exp)
        # first addresses
        xpub_ext = derive(xpub, "./0/0")  # external
        address = p2pkh(xpub_ext)
        exp_address = b"moutHSzeFWViMNEcvBxKzNCMj2kca8MvE1"
        self.assertEqual(address, exp_address)
        xpub_int = derive(xpub, "./1/0")  # internal
        address = p2pkh(xpub_int)
        exp_address = b"myWcXdNais9ExumnGKnNoJwoihQKfNPG9i"
        self.assertEqual(address, exp_address)

        # legacy segwit (p2wsh-p2sh)
        # m / 49h / coin_typeh / accounth / change / address_index
        path = "m/49h/1h/0h"
        version = NETWORKS["testnet"]["slip32_p2wsh_p2sh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "upub5Dj8j7YrwodV68mt58QmNpSzjqjso2WMXEpLGLSvskKccGuXhCh3dTedkzVLAePA617UyXAg2vdswJXTYjU4qjMJaHU79GJVVJCAiy9ezZ2"
        self.assertEqual(xpub.decode(), exp)
        # first addresses
        xpub_ext = derive(xpub, "./0/0")  # external
        address = p2wpkh_p2sh(xpub_ext)
        exp_address = b"2Mw8tQ6uT6mHhybarVhjgomUhHQJTeV9A2c"
        self.assertEqual(address, exp_address)
        xpub_int = derive(xpub, "./1/0")  # internal
        address = p2wpkh_p2sh(xpub_int)
        exp_address = b"2N872CRJ3E1CzWjfixXr3aeC3hkF5Cz4kWb"
        self.assertEqual(address, exp_address)

        # legacy segwit (p2wsh-p2sh)
        # m / 49h / coin_typeh / accounth / change / address_index
        path = "m/49h/1h/0h"
        version = NETWORKS["testnet"]["slip32_p2wpkh_p2sh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "Upub5QdDrMHJWmBrWhwG1nskCtnoTdn91PBwqWU1BbiUFXA2ETUSTc5KiaWZZhSoj5c4KUBTr7Anv92P4U9Dqxd1zDTyQkaWYfmVP2U3Js1W5cG"
        self.assertEqual(xpub.decode(), exp)

        # native segwit (p2wpkh)
        # m / 84h / coin_typeh / accounth / change / address_index
        path = "m/84h/1h/0h"
        version = NETWORKS["testnet"]["slip32_p2wpkh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "vpub5ZhJmduYY7M5J2qCJgSW7hunX6zJrr5WuNg2kKt321HseZEYxqJc6Zso47aNXQw3Wf3sA8kppbfsxnLheUNXcL3xhzeBHLNp8fTVBN6DnJF"
        self.assertEqual(xpub.decode(), exp)
        # first addresses
        xpub_ext = derive(xpub, "./0/0")  # external
        # explicit network is required to discriminate from testnet
        address = p2wpkh(xpub_ext, "regtest")
        exp_address = b"bcrt1qv8lcnmj09rpdqwgl025h2deygur64z4hqf7me5"
        self.assertEqual(address, exp_address)
        xpub_int = derive(xpub, "./1/0")  # internal
        # explicit network is required to discriminate from testnet
        address = p2wpkh(xpub_int, "regtest")
        exp_address = b"bcrt1qqhxvky4y6qkwpvdzqjkdafmj20vs5trmt6y8w5"
        self.assertEqual(address, exp_address)

        # native segwit (p2wsh)
        # m / 84h / coin_typeh / accounth / change / address_index
        path = "m/84h/1h/0h"
        version = NETWORKS["testnet"]["slip32_p2wsh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "Vpub5kbPtsdz74uSibzaFLuUwnFbEu2a5Cm7DeKhfb9aPn8HGjoTjEgtBgjirpXr5r9wk87r2ikwhp4P5wxTwhXUkpAdYTkagjqp2PjMmGPBESU"
        self.assertEqual(xpub.decode(), exp)

    def test_mainnet_versions(self):

        # data cross-checked with Electrum and
        # https://jlopp.github.io/xpub-converter/

        # 128 bits
        raw_entr = bytes.fromhex("6" * 32)
        # 12 words
        mnemonic = bip39.mnemonic_from_entropy(raw_entr, "en")
        seed = bip39.seed_from_mnemonic(mnemonic, "")

        # p2pkh BIP44
        # m / 44h / coin_typeh / accounth / change / address_index
        path = "m/44h/0h/0h"
        version = NETWORKS["mainnet"]["bip32_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "xpub6C3uWu5Go5q62JzJpbjyCLYRGLYvexFeiepZTsYZ6SRexARkNfjG7GKtQVuGR3KHsyKsAwv7Hz3iNucPp6pfHiLvBczyK1j5CtBtpHB3NKx"
        self.assertEqual(xpub.decode(), exp)
        # first addresses
        xpub_ext = derive(xpub, "./0/0")  # external
        address = p2pkh(xpub_ext)
        exp_address = b"1DDKKVHoFWGfctyEEJvrusqq6ipEaieGCq"
        self.assertEqual(address, exp_address)
        xpub_int = derive(xpub, "./1/0")  # internal
        address = p2pkh(xpub_int)
        exp_address = b"1FhKoffreKHzhtBMVW9NSsg3ZF148JPGoR"
        self.assertEqual(address, exp_address)

        # legacy segwit (p2wsh-p2sh)
        # m / 49h / coin_typeh / accounth / change / address_index
        path = "m/49h/0h/0h"
        version = NETWORKS["mainnet"]["slip32_p2wsh_p2sh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "ypub6YBGdYufCVeoPVmNXfdrWhaBCXsQoLKNetNmD9bPTrKmnKVmiyU8f1uJqwGdmBb8kbAZpHoYfXQTLbWpkXc4skQDAreeCUXdbX9k8vtiHsN"
        self.assertEqual(xpub.decode(), exp)
        # first addresses
        xpub_ext = derive(xpub, "./0/0")  # external
        address = p2wpkh_p2sh(xpub_ext)
        exp_address = b"3FmNAiTCWe5kPMgc4dtSgEdY8VuaCiJEH8"
        self.assertEqual(address, exp_address)
        xpub_int = derive(xpub, "./1/0")  # internal
        address = p2wpkh_p2sh(xpub_int)
        exp_address = b"34FLgkoRYX5Q5fqiZCZDwsK5GpXxmFuLJN"
        self.assertEqual(address, exp_address)

        # legacy segwit (p2wpkh-p2sh)
        # m / 49h / coin_typeh / accounth / change / address_index
        path = "m/49h/0h/0h"
        version = NETWORKS["mainnet"]["slip32_p2wpkh_p2sh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "Ypub6j5Mkne6mTDAp4vkUL6qLmuyvKug1gzxyA2S8QrvqdABQW4gVNrQk8mEeeE7Kcp2z4EYgsofYjnxTm8b3km22EWt1Km3bszdVFRcipc6rXu"
        self.assertEqual(xpub.decode(), exp)

        # native segwit (p2wpkh)
        # m / 84h / coin_typeh / accounth / change / address_index
        path = "m/84h/0h/0h"
        version = NETWORKS["mainnet"]["slip32_p2wpkh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "zpub6qg3Uc1BAQkQvcBUYMmZHSzbsshSon3FvJ8yvH3ZZMjFNvJkwSji8UUwghiF3wvpvSvcNWVP8kfUhc2V2RwGp6pTC3ouj6njj956f26TniN"
        self.assertEqual(xpub.decode(), exp)
        # first addresses
        xpub_ext = derive(xpub, "./0/0")  # external
        address = p2wpkh(xpub_ext)
        exp_address = b"bc1q0hy024867ednvuhy9en4dggflt5w9unw4ztl5a"
        self.assertEqual(address, exp_address)
        xpub_int = derive(xpub, "./1/0")  # internal
        address = p2wpkh(xpub_int)
        exp_address = b"bc1qy4x03jyl88h2zeg7l287xhv2xrwk4c3ztfpjd2"
        self.assertEqual(address, exp_address)

        # native segwit (p2wsh)
        # m / 84h / coin_typeh / accounth / change / address_index
        path = "m/84h/0h/0h"
        version = NETWORKS["mainnet"]["slip32_p2wsh_prv"]
        rootprv = rootxprv_from_seed(seed, version)
        xprv = derive(rootprv, path)
        xpub = xpub_from_xprv(xprv)
        exp = "Zpub72a8bqjcjNJnMBLrV2EY7XLQbfji28irEZneqYK6w8Zf16sfhr7zDbLsVQficP9j9uzbF6VW1y3ypmeFKf6Dxaw82WvK8WFjcsLyEvMNZjF"
        self.assertEqual(xpub.decode(), exp)

    def test_rootxprv_from_mnemonic(self):
        mnemonic = (
            "abandon abandon atom  trust  ankle   walnut  "
            "oil     across  awake bunker divorce abstract"
        )
        passphrase = ""
        rootxprv = mxprv_from_bip39_mnemonic(mnemonic, passphrase)
        exp = "xprv9s21ZrQH143K3ZxBCax3Wu25iWt3yQJjdekBuGrVa5LDAvbLeCT99U59szPSFdnMe5szsWHbFyo8g5nAFowWJnwe8r6DiecBXTVGHG124G1"
        self.assertEqual(rootxprv.decode(), exp)

    def test_crack(self):
        parent_xpub = "xpub6BabMgRo8rKHfpAb8waRM5vj2AneD4kDMsJhm7jpBDHSJvrFAjHJHU5hM43YgsuJVUVHWacAcTsgnyRptfMdMP8b28LYfqGocGdKCFjhQMV"
        child_xprv = "xprv9xkG88dGyiurKbVbPH1kjdYrA8poBBBXa53RKuRGJXyruuoJUDd8e4m6poiz7rV8Z4NoM5AJNcPHN6aj8wRFt5CWvF8VPfQCrDUcLU5tcTm"
        parent_xprv = crack_prvkey(parent_xpub, child_xprv)
        self.assertEqual(xpub_from_xprv(parent_xprv).decode(), parent_xpub)
        # same check with XKeyDict
        parent_xprv = crack_prvkey(deserialize(parent_xpub), deserialize(child_xprv))
        self.assertEqual(xpub_from_xprv(parent_xprv).decode(), parent_xpub)

        # extended parent key is not a public one
        self.assertRaises(ValueError, crack_prvkey, parent_xprv, child_xprv)
        # crack_prvkey(parent_xprv, child_xprv)

        # extended child key is not a private one
        self.assertRaises(ValueError, crack_prvkey, parent_xpub, parent_xpub)
        # crack_prvkey(parent_xpub, parent_xpub)

        # wrong child/parent depth relation
        child_xpub = xpub_from_xprv(child_xprv)
        self.assertRaises(ValueError, crack_prvkey, child_xpub, child_xprv)
        # crack_prvkey(child_xpub, child_xprv)

        # not a child for the provided parent
        child0_xprv = derive(parent_xprv, 0)
        grandchild_xprv = derive(child0_xprv, 0)
        self.assertRaises(ValueError, crack_prvkey, child_xpub, grandchild_xprv)
        # crack_prvkey(child_xpub, grandchild_xprv)

        # hardened derivation
        hardened_child_xprv = derive(parent_xprv, 0x80000000)
        self.assertRaises(ValueError, crack_prvkey, parent_xpub, hardened_child_xprv)
        # crack_prvkey(parent_xpub, hardened_child_xprv)


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()  # pragma: no cover
