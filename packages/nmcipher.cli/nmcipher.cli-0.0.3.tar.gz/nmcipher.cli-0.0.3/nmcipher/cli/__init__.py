from .parser import Parser

from nmcipher.caesar import Caesar
from nmcipher.transposition import Columnar

def caesar():
    def encrypt_func(key, message, symbols):
        cipher = Caesar(key, symbols)
        print(message)
        print(cipher.encrypt(message))

    def decrypt_func(key, message, symbols):
        cipher = Caesar(key, symbols)
        print(message)
        print(cipher.decrypt(message))

    def hack_func(method, message, symbols):
        if method != "brute":
            raise NotImplementedError("Caesar class only supports brute-force method")
        for key in range(len(symbols)):
            cipher = Caesar(key, symbols)
            print(f"With key = {key}:")
            print(f"\tOutput: {cipher.decrypt(message)}")

    Parser(encrypt_func, decrypt_func, hack_func)()


def transposition():
    def encrypt_func(key, message):
        cipher = Columnar(key)
        print(message)
        print(cipher.encrypt(message))

    def decrypt_func(key, message):
        cipher = Columnar(key)
        print(message)
        print(cipher.decrypt(message))

    def hack_func(method, message, dictionary_filepath='/Users/neilmarshall/Documents/Programming/python/ciphers/sandbox/CrackingCodesFiles/dictionary.txt'):
        if method != "brute":
            raise NotImplementedError("Columnar class only supports brute-force method")
        de = DetectEnglish(dictionary_filepath)
        def compare_keys(k):
            decrypted_message = Columnar(k).decrypt(message)
            return de.english_score(decrypted_message.split())
        expected_key = max(range(1, len(message) + 1), key=compare_keys)
        print(f"With key = {expected_key}:")
        print(f"\tOutput: {Columnar(expected_key).decrypt(message)}")

    Parser(encrypt_func, decrypt_func, hack_func)()
