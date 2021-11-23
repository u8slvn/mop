import argparse
import re

from mop import Mop


def extension_list(arg_value, pat=re.compile(r"^(.[a-z0-9]*){1,2}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value


def parse_args():
    parser = argparse.ArgumentParser(description='File deletion based on extension.')
    parser.add_argument(
        metavar='dir_path',
        dest="dir_path",
        type=str,
        help="The path directory to clean up.",
    )
    parser.add_argument(
        '-e',
        '--ext',
        dest='extensions',
        type=extension_list,
        default="",
        help="List of file extensions to delete.",
    )
    parser.add_argument(
        '-r',
        '--recursive',
        required=False,
        dest='recursive',
        action='store_true',
        help="Recursive mode, delete file matching extensions in all sub folders."
    )
    parser.add_argument(
        '-x',
        '--exclude',
        required=False,
        dest='exclude',
        action='store_true',
        help="Switch to exclude mode, all the listed extension will be preserved from deletion."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    mop = Mop(
        dir_path=args.dir_path,
        extensions=args.extensions,
        recursive=args.recursive,
        exclude=args.exclude,
    )
    while True:
        ok = input(f"Mop collected {mop.files_to_delete_count} file(s) to delete, do you agree: [y/N]: ") or "n"
        if ok.lower() == "y":
            mop.clean()
            break
        if ok.lower() == "n":
            break
