from stv_path_converter.text.change_text import parse_text
import argparse

def  stv_parse():

    pt = parse_text()

    parser = argparse.ArgumentParser(
        description=pt[0],
        epilog='Example: stv_path_converter --win-to-linux "C:\\Program Files"'
    )

    parser.add_argument('-d', '--direction',
                        choices=['auto', 'win-to-linux', 'linux-to-win'],
                        default='auto',
                        help=pt[1])
    parser.add_argument('-s', '--style', choices=['wsl', 'cygwin', 'posix'],
                        default='wsl', help=pt[2])
    parser.add_argument('-m', '--mount-prefix',
                        help=pt[3])

    # 格式选项
    parser.add_argument('-q', '--quote',
                        choices=['never', 'auto', 'always'], default='auto',
                        help=pt[4])
    parser.add_argument('-t', '--trailing-slash',
                        choices=['keep', 'always', 'never'], default='keep',
                        help=pt[5])
    parser.add_argument('--lower', action='store_true',
                        help=pt[6])
    parser.add_argument('--upper', action='store_true',
                        help=pt[7])

    # 高级选项
    parser.add_argument('-e', '--expand-env', action='store_true',
                        help=pt[8])
    parser.add_argument('--validate', action='store_true',
                        help=pt[9])
    parser.add_argument('-v', '--verbose', action='store_true',
                        help=pt[10])

    # 输入处理
    parser.add_argument('paths', nargs='*',
                        help=pt[11])
    parser.add_argument('-i', '--input-file',
                        help=pt[12])

    parser.add_argument('-lic', '--license', action='store_true',
                        help=pt[13])

    parser.add_argument('-V', '--version', action='store_true',
                        help=pt[14])

    args = parser.parse_args()
    return args