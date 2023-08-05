# __main__.py

# from importlib import resources  # Python 3.7+
# import sys

import argparse
from whatsapp_converter import whatsapp_converter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the WhatsApp file containing the exported chat")
    parser.add_argument("resultset", help="filename of the resultset", default="resultset.csv", nargs='*')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--debug", help="increase output verbosity to debug", action="store_true")

    # parser.add_argument("-nl", "--newline", help="message across various lines is counted as a new message", action="store_true")
    args = parser.parse_args()

    print ("WhatsApp Converter to read exported chat files from WhatsApp and convert them to a CSV file")
    whatsapp_converter.convert(filename=args.filename, resultset=args.resultset, verbose=args.verbose, debug=args.debug)

if __name__ == "__main__":
    main()
