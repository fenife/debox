#!/bin/env python3

# vscode 插件下载
# https://vsc-extension.dreamsoul.cn/

# 参考
# https://zhuanlan.zhihu.com/p/26003070992

# platform选项：
# win32-x64: Windows 64-bit
# win32-ia32: Windows 32-bit
# win32-arm64: Windows ARM64
# darwin-x64: macOS Intel
# darwin-arm64: macOS Apple Silicon
# linux-x64: Linux 64-bit
# linux-arm64: Linux ARM64
# alpine-x64: Alpine Linux

def _gen_vsix_url(vsix_info: str) -> str:
    """生成VSIX文件下载URL的简化版本"""
    lines = [line.strip()
             for line in vsix_info.strip().split('\n') if line.strip()]
    publisher, name = lines[lines.index("Identifier") + 1].split('.')
    version = lines[lines.index("Version") + 1]
    return f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{name}/{version}/vspackage"

def gen_vsix_url(ident, ver) -> str:
    """生成VSIX文件下载URL的简化版本"""
    publisher, name = ident.split('.')
    version = ver
    platform = 'linux-x64'
    url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{name}/{version}/vspackage"

    url += "?targetPlatform={platform}"

    print(f"VSIX: {ident}")
    print(f"{url}")
    print()


if __name__ == '__main__':
    vsix_info = '''
    Identifier
    vscodevim.vim
    Version
    1.32.4
    '''
    vsix_list = [
        # ident, version
        # ["vscodevim.vim", "1.32.4"],
        # ["ms-python.python", "2025.0.0"],
        # ["ms-python.vscode-pylance", "2025.10.2"],
        # ["ms-python.debugpy", "2025.18.0"],
        # ["ms-python.python", "2021.12.1559732655"],
        # ["ms-ceintl.vscode-language-pack-zh-hans", "1.102.2025071609"],
        # ["golang.go", "0.52.2"],
        ["maattdd.gitless", "11.7.2"],
    ]

    for v in vsix_list:
        gen_vsix_url(v[0], v[1])
