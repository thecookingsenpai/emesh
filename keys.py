from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import rsa
import os

# LINK https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/

# NOTE Identity keys
privateKey = None
privateBytes = None
publicKey = None
publicBytes = None
# NOTE Encryption keys
privateRSAKey = None
privateRSAPEM = None
publicRSAKey = None
publicRSAPEM = None

# INFO Common entry point to authentication
def ensure():
    if(
        os.path.exists("private.key")
	):
        print("[ED25519] Loading ed25519 private key...")
        load()
    else:
        print("[ED25519] Creating ed25519 private key...")
        create()

def create():
    global privateKey
    global privateBytes
    # ED25519 Creation
    print("[ED25519] Generating ed25519 identity...")
    privateKey = ed25519.Ed25519PrivateKey.generate() 
    print(privateKey)
    privateBytes = privateKey.private_bytes(
		encoding=serialization.Encoding.Raw,
		format=serialization.PrivateFormat.Raw,
		encryption_algorithm=serialization.NoEncryption()
	)
    print(privateBytes.hex())
    # Public Key Creation
    publicDerivation()
    # RSA Creation
    derive()
    # Writing file
    save()

def load(filepath="./"):
    global privateBytes
    # Reading file
    with open(filepath + "private.key", "rb") as keyFile:
        privateBytes = keyFile.read()
    # Loading key
    try:
        loadBytes(privateBytes)
        print("[ED25519] Loaded ed25519 private key from file [+]")
    except Exception as e:
        print("[ED25519] Could not load ed25519 private key: [X]")
        print(e)
        exit()
        
# INFO privateBytesProvided must be the same kind of data as the privateBytes (aka bytes)
def loadBytes(privateBytesProvided: bytes):
    global privateKey
    print("[ED25519] Loading ed25519 private key from bytes... [*]")
    privateKey = ed25519.Ed25519PrivateKey.from_private_bytes(privateBytesProvided)
    print("[ED25519] Loaded ed25519 private key from bytes [+]")
    #print(privateKey)
    # Public Key Creation
    publicDerivation()
    # RSA Creation
    derive()
    
# INFO Deriving a public key from the private key
def publicDerivation():
    global publicKey
    global publicBytes
    print("[ED25519] Generating ed25519 public key...[*]")
    publicKey = privateKey.public_key()
    #print(publicKey)
    publicBytes = publicKey.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
	)
    print("[ED25519] We are: " + publicBytes.hex())
    print("[ED25519] Generated ed25519 public key [+]")
   #print(publicBytes.hex())
    
# INFO RSA Derivation
def derive():
    global privateRSAKey
    global privateRSAPEM
    global publicRSAKey
    global publicRSAPEM
    # RSA Creation
    print("[RSA] Generating RSA keys from ed25519 identity... [*]")
    privateRSAKey = rsa.generate_key(privateBytes.hex()) # So that the two are linked
    privateRSAPEM = privateRSAKey.exportKey("PEM")
    publicRSAKey = privateRSAKey.public_key()
    publicRSAPEM = publicRSAKey.exportKey("PEM")
    print("[RSA] Generated RSA keys from ed25519 identity [+]")
    #print(privateRSAPEM)
    #print(publicRSAPEM)

# INFO Encrypting a message (returning bytes)
def encrypt(message, publicKey=None):
    global publicRSAKey
    # Supporting self encryption
    if not publicKey:
        publicKey = publicRSAKey
    # Generating the encrypted message
    encrypted = rsa.encrypt(message, publicKey)
    return encrypted

# INFO Decrypting a message (returning bytes)
def decrypt(message, privateKey=None):
    global privateRSAKey
    # Supporting self decryption by default
    if not privateKey:
        privateKey = privateRSAKey
    # Generating the decrypted message
    decrypted = rsa.decrypt(message, privateKey)
    return decrypted

# INFO Sign a message after encoding it (returning bytes)
def sign(message):
    global privateKey
    signature = privateKey.sign(message.encode('utf-8'))
    return signature

# INFO Verify a message (returning boolean)
def verify(message, signature, publicKeyProvided=None):
    global publicKey
    # Supporting self verification
    if not publicKeyProvided:
        publicKeyProvided = publicKey
    # Generating the verified result
    return publicKey.verify(signature, message.encode('utf-8'))

# ANCHOR Utilities
def save():
    global privateBytes
    print("[ED25519] Saving ed25519 key...")
    with open("private.key", "wb") as f:
        f.write(privateBytes)
	