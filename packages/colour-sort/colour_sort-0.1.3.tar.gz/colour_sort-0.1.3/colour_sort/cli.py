import argparse
import itertools
import sys
import typing

from PIL import Image
from colour_sort import image, verify, sort_type

CLI_SYNTAX_ERROR = 2

def generate_image(args):
    infile = args.infile
    outfile = args.outfile
    sort_type_ = args.sort

    input_image = Image.open(infile)
    mode = sort_type.SortType.from_str(sort_type_)

    generated = image.create_sorted_image(input_image, mode=mode)
    generated.save(outfile)


def verify_image(args):
    infile = args.infile
    input_image = Image.open(infile)
    valid = verify.verify_image(input_image)
    if valid:
        print('%s is a valid allrgb image!' % infile)
    else:
        print('%s is not a valid allrgb image' % infile)


def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    generate_parser = subparsers.add_parser('generate')
    generate_parser.add_argument('infile')
    generate_parser.add_argument('outfile')
    generate_parser.add_argument('--sort', default='brightness', choices=[mode.name.lower() for mode in sort_type.SortType])
    generate_parser.set_defaults(func=generate_image)

    verify_parser = subparsers.add_parser('verify')
    verify_parser.add_argument('infile')
    verify_parser.set_defaults(func=verify_image)

    args = parser.parse_args()
    if not args.subparser_name:
        parser.print_usage(file=sys.stderr)
        print(f'colour: error: one of the following arguments is required: {", ".join(subparsers.choices.keys())}', file=sys.stderr)
        sys.exit(CLI_SYNTAX_ERROR)

    args.func(args)

if __name__ == '__main__':
    run()
