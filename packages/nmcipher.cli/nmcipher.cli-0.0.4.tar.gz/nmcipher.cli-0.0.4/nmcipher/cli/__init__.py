from .parser import Parser
from .detect_english import DetectEnglish

from nmcipher.caesar import Caesar
from nmcipher.transposition import Columnar

def caesar(args=None):
    def encrypt_func(*, message=None, key=None, symbols=None, **kwargs):
        if message is None or key is None or symbols is None:
            raise ValueError("missing input parameters")
        cipher = Caesar(key, symbols)
        print(f"Original message: {message}")
        print(f"Encrypted message: {cipher.encrypt(message)}")

    def decrypt_func(*, message=None, key=None, symbols=None, **kwargs):
        if message is None or key is None or symbols is None:
            raise ValueError("missing input parameters")
        cipher = Caesar(key, symbols)
        print(f"Encrypted message: {message}")
        print(f"Decrypted message: {cipher.decrypt(message)}")

    def hack_func(*, message=None, symbols=None, dictionary_filepath=None, **kwargs):
        if message is None or symbols is None:
            raise ValueError("missing input parameters")
        if dictionary_filepath is None:
            for key in range(len(symbols)):
                cipher = Caesar(key, symbols)
                print(f"Checking key '{key}':")
                print(f"\tOutput: {cipher.decrypt(message)}")
        else:
            de = DetectEnglish(dictionary_filepath)
            def compare_keys(k):
                decrypted_message = Caesar(k, symbols).decrypt(message)
                return de.english_score(decrypted_message.split())
            expected_key = max(range(1, len(message) + 1), key=compare_keys)
            print(f"Checking key '{expected_key}':")
            print(f"\tOutput: {Caesar(expected_key, symbols).decrypt(message)}")

    Parser(encrypt_func, decrypt_func, hack_func)(args)


def transposition(args=None):
    def encrypt_func(*, message=None, key=None, **kwargs):
        if message is None or key is None:
            raise ValueError("missing input parameters")
        cipher = Columnar(key)
        print(f"Original message: {message}")
        print(f"Encrypted message: {cipher.encrypt(message)}")

    def decrypt_func(*, message=None, key=None, **kwargs):
        if message is None or key is None:
            raise ValueError("missing input parameters")
        cipher = Columnar(key)
        print(f"Encrypted message: {message}")
        print(f"Decrypted message: {cipher.decrypt(message)}")

    def hack_func(*, message=None, dictionary_filepath=None, **kwargs):
        if message is None:
            raise ValueError("missing input parameters")
        if dictionary_filepath is None:
            for key in range(len(message) // 2):
                cipher = Columnar(key)
                print(f"Checking key '{key}':")
                print(f"\tOutput: {cipher.decrypt(message)}")
        else:
            de = DetectEnglish(dictionary_filepath)
            def compare_keys(k):
                decrypted_message = Columnar(k).decrypt(message)
                return de.english_score(decrypted_message.split())
            expected_key = max(range(1, len(message) + 1), key=compare_keys)
            print(f"Checking key '{expected_key}':")
            print(f"\tOutput: {Columnar(expected_key).decrypt(message)}")

    Parser(encrypt_func, decrypt_func, hack_func)(args)
