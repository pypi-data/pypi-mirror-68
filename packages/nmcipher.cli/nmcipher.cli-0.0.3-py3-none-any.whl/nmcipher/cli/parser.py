import argparse

class Parser():
    """
    >>> encrypt_func = lambda _, m: m[::-1]
    >>> decrypt_func = lambda _, m: m[::-1]
    >>> hack_func = lambda _, m: m[::-1]
    >>> parser = Parser(encrypt_func, decrypt_func, hack_func)

    >>> parser(["enc", "4", "ABC"])
    'CBA'

    >>> parser(["dec", "4", "CBA"])
    'ABC'

    >>> parser(["hack", "brute", "CBA"])
    'ABC'

    >>> parser(["hack", "brute", "ABC", "-s", "ABCDEF", "-d", "filepath"])
    Traceback (most recent call last):
        ...
    SystemExit: 2
    """

    def __init__(self, encrypt_func, decrypt_func, hack_func):

        # create argument parser
        self.parser = argparse.ArgumentParser(description="encrypt and decrypt messages")
        subparsers = self.parser.add_subparsers(description="valid subcommands", dest="subcommand")

        # add encryption subcommand
        encrypt_parser = subparsers.add_parser("encrypt", aliases=["enc"], help="encrypt a message")
        encrypt_parser.add_argument("key", type=int, help="encryption key")
        encrypt_parser.add_argument("message", type=str, help="message to encrypt")
        encrypt_parser.add_argument("--symbols", "-s", type=str, help="encryption symbols")
        encrypt_parser.set_defaults(func=encrypt_func)

        # add decryption subcommand
        decrypt_parser = subparsers.add_parser("decrypt", aliases=["dec"], help="decrypt an encrypted message")
        decrypt_parser.add_argument("key", type=int, help="decryption key")
        decrypt_parser.add_argument("message", type=str, help="message to decrypt")
        decrypt_parser.add_argument("--symbols", "-s", type=str, help="decryption symbols")
        decrypt_parser.set_defaults(func=decrypt_func)

        # add hack subcommand
        hack_parser = subparsers.add_parser("hack", help="hack an encrypted message")
        hack_parser.add_argument("method", choices=["brute"], help="attack method")
        hack_parser.add_argument("message", type=str, help="message to decrypt")
        group = hack_parser.add_mutually_exclusive_group()
        group.add_argument("--symbols", "-s", type=str, help="decryption symbols")
        group.add_argument("--dictionary", "-d", type=str, help="filepath to dictionary of known words")
        hack_parser.set_defaults(func=hack_func)

    def __call__(self, args=None):
        parsed_args = self.parser.parse_args(args)
        if parsed_args.subcommand == "hack":
            if parsed_args.symbols:
                return parsed_args.func(parsed_args.method, parsed_args.message, parsed_args.symbols)
            elif parsed_args.dictionary:
                return parsed_args.func(parsed_args.method, parsed_args.message, parsed_args.dictionary)
            else:
                return parsed_args.func(parsed_args.method, parsed_args.message)
        if parsed_args.symbols:
            return parsed_args.func(parsed_args.key, parsed_args.message, parsed_args.symbols)
        else:
            return parsed_args.func(parsed_args.key, parsed_args.message)
