import os
from ecc.curves import SECP_256k1
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.x963kdf import X963KDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

#this represents the cryptogram that Bob must decipher
class cryptogram():
    a_public_key = ""
    b_private_key = ""
    mTag = ""
    c = ""
    salt = os.urandom(16)


def generateCryptogram(pt):
    # generating diffie-hellman keys with a key size of 512 and default backend
    parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())

    # generating keys for Alice
    a_private_key = parameters.generate_private_key()
    a_public_key = a_private_key.public_key()

    # generating keys for Bob
    b_private_key = parameters.generate_private_key()
    b_public_key = b_private_key.public_key()

    # creating a shared secret
    a_shared_key = a_private_key.exchange(b_public_key)

    # passing the secret on to the KDF function
    e = cryptogram()
    salt = os.urandom(16)
    e2 = keyDerivationFunction(pt, a_shared_key, hashes.SHA256(), 32, salt,
                               100000, default_backend())

    #saving Alice's public key and Bob's private key to simulate two individuals
    e.a_public_key = a_public_key
    e.b_private_key = b_private_key
    e.mTag = e2.mTag
    e.c = e2.c
    e.salt = salt
    return e


def degenerateCryptogram(cg):
    #assigning Bob's shared key fromt he private key of Bob and public key of Alice, which we saved beforehand
    b_shared_key = cg.b_private_key.exchange(cg.a_public_key)

    # passing the secret on to the KDF2 function for decryption
    e = cryptogram()
    e2 = keyDerivationFunction2(cg.mTag, cg.c, b_shared_key, hashes.SHA256(), 32, cg.salt,
                                100000, default_backend())
    e.c = e2.c
    return e


def keyDerivationFunction(pt, a_shared_key, algorithm, length, salt, iterations, backend):
    #using PBKDF2MAC function to derive and verify an eKey for encryption
    kdf = PBKDF2HMAC(algorithm, length, salt, iterations, backend)
    eKey = kdf.derive(a_shared_key)
    kdf = PBKDF2HMAC(algorithm, length, salt, iterations, backend)
    kdf.verify(a_shared_key, eKey)

    #using X963KDF function to derive and verify a macKey for the MAC function
    kdf2 = X963KDF(algorithm, length, "", backend)
    macKey = kdf2.derive(a_shared_key)
    kdf2 = X963KDF(algorithm, length, "", backend)
    kdf2.verify(a_shared_key, macKey)

    #creating a cryptogram to save the encrypted message and MAC tag
    e = cryptogram()
    iv = salt

    #encrypting
    e.c = symmetricEncrypt(pt, eKey, iv, default_backend())

    #creating tag
    e.mTag = macFunction(macKey, hashes.SHA256(), default_backend())
    return e


def keyDerivationFunction2(mTag, ct, b_shared_key, algorithm, length, salt, iterations, backend):
    #extending the shared key with the PBKDF2 algorithm to get the eKey
    kdf = PBKDF2HMAC(algorithm, length, salt, iterations, backend)
    eKey = kdf.derive(b_shared_key)
    kdf = PBKDF2HMAC(algorithm, length, salt, iterations, backend)
    kdf.verify(b_shared_key, eKey)

    # extending the shared key with the X963KDF algorithm to get the macKey
    kdf2 = X963KDF(algorithm, length, "", backend)
    macKey = kdf2.derive(b_shared_key)
    kdf2 = X963KDF(algorithm, length, "", backend)
    kdf2.verify(b_shared_key, macKey)

    #checking that our macKey is the same as Alice's
    e = cryptogram()
    e.mTag = macFunction(macKey, hashes.SHA256(), default_backend())
    if(e.mTag == mTag):
        e.c = symmetricDecrypt(ct, eKey, salt, default_backend())
    else:
        print "wrong tag, exiting program"
        return
    return e


def symmetricEncrypt(pt, key, iv, backend):
    #symmetric encrypticion using CTR algorithm and eKey
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(pt) + encryptor.finalize()
    return ct


def symmetricDecrypt(ct, key, iv, backend):
    #symmetric decryption using CTR algorithm and eKey we created before
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend)
    decryptor = cipher.decryptor()
    dt = decryptor.update(ct) + decryptor.finalize()
    return dt


def macFunction(key, hash, backend):
    #generating our macTag using our macKey
    h = hmac.HMAC(key, hash, backend)
    h.update(key)
    return h.finalize()

def driver():
    #command line interface for the program
    response = raw_input("Type 'encrypt' to begin processing a file or text or 'exit' to end program: ")
    if response == "encrypt":
        response2 = raw_input("Enter 'f' for the file you want to encrypt or 't' for text you want to encrypt: ")
        if response2 == "f":
            response3 = raw_input("Enter the filepath for the file you want to encrypt to start encryption: ")
            if response3.endswith(".txt"):
                file = open(response3)
                content = file.read()
                cg = generateCryptogram(content)
                print "U = " + str(cg.a_public_key)
                print "tag = " + cg.mTag
                print "c = \n" + cg.c
                response4 = raw_input("Enter 'd' to decrypt this cryptogram or 'e' to exit the program: ")
                if response4 == "d":
                    dg = degenerateCryptogram(cg)
                    print "deciphered text:\n" + dg.c
                if response == "e":
                    print "exiting program"
                    return
            else:
                print "invalid filepath"
                return
        if response2 == "t":
            response3 = raw_input("Enter the text to start encryption: ")
            cg = generateCryptogram(response3)
            print "U = " + str(cg.a_public_key)
            print "tag = " + cg.mTag
            print "c = \n" + cg.c
            response4 = raw_input("Enter 'd' to decrypt this cryptogram or 'e' to exit the program: ")
            if response4 == "d":
                dg = degenerateCryptogram(cg)
                print "deciphered text:\n" + dg.c
            if response == "e":
                print "exiting program"
                return

    elif response == "exit":
        print "exiting program"
        return
    else:
        print "invalid response, exiting program"
        return


if __name__ == '__main__':
    driver()
