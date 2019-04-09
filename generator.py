#!/usr/bin/env python3

from sys import argv,stderr,stdout,exit
import argparse
from encodings.aliases import aliases
from codecs import encode as cencode
from pathlib import Path

ENCODINGS = list(set(aliases.values()))
ENCODINGS.remove('rot_13')

for e in ENCODINGS:
    if e.startswith('base'):
        ENCODINGS.pop(ENCODINGS.index(e))

def encode(s,encoding='utf-16'):
    'UTF-16 encode the string and return each char URI encoded'

    try:
        return ''.join(['%{:0>2x}'.format(b) for b in cencode(s,encoding)])
    except TypeError as e:
        if e.__str__() == "TypeError: a bytes-like object is required, not 'str'":
            return ''.join(['%{:0>2x}'.format(b) for b in cencode(bytes(s),encoding)])
    except LookupError as e:
        return None
    except Exception as e:
        print(f'[+] Failed encoding for: {encoding}',file=stderr)
        print(f'Error Message: {e}',file=stderr)
        return None

if __name__ == '__main__':

    # =========
    # INTERFACE
    # =========

    parser = argparse.ArgumentParser(prog='encoder',
        description='Encode a string')

    # Input Group
        # Accepts either an input string to encode or a list of file names
        # If file names are given, each string is encoded and returned
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--string','-s',
        help='String to encode')
    input_group.add_argument('--input-files','-i',
        nargs='+',
        help='One or more input files. Each line will be encoded in varying '\
            'encoders and returned to stdout')

    # Encoder Group
        # Determines which encoders are applied to each target string
        # Can be a list of encoders or all encoders
    encoder_group = parser.add_mutually_exclusive_group(required=True)
    encoder_group.add_argument('--encoders','-e',
        choices=ENCODINGS,
        default='utf_16',
        nargs='+',
        help='Encoding. See `codecs` module for valid values.')
    encoder_group.add_argument('--all-encoders','-a',
        action='store_true',
        help='Encode with all encoders instead of specific encoders')

    # Lookup Group
        # Determines if a lookup operation should be performed
        # Common encodings flags will return only the most common encoding formats
        # (helps with noise reduction)
    lookup_group = encoder_group.add_argument_group()
    encoder_group.add_argument('--lookup','-l',
        help='Return the encoding for a given encoded value. Useful when'\
        ' multiple encoders were attempted in sequence')
    parser.add_argument('--common-encodings-only','-c',
        action='store_true',
        help='Return only common encodings: utf, ascii')

    args = parser.parse_args()

    # =========================
    # BEGINNING EXECUTION LOGIC
    # =========================

    if args.string:
        print(f'[+] Encoding (no leading/trailing quotes): \'{args.string}\'',file=stderr)
    elif args.input_files:
        print(f'[+] Encoding lines from files',file=stderr)
    elif args.lookup:
        print(f'[+] Looking up encoding for: \'{args.string}\'',file=stderr)

    # Filter encoders
    if args.all_encoders or args.lookup:
        encoders = ENCODINGS
    else:
        encoders = args.encoders

    # Verify input files are valid
    if args.input_files:

        for f in args.input_files:
            p = Path(f)
            assert p.exists() and p.is_file(), (
                f'Input file does not exist or is not a file: {f}'
            )

    # ==============
    # ENCODE STRINGS
    # ==============

    # Store all encoded strings
    encoded = []

    # Used when performing a lookup
        # tracks all encodings that return a matching string
    encodings = []
    for e in encoders:

        # Encode a single string
        if args.string:

            s = encode(args.string,e)
            if s and not s in encoded: encoded.append(s)
            if args.lookup and s == args.lookup and e not in encodings:
                encodings.append(e)

        # Encode all lines in each input file
            # Doing the same as above on a per-line basis
        else:

            for f in args.input_files:

                with open(f) as infile:

                    for line in infile:

                        line = line.strip()
                        s = encode(line,e)
                        if s and not s in encoded: encoded.append(s)
                        if args.lookup and s == args.lookup and e not in encodings:
                            encodings.append(e)

    # Determine if there was a match and print relevant information
    if args.lookup:

        if not encodings: print('[+] No match identified')
        else:
            from re import search
            encodings = sorted(encodings)
            common_encodings = [e for e in encodings if search(r'utf|ascii',e)]
            print('[+] Common Encodings:',file=stderr)
            print(','.join(common_encodings))
            if not args.common_encodings_only:
                print('[+] All Encodings:',file=stderr)
                print(','.join(encodings))

    # Dump encoded values to stdout
    else:

        print('\n'.join(encoded))

    print('[+] Done!',file=stderr)
