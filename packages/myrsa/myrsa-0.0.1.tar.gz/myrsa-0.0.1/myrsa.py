# Python3
# pip install rsa

import base64
import hashlib

import rsa
from rsa import common, transform, core
from rsa.pkcs1 import _pad_for_signing


VERSION = '0.0.1'


def newkeys(nbits=128):
    if nbits > 4096:
        print('[WARNING] nbits is too big, it will take a long time.')
    if nbits < 128:
        print('[WARNING] nbits is too small.')
    pub_key, priv_key = rsa.newkeys(nbits)
    pubkey = base64.b64encode(pub_key.save_pkcs1('DER')).decode()
    prikey = base64.b64encode(priv_key.save_pkcs1('DER')).decode()
    return pubkey, prikey


def encrypt(message, pubkey, encoding='utf8'):
    assert isinstance(message, str), 'message must be a sting!'
    assert isinstance(pubkey, str), 'pubkey must be a sting!'
    
    pubder = base64.b64decode(pubkey)
    pub_key = rsa.PublicKey.load_pkcs1(pubder, 'DER')
    message = message.encode(encoding)
    
    keylength = common.byte_size(pub_key.n)
    block_length = keylength - 11
    assert block_length > 0, 'nbits of key is to small, please set bigger then 128!'
    
    crypto = b''
    while message:
        m = message[:block_length]
        message = message[block_length:]
        c = rsa.encrypt(m, pub_key)
        crypto += c

    crypto = base64.b64encode(crypto).decode()
    return crypto


def decrypt(crypto, prikey, encoding='utf8'):
    assert isinstance(crypto, str), 'crypto must be a sting!'
    assert isinstance(prikey, str), 'prikey must be a sting!'
    prider = base64.b64decode(prikey)
    priv_key = rsa.PrivateKey.load_pkcs1(prider, 'DER')
    crypto = base64.b64decode(crypto)
    
    keylength = common.byte_size(priv_key.n)
    
    message = b''
    while crypto:
        c = crypto[:keylength]
        crypto = crypto[keylength:]
        m = rsa.decrypt(c, priv_key)
        message += m

    message = message.decode(encoding)
    return message


def sign(message, prikey, encoding='utf8'):
    assert isinstance(message, str), 'message must be a sting!'
    assert isinstance(prikey, str), 'prikey must be a sting!'
    
    message = message.encode(encoding)
    prider = base64.b64decode(prikey)
    priv_key = rsa.PrivateKey.load_pkcs1(prider, 'DER')

    message_hash = hashlib.md5(message).digest()

    keylength = common.byte_size(priv_key.n)
    block_length = keylength - 11
    assert block_length > 0, 'nbits of key is to small, please set bigger then 128!'

    signature = b''
    while message_hash:
        cleartext = message_hash[:block_length]
        message_hash = message_hash[block_length:]

        # ===== copy from rsa.pkcs1:sign_hash =====
        padded = _pad_for_signing(cleartext, keylength)
        payload = transform.bytes2int(padded)
        encrypted = priv_key.blinded_encrypt(payload)
        block = transform.int2bytes(encrypted, keylength)

        signature += block

    signature = base64.b64encode(signature).decode()
    return signature


def verify(message, signature, pubkey, encoding='utf8'):
    assert isinstance(message, str), 'message must be a sting!'
    assert isinstance(signature, str), 'signature must be a sting!'

    message = message.encode(encoding)
    signature_full = base64.b64decode(signature)
    pubder = base64.b64decode(pubkey)
    pub_key = rsa.PublicKey.load_pkcs1(pubder, 'DER')

    message_hash = hashlib.md5(message).digest()
    
    keylength = common.byte_size(pub_key.n)
    
    decrypted_hash = b''
    while signature_full:
        signature = signature_full[:keylength]
        signature_full = signature_full[keylength:]

        # ===== copy from rsa.pkcs1:verify =====
        encrypted = transform.bytes2int(signature)
        decrypted = core.decrypt_int(encrypted, pub_key.e, pub_key.n)
        clearsig = transform.int2bytes(decrypted, keylength)

        if clearsig[0:2] != b'\x00\x01':
            return False
        clearsig = clearsig[2:]
        if b'\x00' not in clearsig:
            return False
        sep_idx = clearsig.index(b'\x00')
        clearsig = clearsig[sep_idx + 1:]
        
        decrypted_hash += clearsig
        
    return decrypted_hash == message_hash


if __name__ == '__main__':
    pubkey, prikey = newkeys()
    print((pubkey, prikey))

    message = 'Hello@世界'

    crypto = encrypt(message, pubkey)
    print(crypto)

    message = decrypt(crypto, prikey)
    print(message)

    signature = sign(message, prikey)
    print(signature)
    
    verified = verify(message, signature, pubkey)
    print(verified)
