#!/usr/bin/env python
import argparse
import asyncio
import logging
import sys
import os
from PIL import Image, ImageDraw, ImageFont

from catprinter import logger
from catprinter.cmds import PRINT_WIDTH, cmds_print_img
from catprinter.ble import run_ble
from catprinter.img import read_img, show_preview


def parse_args():
    args = argparse.ArgumentParser(
        description='Prints an image or text on your cat thermal printer.')
    args.add_argument('filename', type=str, nargs='?', default=None, 
                      help='Path to the image file or text string to print.')
    args.add_argument('-t', '--text', type=str, 
                      help='Text string to convert to an image and print (use \\n for new lines).')
    args.add_argument('-l', '--log-level', type=str,
                      choices=['debug', 'info', 'warn', 'error'], default='info')
    args.add_argument('-b', '--img-binarization-algo', type=str,
                      choices=['mean-threshold', 'floyd-steinberg', 'halftone', 'none'],
                      default='floyd-steinberg',
                      help=f'Which image binarization algorithm to use. If \'none\' is used, no binarization will be used. In this case, the image has to have a width of {PRINT_WIDTH} px.')
    args.add_argument('-s', '--show-preview', action='store_true',
                      help='If set, displays the final image and asks the user for confirmation before printing.')
    args.add_argument('-d', '--device', type=str, default='',
                      help=('The printer\'s Bluetooth Low Energy (BLE) address '
                            '(MAC address on Linux; UUID on macOS) '
                            'or advertisement name (e.g.: "GT01", "GB02", "GB03"). '
                            'If omitted, the script will try to auto discover '
                            'the printer based on its advertised BLE services.'))
    args.add_argument('-darker', action='store_true',
                      help="Print the image in text mode. This leads to more contrast, but slower speed.")
    args.add_argument('-f', '--font', type=str, default='arial.ttf',
                      help='Path to a TTF font file to use for the text.')
    args.add_argument('--font-size', type=int, default=20,
                      help='Font size to use for the text.')
    return args.parse_args()


def configure_logger(log_level):
    logger.setLevel(log_level)
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(log_level)
    logger.addHandler(h)


def text_to_image(text, output_path, font_path, font_size):
    # Create an image from the text
    font = ImageFont.truetype(font_path, font_size)
    
    # Split text into lines
    lines = text.split('\n')
    
    # Create a temporary image to get the text size for all lines
    temp_image = Image.new('1', (1, 1))  # 1x1 image to avoid creating a large image
    draw = ImageDraw.Draw(temp_image)

    # Calculate the width and height needed for the multi-line text
    max_width = 0
    total_height = 0

    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = text_bbox[2] - text_bbox[0]
        line_height = text_bbox[3] - text_bbox[1]
        max_width = max(max_width, line_width)
        total_height += line_height

    # Create a new image with the appropriate dimensions
    image = Image.new('1', (max_width, total_height), 1)  # Create a white image
    draw = ImageDraw.Draw(image)
    
    # Draw each line of text on the image
    current_y = 0
    for line in lines:
        draw.text((0, current_y), line, fill=0, font=font)  # Draw the text on the image
        current_y += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]  # Update y position for the next line

    # Save the image to the output path
    image.save(output_path)


def main():
    args = parse_args()

    log_level = getattr(logging, args.log_level.upper())
    configure_logger(log_level)

    # Check if text is provided and convert it to an image
    if args.text:
        filename = 'output_image.png'  # Temporary filename for the image
        text_to_image(args.text, filename, args.font, args.font_size)
    elif args.filename:
        filename = args.filename
        if not os.path.exists(filename):
            logger.info('🛑 File not found. Exiting.')
            return
    else:
        logger.info('🛑 No input provided. Exiting.')
        return

    try:
        bin_img = read_img(
            filename,
            PRINT_WIDTH,
            args.img_binarization_algo,
        )
        if args.show_preview:
            show_preview(bin_img)
    except RuntimeError as e:
        logger.error(f'🛑 {e}')
        return

    logger.info(f'✅ Read image: {bin_img.shape} (h, w) pixels')
    data = cmds_print_img(bin_img, dark_mode=args.darker)
    logger.info(f'✅ Generated BLE commands: {len(data)} bytes')

    # Try to autodiscover a printer if --device is not specified.
    asyncio.run(run_ble(data, device=args.device))


if __name__ == '__main__':
    main()
