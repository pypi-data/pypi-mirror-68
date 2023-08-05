import unittest

from junopass import JunoPass


class TestEncryption(unittest.TestCase):

    def setUp(self):
        access_token = "8c7a60ada2a65933f0a431921b45368a45fe424d"
        junopass_public_key = "ae7b59d370ec4d04011baf2738ef068cb1dde6d22e55d16e6ccc0f6c69307cc4"
        project_id = "20cbc960-f786-45fa-a3ad-a9659b097a41"
        self.jp = JunoPass(access_token, junopass_public_key, project_id)

    def test_device_setup(self):
        prvtkey, pubkey = self.jp.setup_device()
        self.assertIsNotNone(prvtkey)
        self.assertIsNotNone(pubkey)
        self.assertNotEqual(prvtkey, pubkey)

    def test_register(self):
        prvtkey, pubkey = self.jp.setup_device()

        method = "EMAIL"
        identifier = "felix.cheruiyot@kenyaapps.net"
        valid_challenge, device_id, _ = self.jp.authenticate(
            method, identifier, pubkey)
        self.assertIsNotNone(valid_challenge)
        self.assertIsNotNone(device_id)

    def test_verification(self):
        prvtkey, pubkey = self.jp.setup_device()

        # Step 1
        method = "EMAIL"
        identifier = "felix.cheruiyot@kenyaapps.net"
        valid_challenge, device_id, _ = self.jp.authenticate(
            method, identifier, pubkey)

        # Step 2
        resp = self.jp.verify(valid_challenge, device_id, prvtkey)

        self.assertIsNotNone(valid_challenge)
        self.assertIsNotNone(device_id)
