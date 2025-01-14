from datetime import datetime

import pytest

import wacryptolib


def _common_signature_checks(keypair, message, signature, signature_algo):

    assert isinstance(signature["digest"], bytes)
    assert isinstance(signature["timestamp_utc"], int)
    utcnow = datetime.utcnow().timestamp()
    assert utcnow - 10 <= signature["timestamp_utc"] <= utcnow

    wacryptolib.signature.verify_message_signature(
        key=keypair["public_key"],
        message=message,
        signature=signature,
        signature_algo=signature_algo,
    )

    with pytest.raises(ValueError, match="signature"):
        wacryptolib.signature.verify_message_signature(
            key=keypair["public_key"],
            message=message + b"X",
            signature=signature,
            signature_algo=signature_algo,
        )

    signature_corrupted = signature.copy()
    signature_corrupted["digest"] += b"x"
    with pytest.raises(ValueError, match="signature"):
        wacryptolib.signature.verify_message_signature(
            key=keypair["public_key"],
            message=message,
            signature=signature_corrupted,
            signature_algo=signature_algo,
        )

    signature_corrupted = signature.copy()
    signature_corrupted["timestamp_utc"] += 1
    with pytest.raises(ValueError, match="signature"):
        wacryptolib.signature.verify_message_signature(
            key=keypair["public_key"],
            message=message,
            signature=signature_corrupted,
            signature_algo=signature_algo,
        )


def test_sign_and_verify_with_rsa_key():
    message = b"Hello"

    keypair = wacryptolib.key_generation.generate_asymmetric_keypair(
        key_type="RSA", serialize=False, key_length_bits=2048
    )
    signature = wacryptolib.signature.sign_message(
        key=keypair["private_key"], message=message, signature_algo="PSS"
    )
    _common_signature_checks(
        keypair=keypair, message=message, signature=signature, signature_algo="PSS"
    )


def test_sign_and_verify_with_dsa_key():
    message = "Mon hât èst joli".encode("utf-8")

    keypair = wacryptolib.key_generation.generate_asymmetric_keypair(
        key_type="DSA", serialize=False, key_length_bits=2048
    )
    signature = wacryptolib.signature.sign_message(
        key=keypair["private_key"], message=message, signature_algo="DSS"
    )
    _common_signature_checks(
        keypair=keypair, message=message, signature=signature, signature_algo="DSS"
    )


def test_sign_and_verify_with_ecc_key():
    message = "Msd sd 867_ss".encode("utf-8")

    keypair = wacryptolib.key_generation.generate_asymmetric_keypair(
        key_type="ECC", serialize=False, curve="p256"
    )
    signature = wacryptolib.signature.sign_message(
        key=keypair["private_key"], message=message, signature_algo="DSS"
    )
    _common_signature_checks(
        keypair=keypair, message=message, signature=signature, signature_algo="DSS"
    )


def test_generic_signature_errors():

    message = b"Hello"

    keypair = wacryptolib.key_generation.generate_asymmetric_keypair(
        key_type="RSA", serialize=False, key_length_bits=2048
    )

    with pytest.raises(ValueError, match="Unknown signature algorithm"):
        wacryptolib.signature.sign_message(
            key=keypair["private_key"], message=message, signature_algo="EIXH"
        )

    with pytest.raises(ValueError, match="Incompatible key type"):
        wacryptolib.signature.sign_message(
            key=keypair["private_key"],
            message=message,
            signature_algo="DSS",  # RSA key not accepted here
        )

    with pytest.raises(ValueError, match="Unknown signature algorithm"):
        wacryptolib.signature.verify_message_signature(
            key=keypair["public_key"],
            message=message,
            signature={},
            signature_algo="XPZH",
        )
