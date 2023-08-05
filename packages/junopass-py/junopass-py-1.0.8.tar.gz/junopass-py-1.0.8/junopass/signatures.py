import nacl.encoding
import nacl.signing


def _generate_device_keys():
    """
    Generate device public and private key pairs
    """
    signing_key = nacl.signing.SigningKey.generate()
    private_key = signing_key.encode(encoder=nacl.encoding.HexEncoder)

    verify_key = signing_key.verify_key
    public_key = verify_key.encode(encoder=nacl.encoding.HexEncoder)
    return private_key.decode("utf-8"), public_key.decode("utf-8")


def _sign_message(private_key_hex, message):
    """
    Sign message with your own key i.e device private key
    """
    signing_key = nacl.signing.SigningKey(
        private_key_hex, encoder=nacl.encoding.HexEncoder)
    signed = signing_key.sign(message.encode("utf-8"))
    return signed.hex()


def _verify_junopass_message(public_key, signed_message):
    """
    Verify the authenticity of JunoPass message using its public key.
    Return a boolean as per its status
    """
    verify_key = nacl.signing.VerifyKey(
        public_key, encoder=nacl.encoding.HexEncoder)
    sign_message_byte = bytes.fromhex(signed_message)
    return str(verify_key.verify(sign_message_byte))
