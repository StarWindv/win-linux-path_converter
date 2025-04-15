# STV Path Converter 🌐  

A smart and versatile command-line tool that supports flexible conversion between Windows and Linux path formats, offering style customization and advanced formatting options.  

[中文版](./README.md)  

---  

## Key Features ✨  

- **Automatic Direction Detection**: Intelligently identifies input path format (Windows ↔ Linux).  
- **Multi-Style Support**: Compatible with WSL, Cygwin, and POSIX path standards.  
- **Environment Variable Handling**: Optionally expands or preserves environment variables (`%VAR%` ↔ `$VAR`).  
- **Custom Mount Prefix**: Define personalized mount points (e.g., `/my-mount/`).  
- **Format Control**:  
   - Quote handling policy (`always`/`auto`/`never`)  
   - Trailing slash management  
   - Case conversion (force lowercase/uppercase)  
- **Path Validation**: Checks for illegal characters in Windows paths.  
- **Batch Processing**: Supports reading paths from files or standard input.  

---  

## Installation Guide 📦  

### Install via pip  
```bash  
pip install stv_path_converter  
```  

### Build from Source  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/StarWindv/win-linux-path_converter  
   ```  
2. Install using pip:  
   ```bash  
   cd win-linux-path_converter  
   pip install .  
   ```  

---  

## Usage Examples 🛠️  

### Basic Conversion  
```bash  
stv_path "C:\Program Files"  
# Output: /mnt/c/Program\ Files  

stv_path "/my_mount/c/user/docs" -m my_mount  
# Output: C:\home\user\docs  
```  

### Quick Reference for Advanced Options  
| Option                  | Description                                  |  
|-------------------------|---------------------------------------------|  
| `-d, --direction`     | Conversion direction: `auto` (default), `win-to-linux`, `linux-to-win` |  
| `-s, --style`         | Conversion style: `wsl`, `cygwin`, `posix` (default: `wsl`) |  
| `-m, --mount-prefix`  | Custom mount prefix (e.g., `/my-mount/`)    |  
| `-q, --quote`         | Quote handling policy (`auto`/`always`/`never`) |  
| `-t, --trailing-slash`| Trailing slash handling (`keep`/`always`/`never`) |  
| `--lower/--upper`     | Force lowercase/uppercase output            |  
| `-e, --expand-env`    | Expand environment variables                |  
| `--validate`          | Validate Windows path legality             |  

### Scenario Examples  
1. Convert Windows UNC path to WSL format:  
   ```bash  
   stv_path "\\server\share\file.txt" --style wsl  
   # Output: /mnt/server/share/file.txt  
   ```  

2. Convert Cygwin path to quoted Windows path:  
   ```bash  
   stv_path -d linux-to-win "/cygdrive/d/My Documents" --quote always  
   # Output: "D:\My Documents"  
   ```  

3. Batch convert paths from a file:  
   ```bash  
   stv_path -i paths.txt  
   ```  

---  

## Project Structure 🌳  

```
.
├── LICENSE  
├── README.md  
├── pyproject.toml  
└── src  
    └── stv_path_converter  
        ├── __init__.py  
        ├── core  
        │   ├── __init__.py  
        │   ├── converter.py    # Core conversion logic  
        │   └── stv_parse.py    # Path parsing utilities  
        ├── main.py             # CLI entry point  
        ├── text  
        │   ├── __init__.py  
        │   └── change_text.py  # Text formatting helpers  
        └── utils  
            ├── __init__.py  
            ├── head.py         # Header utilities  
            └── lic.py          # License management  
```  

---  

## Contribution Guidelines 🤝  

Contributions are welcome! Feel free to submit issues and PRs anytime!  

---  

## License 📜  

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.  

---  

<sub>🛠️ Crafted for cross-platform developers.</sub>  

### Version Highlights  
- **Localization Optimization**: Technical terminology tailored for Chinese users  
- **Format Adaptation**: Complies with Chinese punctuation and typesetting conventions  
- **Scenario-Based Examples**: Practical demonstrations aligned with real development needs  
- **Clear Structure**: Maintains consistent hierarchy with the English version
