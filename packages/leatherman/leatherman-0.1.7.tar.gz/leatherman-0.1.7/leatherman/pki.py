#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey
from cryptography.hazmat.backends.openssl.x509 import _CertificateSigningRequest


class CreateModhashRequiresKeyOrCsrError(Exception):
    def __init__(self, obj):
        msg = f"_create_modhash requires key or csr but got obj={obj}"
        super(CreateModhashRequiresKeyOrCsrError, self).__init__(msg)


ENCODING = dict(DER=serialization.Encoding.DER, PEM=serialization.Encoding.PEM)

OIDS_MAP = dict(
    common_name=NameOID.COMMON_NAME,
    org_name=NameOID.ORGANIZATION_NAME,
    org_unit=NameOID.ORGANIZATIONAL_UNIT_NAME,
    org_country=NameOID.COUNTRY_NAME,
    org_city=NameOID.LOCALITY_NAME,
    org_state=NameOID.STATE_OR_PROVINCE_NAME,
    org_zip=NameOID.POSTAL_CODE,
    org_addr1=NameOID.STREET_ADDRESS,
    org_addr2=NameOID.STREET_ADDRESS,
    org_contact_job_title=NameOID.TITLE,
    org_contact_firstname=NameOID.GIVEN_NAME,
    org_contact_lastname=NameOID.SURNAME,
    org_contact_email=NameOID.EMAIL_ADDRESS,
)


def _create_key(common_name, public_exponent, key_size, **kwargs):
    key = rsa.generate_private_key(
        public_exponent=public_exponent, key_size=key_size, backend=default_backend()
    )
    return key


def _create_oids(common_name, oids):
    attrs = [x509.NameAttribute(NameOID.COMMON_NAME, common_name)]
    for key, value in oids.items():
        attr = OIDS_MAP.get(key, None)
        if attr:
            attrs += [x509.NameAttribute(attr, str(value))]
    return attrs


def _add_sans(subject, sans):
    subject.add_extension(
        x509.SubjectAlternativeName([x509.DNSName(san) for san in sans]), critical=False
    )


def _create_csr(common_name, key, oids=None, sans=None):
    builder = x509.CertificateSigningRequestBuilder()
    oids = _create_oids(common_name, oids if oids else {})
    subject = builder.subject_name(x509.Name(oids))
    if sans:
        _add_sans(subject, sans)
    csr = subject.sign(key, hashes.SHA256(), default_backend())
    return csr


def _create_modhash(obj):
    if isinstance(obj, _RSAPrivateKey):
        modulus_int = obj.private_numbers().public_numbers.n
    elif isinstance(obj, _CertificateSigningRequest):
        modulus_int = obj.public_key().public_numbers().n
    else:
        raise CreateModhashRequiresKeyOrCsrError(obj)
    modulus_hex = hex(modulus_int).rstrip("L").lstrip("0x").upper()
    modulus_bytes = f"Modulus={modulus_hex}\n".encode("utf-8")
    md5 = hashlib.md5()
    md5.update(modulus_bytes)
    return md5.hexdigest()


def get_serial(crt):
    crt = x509.load_pem_x509_certificate(str.encode(crt), default_backend())
    return crt.serial_number


def get_sha1(crt):
    crt = x509.load_pem_x509_certificate(str.encode(crt), default_backend())
    return crt.fingerprint(hashes.SHA1()).hex()


def get_sha2(crt):
    crt = x509.load_pem_x509_certificate(str.encode(crt), default_backend())
    return crt.fingerprint(hashes.SHA256()).hex()


def create_modhash_key_and_csr(
    common_name,
    public_exponent=None,
    key_size=None,
    key=None,
    csr=None,
    oids=None,
    sans=None,
    encoding="PEM",
):
    if csr:
        csr = x509.load_pem_x509_csr(str.encode(csr), default_backend())
    elif key:
        key = serialization.load_pem_private_key(
            str.encode(key), password=None, backend=default_backend()
        )
        csr = _create_csr(common_name, key, oids, sans)
    else:
        key = _create_key(common_name, public_exponent, key_size)
        csr = _create_csr(common_name, key, oids, sans)
    modhash = _create_modhash(csr)
    if isinstance(key, _RSAPrivateKey):
        key = key.private_bytes(
            encoding=ENCODING[encoding],
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")
    if isinstance(csr, _CertificateSigningRequest):
        csr = csr.public_bytes(ENCODING[encoding]).decode("utf-8")
    return (modhash, key, csr)
