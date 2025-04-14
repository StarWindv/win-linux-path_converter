from stv_utils import is_ch

def parse_text():
    if is_ch():

        title = "==========+ 在 Windows 与 Linux 之间进行路径格式转换 +=========="

        direction_help = "转换方向"
        style_help = "转换样式"
        mount_prefix_help = "自定义挂载前缀（例如 /my-mount/）"

        # 格式选项
        quote_help = "引号处理策略"
        trailing_slash_help = "尾部斜杠处理方式"
        lower_help = "强制输出小写"
        upper_help = "强制输出大写"

        # 高级选项
        expand_env_help = "展开环境变量"
        validate_help = "验证Windows路径"
        verbose_help = "显示详细输出"

        # 输入处理
        paths_help = "要转换的路径（为空则从标准输入读取）"
        input_file_help = "从文件中读取路径"

        license_help = "显示许可证信息"
        version_help = "显示项目版本"

    else:

        title = "==========+ Convert paths between Windows and Linux formats +=========="

        direction_help = "Conversion direction"
        style_help = "Conversion style"
        mount_prefix_help = "Custom mount prefix (e.g. /my-mount/)"

        quote_help = "Quote handling strategy"
        trailing_slash_help = "Trailing slash handling"
        lower_help = "Force lowercase output"

        upper_help = "Force uppercase output"
        expand_env_help = "Expand environment variables"
        validate_help = "Validate Windows paths"

        verbose_help = "Show verbose output"
        paths_help = "Paths to convert (read from stdin if empty)"
        input_file_help = "Read paths from file"

        license_help = "Show license information"

        version_help = "Show project version"


    array = [title,
             direction_help, style_help, mount_prefix_help,
             quote_help, trailing_slash_help, lower_help,
             upper_help, expand_env_help, validate_help,
             verbose_help, paths_help, input_file_help,
             license_help, version_help]

    return array