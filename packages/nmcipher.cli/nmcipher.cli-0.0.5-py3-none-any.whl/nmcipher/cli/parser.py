import argparse

class Parser():
    """
    >>> encrypt_func = lambda **kwargs: kwargs["message"][::-1]
    >>> decrypt_func = lambda **kwargs: kwargs["message"][::-1]
    >>> hack_func = lambda **kwargs: kwargs["message"][::-1]
    >>> parser = Parser(encrypt_func, decrypt_func, hack_func)

    >>> parser(["encrypt", "--key", "4", "--message", "ABC"])
    'CBA'

    >>> parser(["dec", "-k", "4", "-m", "CBA"])
    'ABC'

    >>> parser(["hack", "-m", "CBA"])
    'ABC'
    """

    def __init__(self, encrypt_func, decrypt_func, hack_func):

        # create argument parser
        self.parser = argparse.ArgumentParser(description="encrypt and decrypt messages")
        subparsers = self.parser.add_subparsers(description="valid subcommands", dest="subcommand")

        # add encryption subcommand
        encrypt_parser = subparsers.add_parser("encrypt", aliases=["enc"], help="encrypt a message")
        encrypt_parser.add_argument("--message", "-m", type=str, help="message to encrypt")
        encrypt_parser.add_argument("--key", "-k", type=int, help="encryption key")
        encrypt_parser.add_argument("--symbols", "-s", type=str, help="encryption symbols")
        encrypt_parser.set_defaults(func=encrypt_func)

        # add decryption subcommand
        decrypt_parser = subparsers.add_parser("decrypt", aliases=["dec"], help="decrypt an encrypted message")
        decrypt_parser.add_argument("--message", "-m", type=str, help="message to decrypt")
        decrypt_parser.add_argument("--key", "-k", type=int, help="decryption key")
        decrypt_parser.add_argument("--symbols", "-s", type=str, help="decryption symbols")
        decrypt_parser.set_defaults(func=decrypt_func)

        # add hack subcommand
        hack_parser = subparsers.add_parser("hack", help="hack an encrypted message")
        hack_parser.add_argument("--message", "-m", type=str, help="message to decrypt")
        hack_parser.add_argument("--symbols", "-s", type=str, help="decryption symbols")
        hack_parser.add_argument("--dictionary", "-d", type=str, help="filepath to dictionary of known words")
        hack_parser.set_defaults(func=hack_func)

    def __call__(self, args=None):
        parsed_args = self.parser.parse_args(args)

        kwargs = None
        if parsed_args.subcommand in {"encrypt", "enc"}:
            kwargs = {"message": parsed_args.message, "key": parsed_args.key, "symbols": parsed_args.symbols}
        elif parsed_args.subcommand in {"decrypt", "dec"}:
            kwargs = {"message": parsed_args.message, "key": parsed_args.key, "symbols": parsed_args.symbols}
        elif parsed_args.subcommand in {"hack"}:
            kwargs = {"message": parsed_args.message, "symbols": parsed_args.symbols, "dictionary_filepath": parsed_args.dictionary}
        else:
            raise ValueError("subcommand not recognised")

        return parsed_args.func(**kwargs)
