#!/usr/bin/env python
import argparse
import asyncio
import logging
import sys
import os

from catprinter import logger
from catprinter.cmds import cmds_print_text
from catprinter.ble import run_ble


def parse_args():
    args = argparse.ArgumentParser(
        description='Prints text on your cat thermal printer.')
    args.add_argument('filename', type=str, nargs='?', default=None, 
                      help='Path to the text file to print.')
    args.add_argument('-t', '--text', type=str, 
                      help='Text string to print (use \\n for new lines).')
    args.add_argument('-l', '--log-level', type=str,
                      choices=['debug', 'info', 'warn', 'error'], default='info')
    args.add_argument('-d', '--device', type=str, default='',
                      help=('The printer\'s Bluetooth Low Energy (BLE) address '
                            '(MAC address on Linux; UUID on macOS) '
                            'or advertisement name (e.g.: "GT01", "GB02", "GB03"). '
                            'If omitted, the script will try to auto discover '
                            'the printer based on its advertised BLE services.'))
    args.add_argument('-f', '--font-size', type=int, default=10,
                      help='Font size to use for the text.')
    return args.parse_args()


def configure_logger(log_level):
    logger.setLevel(log_level)
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(log_level)
    logger.addHandler(h)


def print_text(text, device):
    """ Function to send raw text to the printer """
    if not text:
        logger.info('🛑 No text provided to print. Exiting.')
        return

    logger.info(f'✅ Text to print:\n{text}')
    # Send the text directly to the printer (assuming it supports this)
    data = cmds_print_text(text)  # Assuming cmds_print_text sends text commands to the printer
    logger.info(f'✅ Generated printer commands: {len(data)} bytes')

    # Try to autodiscover a printer if --device is not specified
    asyncio.run(run_ble(data, device=device))


def main():
    args = parse_args()

    log_level = getattr(logging, args.log_level.upper())
    configure_logger(log_level)

    text_to_print = ''
    
    if args.text:
        text_to_print = args.text
    elif args.filename:
        if not os.path.exists(args.filename):
            logger.info('🛑 File not found. Exiting.')
            return
        with open(args.filename, 'r') as f:
            text_to_print = f.read()

    print_text(text_to_print, args.device)


if __name__ == '__main__':
    main()
