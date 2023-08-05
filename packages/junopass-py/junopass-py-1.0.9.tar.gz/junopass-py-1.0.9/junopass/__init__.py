import time

from junopass import signatures
from junopass import client


class JunoPass(object):
    def __init__(self, access_token, junopass_public_key, project_id):
        self.access_token = access_token
        self.junopass_public_key = junopass_public_key
        self.project_id = project_id

    def setup_device(self):
        """
        Generates device signing key
        Use this only on new devices e.g during setup/registration.
        Consider keeping the keys in a safe place for future use.
        Note the private_key must never be shared.

        Returns a tupple of key pair (private_key, public_key).

        Example:
            from junopass import JunoPass
            jp = JunoPass(<Access-Token>, <JunoPass-Public-Key>, <Project-ID>)
            private_key, public_key = jp.setup_device()
        """
        return signatures._generate_device_keys()

    def authenticate(self, method, identifier, public_key):
        """
        Submit authentication details to JunoPass.
        Verify signed challenge hash for authenticity.

        Parameters:
            method string - Options EMAIL, PHONE_NUMBER, BIOMETRIC
            public_key string - Device public key
            identifier string -Identifier i.e User email address or phone number

        Returns a valid challenge hex string and device_id for use in the verification stage.

        Example:
            prvtkey, pubkey = jp.setup_device()

            method = "EMAIL"
            identifier = "felix.cheruiyot@kenyaapps.net"
            valid_challenge, device_id, login_request = jp.authenticate(method, identifier, pubkey)
        """
        if not self.project_id:
            raise Exception("project_id is required")

        payload = {
            "method": method,
            "identifier": identifier,
            "public_key": public_key,
            "project_id": self.project_id
        }
        resp = client._authenticate_request(self.access_token, payload)
        if (resp.status_code != 200 and resp.status_code != 201):
            raise Exception(f"Request error: {resp.text}")

        resp_json = resp.json()
        device_id = resp_json.get("device_id")
        received_challenge = resp_json.get("challenge")
        login_request = resp_json.get("login_request")

        # _verify_junopass_message will automatically throws an exception if not valid
        valid_challenge = signatures._verify_junopass_message(
            self.junopass_public_key, received_challenge)
        return valid_challenge, device_id, login_request

    def verify(self, challenge, device_id, private_key_hex, otp=None):
        """
        Verify OTP message.
        Send back the user OTP plus a valid challenge obtained in step 1 i.e authenticate function.

        Parameters:
            challenge string - From step 1
            device_id string - From step 1
            private_key_hex string - Device private id
            otp integer - User received OTP token

        Example:
            prvtkey, pubkey = self.jp.setup_device()

            # Step 1
            method = "EMAIL"
            identifier = "felix.cheruiyot@kenyaapps.net"
            valid_challenge, device_id = jp.authenticate(
                method, identifier, pubkey)

            # Step 2
            resp = jp.verify(valid_challenge, device_id, prvtkey, otp=120104)
            print(resp)
        """
        if not self.project_id:
            raise Exception("project_id is required")

        timestamp = time.time()
        message = f"{challenge}*{timestamp}*{otp}"
        if not otp:
            message = f"{challenge}*{timestamp}"
        signed_hash = signatures._sign_message(private_key_hex, message)

        payload = {
            "device_id": device_id,
            "signed_hash": signed_hash,
            "project_id": self.project_id
        }

        resp = client._verify_request(self.access_token, payload)
        if (resp.status_code != 200):
            raise Exception(f"Request error: {resp.text}")

        resp = resp.json()
        if not resp.get("access_token_hash"):
            raise Exception("Results error: access_token_hash not found")

        if not resp.get("access_token"):
            raise Exception("Results error: access_token not found")

        # Validate results for authenticity
        # _verify_junopass_message will automatically throws an exception if not valid
        access_token_hash = resp.get("access_token_hash")
        signatures._verify_junopass_message(
            self.junopass_public_key, access_token_hash)

        return resp
