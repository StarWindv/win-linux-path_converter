from stv_path_converter.utils.head import *


class PathConverter:
    def __init__(self, args):
        self.args = args
        self.env_var_pattern = re.compile(r'(%\w+%|\$\w+)')
        self.windows_path_pattern = re.compile(
            r'^(?:([a-zA-Z]:)|(\\\\[^\\]+\\[^\\]+)|([\\\\/]{2,}))([\\\\/].*)?$',
            re.IGNORECASE
        )
        self.mount_map = {
            'wsl': '/mnt/',
            'cygwin': '/cygdrive/',
            'posix': '/'
        }

    def convert(self, input_path):
        try:
            if self.args.direction == 'auto':
                direction = self.detect_direction(input_path)
            else:
                direction = self.args.direction

            if direction == 'win-to-linux':
                return self.win_to_linux(input_path)
            else:
                return self.linux_to_win(input_path)
        except Exception as e:
            if self.args.verbose:
                sys.stderr.write(f"Error converting {input_path}: {str(e)}\n")
            return None

    def detect_direction(self, path):
        if re.match(r'^[a-zA-Z]:[\\/]', path) or re.match(r'^\\\\', path):
            return 'win-to-linux'
        elif re.match(r'^(/mnt/|/cygdrive/)', path):
            return 'linux-to-win'
        return 'linux-to-win' if '/' in path else 'win-to-linux'

    def win_to_linux(self, path):
        # Normalize separators and resolve escapes
        path = path.replace('\\', '/').replace('//', '/')

        # Handle quoted paths
        quoted = False
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
            quoted = True

        # Resolve environment variables
        if self.args.expand_env:
            path = os.path.expandvars(path)
        else:
            path = path.replace('%', '$')

        # Process special paths
        match = self.windows_path_pattern.match(path)
        if match:
            drive, unc, legacy_unc, rest = match.groups()
            if drive:  # Standard Windows path
                drive_letter = drive[0].lower()
                mount_prefix = self.args.mount_prefix or self.mount_map.get(self.args.style, '/mnt/')
                # new_path = f"{mount_prefix}{drive_letter}{rest or ''}"
                rest = (rest or '').replace('\\', '/')  # 确保剩余路径的斜杠方向
                new_path = f"{mount_prefix}{drive_letter}{rest}"
            elif unc:  # UNC path
                unc_parts = unc.split('\\')
                new_path = f"/mnt/{unc_parts[2]}/{unc_parts[3]}{rest or ''}"
            else:  # Legacy path
                new_path = path
        else:  # Relative path
            new_path = path

        # Handle special characters
        new_path = self.escape_special_chars(new_path, 'linux')

        # Case handling
        new_path = self.apply_case(new_path)

        # Trailing slash
        new_path = self.process_trailing_slash(new_path)

        return self.quote_result(new_path, quoted)


    def linux_to_win(self, path):
        # if path.startswith('/cygdrive/'):
        #     mount_prefix = '/cygdrive/'
        #     style_override = 'cygwin'  # 标记为 Cygwin 风格
        # elif path.startswith('/mnt/'):
        #     mount_prefix = '/mnt/'
        #     style_override = 'wsl'     # 标记为 WSL 风格
        # else:
        #     # 如果用户未指定 mount_prefix，则根据 style 参数回退
        #     mount_prefix = self.args.mount_prefix or self.mount_map.get(self.args.style, '/mnt/')
        #     style_override = None

        # 新增 mount_prefix 规范化逻辑（替换删除的部分）：
        mount_prefix = self.args.mount_prefix or self.mount_map.get(self.args.style, '/mnt/')
        # 强制统一为 POSIX 格式（确保以 / 开头和结尾）
        mount_prefix = mount_prefix.replace('\\', '/').rstrip('/') + '/'
        if not mount_prefix.startswith('/'):
            mount_prefix = '/' + mount_prefix


        # Normalize path（保留空格转义处理）
        path = path.replace('\\ ', ' ')

        # Handle quoted paths
        quoted = False
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
            quoted = True

        # Resolve mount points
        if path.startswith(mount_prefix):
            # 分割路径（例如 /cygdrive/d/My Documents → ["d", "My Documents"]）
            parts = path[len(mount_prefix):].split('/', 1)
            drive_letter = parts[0].upper()
            rest = parts[1].replace('/', '\\') if len(parts) > 1 else ''
            new_path = f"{drive_letter}:\\{rest}"
        elif path.startswith('/'):
            # 根目录默认映射到 C 盘（仅在非挂载点路径时生效）
            default_drive = "C" if style_override != 'cygwin' else mount_prefix.split('/')[2].upper()
            new_path = f"{default_drive}:\\{path[1:].replace('/', '\\')}"
        else:
            # 相对路径直接转换斜杠
            new_path = path.replace('/', '\\')

        # Handle environment variables
        new_path = new_path.replace('$', '%') if not self.args.expand_env else os.path.expandvars(new_path)

        # Validate Windows path
        if self.args.validate and not PureWindowsPath(new_path).is_reserved():
            self.validate_windows_path(new_path)

        # Handle special characters
        new_path = self.escape_special_chars(new_path, 'windows')

        # Case handling
        new_path = self.apply_case(new_path)

        # Trailing slash
        new_path = self.process_trailing_slash(new_path, is_windows=True)

        return self.quote_result(new_path, quoted)

    def validate_windows_path(self, path):
        invalid_chars = re.compile(r'[<>:"|?*]')
        if invalid_chars.search(path):
            raise ValueError(f"Invalid Windows path characters: {path}")

    def escape_special_chars(self, path, target):
        special_chars = ' ()[]{}!$&*?;'
        if target == 'linux':
            for char in special_chars:
                path = path.replace(char, f'\\{char}')
        elif target == 'windows' and ' ' in path:
            path = f'{path}'
        return path

    def apply_case(self, path):
        if self.args.lower:
            return path.lower()
        elif self.args.upper:
            return path.upper()
        return path

    def process_trailing_slash(self, path, is_windows=False):
        if self.args.trailing_slash == 'always':
            return path.rstrip('\\/') + ('\\' if is_windows else '/')
        elif self.args.trailing_slash == 'never':
            return path.rstrip('\\/')
        return path

    def quote_result(self, path, already_quoted):
        if self.args.quote == 'always' and not already_quoted:
            return f'"{path}"'
        return path