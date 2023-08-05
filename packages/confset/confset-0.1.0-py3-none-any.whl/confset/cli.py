import sys
from .arguments import ConfsetArguments, create_arg_parser


def main():
    parser = create_arg_parser()
    (options, args) = parser.parse_args()
    confset = ConfsetArguments(args, options)

    try:
        confset.execute()
    except FileNotFoundError:
        print('No writable configuration directories found', file=sys.stderr)
        return 1
    return 0
