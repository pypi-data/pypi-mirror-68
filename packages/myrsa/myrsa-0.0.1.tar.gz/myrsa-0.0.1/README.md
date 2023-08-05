# myrsa

Simple use of RSA for asymmetric encryption and signature

简单使用 rsa 进行非对称加密和签名

Installation
```
pip install myrsa
```

Usage:
```python
import myrsa

pubkey, prikey = myrsa.newkeys()
print((pubkey, prikey))

message = 'Hello@世界'

crypto = myrsa.encrypt(message, pubkey)
print(crypto)

message = myrsa.decrypt(crypto, prikey)
print(message)

signature = myrsa.sign(message, prikey)
print(signature)

verified = myrsa.verify(message, signature, pubkey)
print(verified)
```

