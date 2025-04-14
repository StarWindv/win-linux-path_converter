from stv_path_converter.core.stv_parse import stv_parse
from stv_path_converter.utils.head import *

__version__ = "0.0.1"

def main(__version__ = __version__):
    args = stv_parse()

    if args.license:
        from stv_path_converter.utils.lic import return_license
        print(return_license())
        return

    if args.version:
        print(__version__)
        return

    from stv_path_converter.core.converter import PathConverter
    converter = PathConverter(args)
    if args.input_file:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            paths = [line.strip() for line in f]
    elif not sys.stdin.isatty():
        paths = [line.strip() for line in sys.stdin]
    else:
        paths = args.paths

    # Process paths
    for path in paths:
        if not path:
            continue
        converted = converter.convert(path)
        if converted:
            print(converted)
        elif args.verbose:
            sys.stderr.write(f"Skipped invalid path: {path}\n")

if __name__ == "__main__":
    main()