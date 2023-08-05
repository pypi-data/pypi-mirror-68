# JunoPass Python Support

Implementation of [JunoPass Authentication](https://developers.junopass.com/junopass-api/authenticating-users) API in Python.

## Installation

    pip install junopass-py --upgrade

## Get access token and project id

    Create an account for access token and project id - https://console.junopass.com

## How to setup device

**Note the private_key must never be shared.**

    from junopass import JunoPass

    jp = JunoPass(<Access-Token>, <JunoPass-Public-Key>, <Project-ID>)
    private_key, public_key = jp.setup_device()

## Authenticating user - step 1

Submit authentication details to JunoPass. Verify signed challenge hash for authenticity.

    method = "EMAIL"
    identifier = "testuser@example.com"

    valid_challenge, device_id, login_request = jp.authenticate(method, identifier, pubkey)

## Verify account using challenge and OTP token - step 2

Verify OTP message. Send back the user OTP plus a valid challenge obtained in step 1 i.e authenticate function. This function also checks the returned response for authenticity.

    resp = jp.verify(valid_challenge, device_id, prvtkey, otp=120104)
    print(resp)

## Run Test

    python -m unittest
